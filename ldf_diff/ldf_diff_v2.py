import re

# ==============================================================================
# 1. PURE TEXT-EXTRACTION ENGINE (Bypasses ldfparser object-linking drops)
# ==============================================================================
def extract_ldf_blocks(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return {}, {}, []

    # Extract Nodes
    nodes = []
    nodes_match = re.search(r'Nodes\s*\{(.*?)\}', content, re.DOTALL)
    if nodes_match:
        slave_match = re.search(r'Slaves\s*:\s*([^;]+);', nodes_match.group(1))
        if slave_match:
            nodes = [n.strip() for n in slave_match.group(1).split(',')]

    # Extract Frames & Packed Signals Layout Block
    frames = {}
    frame_matches = re.findall(r'(\w+)\s*:\s*(\w+)\s*,\s*(\w+)\s*,\s*(\d+)\s*\{(.*?)\}', content, re.DOTALL)
    for f_name, f_id, f_pub, f_len, inner in frame_matches:
        signals = []
        sig_lines = re.findall(r'(\w+)\s*,\s*(\d+)\s*;', inner)
        for s_name, offset in sig_lines:
            signals.append({"name": s_name, "offset": int(offset)})
        frames[f_name] = {
            "id": f_id,
            "pub": f_pub,
            "len": f_len,
            "signals": sorted(signals, key=lambda x: x["offset"])
        }

    # Extract Global Signal Bit Widths Matrix
    signals_meta = {}
    sig_block = re.search(r'Signals\s*\{(.*?)\}', content, re.DOTALL)
    if sig_block:
        sig_matches = re.findall(r'(\w+)\s*:\s*(\d+)\s*,', sig_block.group(1))
        for s_name, s_width in sig_matches:
            signals_meta[s_name] = s_width

    return nodes, frames, signals_meta

# ==============================================================================
# 2. FILE LOADING AND ARCHITECTURE EVALUATION
# ==============================================================================
OLD_FILE = 'SFB_BMS2-5682.ldf'
NEW_FILE = 'Upfitter-6x_LIN_20260722_v1.0.0 1.ldf'

old_nodes, old_frames, old_sig_meta = extract_ldf_blocks(OLD_FILE)
new_nodes, new_frames, new_sig_meta = extract_ldf_blocks(NEW_FILE)

# ==============================================================================
# 3. GENERATE ROBUST SCOPED MARKDOWN ENGINE (0% Object Truncation Risk)
# ==============================================================================
with open("ldf_diff_report.md", "w", encoding="utf-8") as out:
    out.write("# LIN Description File (LDF) Semantic Change Report\n\n")
    out.write(f"- **OLD BASE FILE:** {OLD_FILE}\n")
    out.write(f"- **NEW TARGET FILE:** {NEW_FILE}\n\n")
    
    # --- A. Nodes Architecture Block ---
    out.write("## 1. Network Node Updates\n\n")
    o_n, n_n = set(old_nodes), set(new_nodes)
    if not (o_n ^ n_n):
        out.write("No node architecture modifications.\n\n")
    else:
        for n in sorted(list(n_n - o_n)):
            out.write(f"- **[+] Added Slave Node:** {n}\n")
        for n in sorted(list(o_n - n_n)):
            out.write(f"- **[-] Removed Slave Node:** {n}\n")
        out.write("\n")

    # --- B. Scoped Frames Block ---
    out.write("## 2. Frame Architecture & Nested Signals Map\n\n")
    
    # Added Frames Check
    added_frames = sorted(list(set(new_frames.keys()) - set(old_frames.keys())))
    if added_frames:
        out.write("### ➕ Added Frames\n\n")
        for f_name in added_frames:
            f = new_frames[f_name]
            out.write(f"#### frame: **{f_name}**\n")
            out.write(f"- **Frame ID:** {f['id']} | **Size:** {f['len']} Bytes | **Publisher:** {f['pub']}\n")
            out.write("- **Nested Signals Layout Matrix:**\n")
            out.write("  | Signal Variable Target | Bit Offset | Length |\n  | --- | --- | --- |\n")
            for s in f["signals"]:
                out.write(f"  | {s['name']} | {s['offset']} | {new_sig_meta.get(s['name'], 'N/A')} bits |\n")
            out.write("\n")

    # Removed Frames Check
    removed_frames = sorted(list(set(old_frames.keys()) - set(new_frames.keys())))
    if removed_frames:
        out.write("### ➖ Removed Frames\n\n")
        for f_name in removed_frames:
            f = old_frames[f_name]
            out.write(f"#### frame: **{f_name}**\n")
            out.write(f"- **Frame ID:** {f['id']} | **Size:** {f['len']} Bytes\n")
            out.write("- **Nested Signals Matrix:**\n")
            out.write("  | Signal Variable Target | Bit Offset | Length |\n  | --- | --- | --- |\n")
            for s in f["signals"]:
                out.write(f"  | {s['name']} | {s['offset']} | {old_sig_meta.get(s['name'], 'N/A')} bits |\n")
            out.write("\n")

    # Changed Frames Check
    common_frames = sorted(list(set(old_frames.keys()) & set(new_frames.keys())))
    out.write("### 🔄 Changed Frames & Inner Signal Configurations\n\n")
    
    has_any_changed_frames = False
    for f_name in common_frames:
        o_f, n_f = old_frames[f_name], new_frames[f_name]
        
        # Track attribute changes
        f_changes = []
        if o_f["id"] != n_f["id"]:
            f_changes.append(f"| Frame ID | ~~{o_f['id']}~~ | **{n_f['id']}** |")
        if o_f["len"] != n_f["len"]:
            f_changes.append(f"| Length (Bytes) | ~~{o_f['len']}~~ | **{n_f['len']}** |")
        if o_f["pub"] != n_f["pub"]:
            f_changes.append(f"| Publisher Node | ~~{o_f['pub']}~~ | **{n_f['pub']}** |")
            
        # Analyze inner signals differences
        o_sigs = {s["name"]: s["offset"] for s in o_f["signals"]}
        n_sigs = {s["name"]: s["offset"] for s in n_f["signals"]}
        
        s_changes = []
        for s in sorted(list(set(n_sigs.keys()) - set(o_sigs.keys()))):
            s_changes.append(f"| {s} | **ADDED** | Start Bit Offset: {n_sigs[s]} \\| Width: {new_sig_meta.get(s, 'N/A')} bits |")
        for s in sorted(list(set(o_sigs.keys() - n_sigs.keys()))):
            s_changes.append(f"| {s} | *REMOVED* | Was at Offset: {o_sigs[s]} \\| Width: {old_sig_meta.get(s, 'N/A')} bits |")
        for s in sorted(list(set(o_sigs.keys() & n_sigs.keys()))):
            sub_mods = []
            if o_sigs[s] != n_sigs[s]:
                sub_mods.append(f"• Bit Offset: ~~{o_sigs[s]}~~ -> **{n_sigs[s]}**")
            if old_sig_meta.get(s) != new_sig_meta.get(s):
                sub_mods.append(f"• Bit Width: ~~{old_sig_meta.get(s)}~~ -> **{new_sig_meta.get(s)}**")
            if sub_mods:
                s_changes.append(f"| {s} | MODIFIED | {' '.join(sub_mods)} |")

        if f_changes or s_changes:
            has_any_changed_frames = True
            out.write(f"#### frame: **{f_name}**\n\n")
            if f_changes:
                out.write("##### Frame Attribute Changes:\n")
                out.write("| Property Name | Old Base Value | New Target Value |\n| --- | --- | --- |\n")
                for c in f_changes:
                    out.write(c + "\n")
                out.write("\n")
            if s_changes:
                out.write("##### Nested Signal Changes Inside This Frame:\n")
                out.write("| Nested Signal Target | Modification Status | Bit Details / Configuration Shifts |\n| --- | --- | --- |\n")
                for s in s_changes:
                    out.write(s + "\n")
                out.write("\n")

    if not has_any_changed_frames:
        out.write("No matching frame packing layouts or internal signal configurations modified.\n\n")

print("\n[SUCCESS] Custom RegEx Comparison Complete! Check 'ldf_diff_report.md' for nested blocks.")
