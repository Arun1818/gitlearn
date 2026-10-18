import ldfparser
import ldfparser.signal as ldf_sig

# ==============================================================================
# RUNTIME PARSER FIXES (To support non-standard/broken custom LDF attributes)
# ==============================================================================
original_create = ldf_sig.LinSignal.create
@classmethod
def patched_create(cls, name: str, width: int, init_value):
    try:
        return original_create(name, width, init_value)
    except ValueError as e:
        if "must be 1-16 bits long" in str(e):
            obj = cls.__new__(cls)
            obj.name, obj.width, obj.init_value = name, width, init_value
            obj.frames, obj.converters, obj.publishers, obj.subscribers = [], [], [], []
            return obj
        raise e
ldf_sig.LinSignal.create = patched_create

original_get_signal = ldfparser.LDF.get_signal
def patched_get_signal(self, name: str):
    try:
        return original_get_signal(self, name)
    except LookupError:
        for attr in ['_diagnostic_signals', 'diagnostic_signals', '_diagnostics']:
            diag_dict = getattr(self, attr, None)
            if diag_dict and name in diag_dict:
                return diag_dict[name]
        mock_signal = ldf_sig.LinSignal.__new__(ldf_sig.LinSignal)
        mock_signal.name, mock_signal.width, mock_signal.init_value = name, 1, 0
        mock_signal.frames, mock_signal.converters, mock_signal.publishers, mock_signal.subscribers = [], [], [], []
        self._signals[name] = mock_signal
        return mock_signal
ldfparser.LDF.get_signal = patched_get_signal

class FallbackDict(dict):
    def __getitem__(self, key):
        if key not in self:
            from ldfparser.encoding import LinSignalEncodingType
            mock_encoding = LinSignalEncodingType.__new__(LinSignalEncodingType)
            mock_encoding.name, mock_encoding.types, mock_encoding._signals = key, [], []
            self[key] = mock_encoding
        return super().__getitem__(key)

original_ldf_init = ldfparser.LDF.__init__
def patched_ldf_init(self, *args, **kwargs):
    original_ldf_init(self, *args, **kwargs)
    self._signal_encoding_types = FallbackDict(self._signal_encoding_types)
ldfparser.LDF.__init__ = patched_ldf_init
# ==============================================================================

# --- FIX: Safely unpack LinSignal objects into raw strings/integers to prevent sorting crashes ---
def get_frame_signals(frame):
    result = {}
    
    # Check for direct object lists first (most reliable across newer ldfparser versions)
    if hasattr(frame, 'signals') and frame.signals:
        for sig in frame.signals:
            # Handles wrapper objects or direct LinSignal instances
            sig_obj = getattr(sig, 'signal', sig)
            s_name = getattr(sig_obj, 'name', str(sig_obj))
            s_offset = getattr(sig, 'offset', getattr(sig_obj, 'offset', 0))
            result[s_name] = s_offset
        return result

    # Fallback to structural map iteration
    if hasattr(frame, 'signal_map') and frame.signal_map:
        s_map = frame.signal_map
        if isinstance(s_map, dict):
            for k, v in s_map.items():
                s_name = getattr(k, 'name', str(k))
                s_offset = getattr(v, 'offset', v if isinstance(v, (int, float)) else 0)
                result[s_name] = s_offset
        elif isinstance(s_map, list):
            for item in s_map:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    s_name = getattr(item[0], 'name', str(item[0]))
                    result[s_name] = item[1]
                elif hasattr(item, 'name'):
                    result[item.name] = getattr(item, 'offset', 0)
                elif hasattr(item, 'signal'):
                    s_name = getattr(item.signal, 'name', str(item.signal))
                    result[s_name] = getattr(item, 'offset', 0)
                    
    return result

# 1. Parse LDF databases safely
OLD_FILE = 'SFB_BMS2-5682.ldf'
NEW_FILE = 'Upfitter-6x_LIN_20260722_v1.0.0 1.ldf'

old_ldf = ldfparser.parse_ldf(OLD_FILE)
new_ldf = ldfparser.parse_ldf(NEW_FILE)

# 2. Extract Data Maps
old_nodes = set(node.name for node in old_ldf.get_slaves())
new_nodes = set(node.name for node in new_ldf.get_slaves())

old_frm_map = {f.name: f for f in old_ldf.get_unconditional_frames()}
new_frm_map = {f.name: f for f in new_ldf.get_unconditional_frames()}

old_sig_widths = {s.name: s.width for s in old_ldf.get_signals()}
new_sig_widths = {s.name: s.width for s in new_ldf.get_signals()}

# ==============================================================================
# 3. MODULAR WRITING FUNCTIONS
# ==============================================================================
def write_node_section(out):
    out.write("## 1. Network Node Updates\n\n")
    added = sorted(list(new_nodes - old_nodes))
    removed = sorted(list(old_nodes - new_nodes))
    if not added and not removed:
        out.write("No node architecture modifications.\n\n")
    for n in added:
        out.write(f"- **[+] Added Slave Node:** {n}\n")
    for n in removed:
        out.write(f"- **[-] Removed Slave Node:** {n}\n")
    out.write("\n")

