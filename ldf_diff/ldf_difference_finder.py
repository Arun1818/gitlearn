import os, sys, re, argparse

# 1. COMMAND LINE ARGUMENTS INTERFACE
parser = argparse.ArgumentParser(description="Automotive LDF Comparison Tool")
parser.add_argument("-old", required=True, help="Path to old base LDF file")
parser.add_argument("-new", required=True, help="Path to new target LDF file")
parser.add_argument("-o", "--output", default="ldf_diff_report.html")
args = parser.parse_args()

OLD_FILE, NEW_FILE, OUTPUT_REPORT = args.old, args.new, args.output

print("Checking LDF targets...")
if not os.path.exists(OLD_FILE) or not os.path.exists(NEW_FILE):
    print("❌ EXECUTION FAILED: Base or Target LDF file missing in this directory."); sys.exit(1)

print("Compiling comparison assets...")

# 2. RAW TEXT SEGMENT EXTRACTION ENGINE
with open(OLD_FILE, 'r', encoding='utf-8', errors='ignore') as f: txt_o = f.read()
with open(NEW_FILE, 'r', encoding='utf-8', errors='ignore') as f: txt_n = f.read()

def parse_ldf(c_str):
    nds, frms, meta = [], {}, {}
    nm = re.search(r'Nodes\s*\{(.*?)\}', c_str, re.DOTALL)
    if nm:
        sm = re.search(r'Slaves\s*:\s*([^;]+);', nm.group(1))
        if sm: nds = [n.strip() for n in sm.group(1).split(',')]
    sb = re.search(r'Signals\s*\{(.*?)\}', c_str, re.DOTALL)
    if sb:
        for s, w in re.findall(r'(\w+)\s*:\s*(\d+)\s*,', sb.group(1)): meta[s] = w
    for fn, fid, fpb, fln, inn in re.findall(r'(\w+)\s*:\s*(\w+)\s*,\s*(\w+)\s*,\s*(\d+)\s*\{(.*?)\}', c_str, re.DOTALL):
        sgs = [{"name": s, "offset": int(o)} for s, o in re.findall(r'(\w+)\s*,\s*(\d+)\s*;', inn)]
        frms[fn] = {"id": fid, "pub": fpb, "len": fln, "signals": sorted(sgs, key=lambda x: x["offset"])}
    return nds, frms, meta

old_nodes, old_frames, old_sig_meta = parse_ldf(txt_o)
new_nodes, new_frames, new_sig_meta = parse_ldf(txt_n)

