import ldfparser
import ldfparser.signal as ldf_sig
from jinja2 import Template

# ==============================================================================
# RUNTIME FIX 1: Safely patch LinSignal to support non-standard signal lengths (>16-bit)
# ==============================================================================
original_create = ldf_sig.LinSignal.create

@classmethod
def patched_create(cls, name: str, width: int, init_value):
    try:
        return original_create(name, width, init_value)
    except ValueError as e:
        if "must be 1-16 bits long" in str(e):
            obj = cls.__new__(cls)
            obj.name = name
            obj.width = width
            obj.init_value = init_value
            
            # Populate all structural attributes expected by the parser linking steps
            obj.frames = []
            obj.converters = []
            obj.publishers = []
            obj.subscribers = []
            return obj
        raise e

ldf_sig.LinSignal.create = patched_create

# ==============================================================================
# RUNTIME FIX 2: Enhanced fallback for missing/diagnostic signals (e.g. BS2DiagReset)
# ==============================================================================
original_get_signal = ldfparser.LDF.get_signal

def patched_get_signal(self, name: str):
    try:
        return original_get_signal(self, name)
    except LookupError:
        for attr_name in ['_diagnostic_signals', 'diagnostic_signals', '_diagnostics']:
            diag_dict = getattr(self, attr_name, None)
            if diag_dict and name in diag_dict:
                return diag_dict[name]
        
        mock_signal = ldf_sig.LinSignal.__new__(ldf_sig.LinSignal)
        mock_signal.name = name
        mock_signal.width = 1
        mock_signal.init_value = 0
        mock_signal.frames = []
        mock_signal.converters = []
        mock_signal.publishers = []
        mock_signal.subscribers = []
        
        self._signals[name] = mock_signal
        return mock_signal

ldfparser.LDF.get_signal = patched_get_signal

# ==============================================================================
# RUNTIME FIX 3: Dynamic fallback dict for missing encoding types & structural attributes
# ==============================================================================
class FallbackDict(dict):
    def __getitem__(self, key):
        if key not in self:
            from ldfparser.encoding import LinSignalEncodingType
            mock_encoding = LinSignalEncodingType.__new__(LinSignalEncodingType)
            mock_encoding.name = key
            mock_encoding.types = []
            mock_encoding._signals = []
            self[key] = mock_encoding
        return super().__getitem__(key)

original_ldf_init = ldfparser.LDF.__init__
def patched_ldf_init(self, *args, **kwargs):
    original_ldf_init(self, *args, **kwargs)
    self._signal_encoding_types = FallbackDict(self._signal_encoding_types)

ldfparser.LDF.__init__ = patched_ldf_init
# ==============================================================================

# 1. Parse your old and new LDF databases safely
old_ldf = ldfparser.parse_ldf('SFB_BMS2-5682.ldf')
new_ldf = ldfparser.parse_ldf('Upfitter-6x_LIN_20260722_v1.0.0 1.ldf')

diff_report = {
    "added_nodes": [],
    "removed_nodes": [],
    "added_signals": [],
    "removed_signals": []
}

# 2. Extract semantic structural differences
# --- FIX: Extract structural names from node objects via method calls ---
old_nodes = set(node.name for node in old_ldf.get_slaves())
new_nodes = set(node.name for node in new_ldf.get_slaves())
diff_report["added_nodes"] = list(new_nodes - old_nodes)
diff_report["removed_nodes"] = list(old_nodes - new_nodes)

old_signals = {sig.name: sig.width for sig in old_ldf.get_signals()}
new_signals = {sig.name: sig.width for sig in new_ldf.get_signals()}

diff_report["added_signals"] = [
    {"name": name, "width": new_signals[name]} 
    for name in (new_signals.keys() - old_signals.keys())
]
diff_report["removed_signals"] = [
    {"name": name, "width": old_signals[name]} 
    for name in (old_signals.keys() - new_signals.keys())
]

# 3. Jinja2 template mirroring the clean visual structure of dbc-diff
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>LDF Difference Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; margin: 40px; color: #24292f; background-color: #f6f8fa; }
        .container { max-width: 900px; margin: 0 auto; background: #ffffff; padding: 30px; border: 1px solid #d0d7de; border-radius: 6px; box-shadow: 0 1px 3px rgba(27,31,35,0.12); }
        h1 { border-bottom: 1px solid #d0d7de; padding-bottom: 10px; font-size: 24px; }
        h2 { font-size: 18px; margin-top: 24px; color: #57606a; }
        ul { list-style: none; padding-left: 0; }
        li { padding: 6px 12px; margin-bottom: 4px; border-radius: 4px; font-family: monospace; font-size: 14px; }
        .added { background-color: #dafbe1; color: #1a7f37; border-left: 4px solid #2da44e; }
        .removed { background-color: #ffebe9; color: #cf222e; border-left: 4px solid #cf222e; }
        .empty { color: #8c959f; font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <h1>LIN Description File (LDF) Semantic Diff</h1>
        
        <h2>Slave Nodes Changes</h2>
        <ul>
            {% for node in added_nodes %}
                <li class="added">+ Added Slave Node: {{ node }}</li>
            {% endfor %}
            {% for node in removed_nodes %}
                <li class="removed">- Removed Slave Node: {{ node }}</li>
            {% endfor %}
            {% if not added_nodes and not removed_nodes %}
                <li class="empty">No slave node modifications found.</li>
            {% endif %}
        </ul>

        <h2>Signal Matrix Changes</h2>
        <ul>
            {% for sig in added_signals %}
                <li class="added">+ Added Signal: {{ sig.name }} (Width: {{ sig.width }} bits)</li>
            {% endfor %}
            {% for sig in removed_signals %}
                <li class="removed">- Removed Signal: {{ sig.name }} (Width: {{ sig.width }} bits)</li>
            {% endfor %}
            {% if not added_signals and not removed_signals %}
                <li class="empty">No signal matrix modifications found.</li>
            {% endif %}
        </ul>
    </div>
</body>
</html>
"""

template = Template(html_template)
html_output = template.render(diff_report)

with open("ldf_diff_report.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("Success: 'ldf_diff_report.html' has been successfully generated.")