def write_added_frames(out):
    added_f = sorted(list(new_frm_map.keys() - old_frm_map.keys()))
    for f_name in added_f:
        f = new_frm_map[f_name]
        f_sigs = get_frame_signals(f)
        out.write(f"### [ADDED FRAME] {f_name}\n")
        out.write(f"- **Frame ID:** {hex(f.frame_id)} | **Size:** {f.length} Bytes | **Publisher:** {getattr(f.publisher, 'name', f.publisher)}\n")
        out.write("- **Nested Signals Layout Matrix:**\n")
        out.write("  | Signal Name | Offset | Length |\n  | --- | --- | --- |\n")
        # --- FIX: Safely sort on the integer bit offset coordinate ---
        for s_name, offset in sorted(f_sigs.items(), key=lambda x: x[1]):
            out.write(f"  | {s_name} | {offset} | {new_sig_widths.get(s_name, 'N/A')} bits |\n")
        out.write("\n")

def write_removed_frames(out):
    removed_f = sorted(list(old_frm_map.keys() - new_frm_map.keys()))
    for f_name in removed_f:
        f = old_frm_map[f_name]
        f_sigs = get_frame_signals(f)
        out.write(f"### [REMOVED FRAME] {f_name}\n")
        out.write(f"- **Frame ID:** {hex(f.frame_id)} | **Size:** {f.length} Bytes\n")
        out.write("- **Nested Signals Layout Matrix:**\n")
        out.write("  | Signal Name | Offset | Length |\n  | --- | --- | --- |\n")
        # --- FIX: Safely sort on the integer bit offset coordinate ---
        for s_name, offset in sorted(f_sigs.items(), key=lambda x: x[1]):
            out.write(f"  | {s_name} | {offset} | {old_sig_widths.get(s_name, 'N/A')} bits |\n")
        out.write("\n")

def check_signal_diffs(out, o_sigs, n_signals):
    for s in sorted(list(n_signals.keys() - o_sigs.keys())):
        out.write(f"| {s} | **ADDED** | Start Bit Offset: {n_signals[s]} \| Width: {new_sig_widths.get(s, 'N/A')} bits |\n")
    for s in sorted(list(o_sigs.keys() - n_signals.keys())):
        out.write(f"| {s} | *REMOVED* | Was at Offset: {o_sigs[s]} \| Width: {old_sig_widths.get(s, 'N/A')} bits |\n")
    for s in sorted(list(o_sigs.keys() & n_signals.keys())):
        mods = []
        if o_sigs[s] != n_signals[s]:
            mods.append(f"• Bit Offset: ~~{o_sigs[s]}~~ -> **{n_signals[s]}**")
        if old_sig_widths.get(s) != new_sig_widths.get(s):
            mods.append(f"• Bit Width: ~~{old_sig_widths.get(s)}~~ -> **{new_sig_widths.get(s)}**")
        if mods:
            out.write(f"| {s} | MODIFIED | {' '.join(mods)} |\n")

def write_changed_frames(out):
    common_f = sorted(list(old_frm_map.keys() & new_frm_map.keys()))
    for f_name in common_f:
        o_f, n_f = old_frm_map[f_name], new_frm_map[f_name]
        o_sigs, n_sigs = get_frame_signals(o_f), get_frame_signals(n_f)
        
        has_f_change = (o_f.frame_id != n_f.frame_id) or (o_f.length != n_f.length) or (getattr(o_f.publisher, 'name', o_f.publisher) != getattr(n_f.publisher, 'name', n_f.publisher))
        has_s_change = (o_sigs != n_sigs) or any(old_sig_widths.get(s) != new_sig_widths.get(s) for s in (o_sigs.keys() & n_sigs.keys()))
        
        if has_f_change or has_s_change:
            out.write(f"### [CHANGED FRAME] {f_name}\n\n")
            if has_f_change:
                out.write("#### Frame Attribute Changes:\n")
                out.write("| Property Name | Old Base Value | New Target Value |\n| --- | --- | --- |\n")
                if o_f.frame_id != n_f.frame_id:
                    out.write(f"| Frame ID | ~~{hex(o_f.frame_id)}~~ | **{hex(n_f.frame_id)}** |\n")
                if o_f.length != n_f.length:
                    out.write(f"| Length (Bytes) | ~~{o_f.length}~~ | **{n_f.length}** |\n")
                if getattr(o_f.publisher, 'name', o_f.publisher) != getattr(n_f.publisher, 'name', n_f.publisher):
                    out.write(f"| Publisher Node | ~~{getattr(o_f.publisher, 'name', o_f.publisher)}~~ | **{getattr(n_f.publisher, 'name', n_f.publisher)}** |\n")
                out.write("\n")
            
            if has_s_change:
                out.write("#### Nested Signal Changes Inside This Frame:\n")
                out.write("| Nested Signal Target | Modification Status | Bit Details / Configuration Shifts |\n| --- | --- | --- |\n")
                check_signal_diffs(out, o_sigs, n_sigs)
                out.write("\n")

# ==============================================================================
# 4. MAIN EXECUTION FLOW
# ==============================================================================
with open("ldf_diff_report.md", "w", encoding="utf-8") as out:
    out.write("# LIN Description File (LDF) Semantic Change Report\n\n")
    out.write(f"- **OLD BASE FILE:** {OLD_FILE}\n")
    out.write(f"- **NEW TARGET FILE:** {NEW_FILE}\n\n")
    
    write_node_section(out)
    
    out.write("## 2. Frame Architecture & Nested Signals Map\n\n")