# 3. COMPACT GENERATION ENGINE (0% Indentation / Clipboard Risk)
with open(OUTPUT_REPORT, "w", encoding="utf-8") as out:
    out.write("<!DOCTYPE html><html><head><title>LDF Report</title><style>body{font-family:sans-serif;margin:30px;background:#f6f8fa;} .box{max-width:1100px;margin:0 auto;background:#fff;padding:40px;border:1px solid #d0d7de;border-radius:8px;} .card{background:#f8f9fa;border:1px solid #e1e4e8;border-radius:6px;padding:15px;margin-bottom:15px;} table{width:100%;border-collapse:collapse;margin-top:8px;font-size:13px;} th,td{padding:8px 12px;border:1px solid #d0d7de;text-align:left;} th{background:#eaeef2;width:25%;} .bg-a{background:#dafbe1;color:#1a7f37;border-left:4px solid #2da44e;} .bg-r{background:#ffebe9;color:#cf222e;border-left:4px solid #cf222e;} .empty{color:#6e7781;font-style:italic;padding:10px;}</style></head><body><div class='box'><h1>LIN Description File (LDF) Matrix Change Report</h1>")
    out.write(f"<div style='font-family:monospace;font-size:13px;'><b>OLD BASE LDF:</b> {OLD_FILE}<br><b>NEW TARGET LDF:</b> {NEW_FILE}</div><h2>1. Network Node Updates</h2>")
    
    added_nodes = sorted(list(set(new_nodes) - set(old_nodes)))
    removed_nodes = sorted(list(set(old_nodes) - set(new_nodes)))
    if not added_nodes and not removed_nodes:
        out.write("<div class='empty'>No changes found in network cluster architecture nodes.</div>")
    else:
        out.write("<ul>")
        for n in added_nodes: out.write(f"<li class='bg-a'>[+] Added Slave Node: <strong>{n}</strong></li>")
        for n in removed_nodes: out.write(f"<li class='bg-r'>[-] Removed Slave Node: <strong>{n}</strong></li>")
        out.write("</ul>")

    out.write("<h2>2. Message & Frame Architecture (With Nested Layout Signal Maps)</h2>")
    added_frames = sorted(list(set(new_frames.keys()) - set(old_frames.keys())))
    if added_frames:
        out.write("<h3>Added Frames</h3>")
        for f_name in added_frames:
            f = new_frames[f_name]
            out.write(f"<div class='card' style='border-left:4px solid #2da44e;'><div style='font-weight:bold;'>ADDED FRAME: {f_name}</div><table><tr><th>Frame ID</th><td>{f['id']}</td></tr><tr><th>Length (Bytes)</th><td>{f['len']}</td></tr><tr><th>Publisher</th><td>{f['pub']}</td></tr></table><table style='margin-top:10px;'><tr style='background:#f6f8fa;'><th>Signal Name</th><th>Bit Start Offset</th><th>Bit Length</th></tr>")
            for s in f["signals"]: out.write(f"<tr><td><b>{s['name']}</b></td><td>{s['offset']}</td><td>{new_sig_meta.get(s['name'], 'N/A')} bits</td></tr>")
            out.write("</table></div>")

    removed_frames = sorted(list(set(old_frames.keys()) - set(new_frames.keys())))
    if removed_frames:
        out.write("<h3>Removed Frames</h3>")
        for f_name in removed_frames:
            f = old_frames[f_name]
            out.write(f"<div class='card' style='border-left:4px solid #cf222e;'><div style='font-weight:bold;'>REMOVED FRAME: {f_name}</div><table><tr><th>Frame ID</th><td>{f['id']}</td></tr><tr><th>Length</th><td>{f['len']}</td></tr></table><table style='margin-top:10px;'><tr style='background:#f6f8fa;'><th>Signal Name</th><th>Bit Start Offset</th><th>Bit Length</th></tr>")
            for s in f["signals"]: out.write(f"<tr><td><b>{s['name']}</b></td><td>{s['offset']}</td><td>{old_sig_meta.get(s['name'], 'N/A')} bits</td></tr>")
            out.write("</table></div>")

    out.write("<h3>Changed Frames & Inner Signal Configurations</h3>")
    has_any_changes = False
    for f_name in sorted(list(set(old_frames.keys()) & set(new_frames.keys()))):
        o_f, n_f = old_frames[f_name], new_frames[f_name]
        f_changes, s_changes = [], []
        if o_f["id"] != n_f["id"]: f_changes.append(f"<tr><td><b>Frame ID</b></td><td style='color:#cf222e;text-decoration:line-through;'>{o_f['id']}</td><td style='color:#1a7f37;font-weight:bold;'>{n_f['id']}</td></tr>")
        if o_f["len"] != n_f["len"]: f_changes.append(f"<tr><td><b>Length (Bytes)</b></td><td style='color:#cf222e;text-decoration:line-through;'>{o_f['len']}</td><td style='color:#1a7f37;font-weight:bold;'>{n_f['len']}</td></tr>")
        if o_f["pub"] != n_f["pub"]: f_changes.append(f"<tr><td><b>Publisher</b></td><td style='color:#cf222e;text-decoration:line-through;'>{o_f['pub']}</td><td style='color:#1a7f37;font-weight:bold;'>{n_f['pub']}</td></tr>")
        
        o_sigs = {s["name"]: s["offset"] for s in o_f["signals"]}
        n_sigs = {s["name"]: s["offset"] for s in n_f["signals"]}
        for s in sorted(list(set(n_sigs.keys()) - set(o_sigs.keys()))): s_changes.append(f"<tr class='bg-a'><td><b>{s}</b></td><td>ADDED</td><td>Start Bit Offset: {n_sigs[s]} | Width: {new_sig_meta.get(s, 'N/A')} bits</td></tr>")
        for s in sorted(list(set(o_sigs.keys() - n_sigs.keys()))): s_changes.append(f"<tr class='bg-r'><td><b>{s}</b></td><td>REMOVED</td><td>Was at Offset: {o_sigs[s]} | Width: {old_sig_meta.get(s, 'N/A')} bits</td></tr>")
        for s in sorted(list(set(o_sigs.keys() & n_sigs.keys()))):
            sub_mods = []
            if o_sigs[s] != n_sigs[s]: sub_mods.append(f"<div>• Bit Offset: ~~{o_sigs[s]}~~ &rarr; <b>{n_sigs[s]}</b></div>")
            if old_sig_meta.get(s) != new_sig_meta.get(s): sub_mods.append(f"<div>• Bit Width: ~~{old_sig_meta.get(s)}~~ &rarr; <b>{new_sig_meta.get(s)}</b></div>")
            if sub_mods: s_changes.append(f"<tr><td><b>{s}</b></td><td style='color:#953800;font-weight:bold;'>MODIFIED</td><td>{''.join(sub_mods)}</td></tr>")

        if f_changes or s_changes:
            has_any_changes = True
            out.write(f"<div class='card' style='border-left:4px solid #0969da;'><div style='color:#953800;font-weight:bold;'>CHANGED FRAME: {f_name}</div>")
            if f_changes: out.write(f"<table><thead><tr style='background:#eaeef2;'><th>Property</th><th>Old</th><th>New</th></tr></thead><tbody>{''.join(f_changes)}</tbody></table>")
            if s_changes: out.write(f"<div style='font-size:12px;font-weight:600;color:#57606a;margin-top:10px;'>Inner Signal Modifications:</div><table><thead><tr style='background:#eaeef2;'><th>Signal Target</th><th>Status</th><th>Changes</th></tr></thead><tbody>{''.join(s_changes)}</tbody></table>")
            out.write("</div>")

    if not has_any_changes: out.write("<div class='empty'>No matching frame layouts or nested signals modified.</div>")
    out.write("</div></body></html>")

print("\n" + "=" * 80)
print(" ✅ EXECUTION DONE: Report is generated successfully!")
print(f" -> Please open: {OUTPUT_REPORT}")
print("=" * 80 + "\n")
