import os, sys, re, argparse

# ==============================================================================
# 1. COMMAND LINE ARGUMENTS INTERFACE
# ==============================================================================
parser = argparse.ArgumentParser(description="Automotive LIN LDF Scaling Comparison Tool")
parser.add_argument("-old", required=True)
parser.add_argument("-new", required=True)
parser.add_argument("-o", "--output", default="ldf_diff_report.html")
args = parser.parse_args()

OLD_FILE, NEW_FILE, OUTPUT_REPORT = args.old, args.new, args.output
EXCEL_REPORT = "ldf_diff_summary.xls"  # Beautiful, Excel-Compatible Tabular Workbook

print("Checking LDF targets...")
if not os.path.exists(OLD_FILE) or not os.path.exists(NEW_FILE):
    print("❌ EXECUTION FAILED: Input LDF files missing."); sys.exit(1)

print("Processing automotive network matrices...")
with open(OLD_FILE, 'r', encoding='utf-8', errors='ignore') as f: txt_o = f.read()
with open(NEW_FILE, 'r', encoding='utf-8', errors='ignore') as f: txt_n = f.read()

def parse_ldf_advanced(c_str):
    nds, frms, meta, scheds, diags = [], {}, {}, {}, {}
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
    for d_name, d_id in re.findall(r'(MasterReq|SlaveResp)\s*:\s*(\w+)', c_str): diags[d_name] = d_id
    st_block = re.search(r'Schedule_tables\s*\{(.*?)\}\s*(?=\w+\s*\{|\Z)', c_str, re.DOTALL)
    if st_block:
        for st_name, st_inner in re.findall(r'(\w+)\s*\{(.*?)\}', st_block.group(1), re.DOTALL):
            items = []
            for cmd, delay in re.findall(r'(\w+)\s+delay\s+([\d\.]+)\s*ms\s*;', st_inner): items.append(f"{cmd}({delay}ms)")
            scheds[st_name] = " -> ".join(items)
    return nds, frms, meta, diags, scheds

old_n, old_f, old_m, old_d, old_s = parse_ldf_advanced(txt_o)
new_n, new_f, new_m, new_d, new_s = parse_ldf_advanced(txt_n)

# ==============================================================================
# 2. WRITE INTERACTIVE HTML VIEW REPORT
# ==============================================================================
out = open(OUTPUT_REPORT, "w", encoding="utf-8")
out.write("<!DOCTYPE html><html><head><title>LIN Report</title><style>body{font-family:sans-serif;margin:30px;background:#f6f8fa;} .box{max-width:1100px;margin:0 auto;background:#fff;padding:40px;border:1px solid #d0d7de;border-radius:8px;} .card{background:#f8f9fa;border:1px solid #e1e4e8;border-radius:6px;padding:15px;margin-bottom:15px;} table{width:100%;border-collapse:collapse;margin-top:8px;font-size:13px;} th,td{padding:8px 12px;border:1px solid #d0d7de;text-align:left;} th{background:#eaeef2;width:25%;} .bg-a{background:#dafbe1;color:#1a7f37;border-left:4px solid #2da44e;} .bg-r{background:#ffebe9;color:#cf222e;border-left:4px solid #cf222e;} .empty{color:#6e7781;font-style:italic;padding:10px;}</style></head><body><div class='box'><h1>LIN Matrix Change Report</h1>")
out.write(f"<div style='font-family:monospace;font-size:13px;'><b>OLD BASE LDF:</b> {OLD_FILE}<br><b>NEW TARGET LDF:</b> {NEW_FILE}</div><h2>1. Network Node Updates</h2><ul>")
a_nodes, r_nodes = sorted(list(set(new_n) - set(old_n))), sorted(list(set(old_n) - set(new_n)))
for n in a_nodes: out.write(f"<li class='bg-a'>[+] Added Slave Node: <b>{n}</b></li>")
for n in r_nodes: out.write(f"<li class='bg-r'>[-] Removed Slave Node: <b>{n}</b></li>")
if not a_nodes and not r_nodes: out.write("<div class='empty'>No node architecture modifications.</div>")
out.write("</ul><h2>2. Diagnostic Frame Identifier Handling</h2>")
if old_d != new_d or new_d:
    out.write("<div class='card'><table><tr style='background:#f6f8fa;'><th>Diagnostic Name</th><th>Base ID</th><th>Target ID</th></tr>")
    for d in sorted(list(set(old_d.keys() | new_d.keys()))): out.write(f"<tr><td><b>{d}</b></td><td>{old_d.get(d, 'N/A')}</td><td>{new_d.get(d, 'N/A')}</td></tr>")
    out.write("</table></div>")
else: out.write("<div class='empty'>No active diagnostics mappings detected.</div>")
out.write("<h2>3. Message Frame Architecture & Packed Signals Layout Map</h2>")
for fn in sorted(list(set(new_f.keys()) - set(old_f.keys()))):
    f = new_f[fn]
    out.write(f"<div class='card bg-a'><b>ADDED FRAME: {fn}</b> (ID: {f['id']}, Size: {f['len']} Bytes)<table>")
    for s in f["signals"]: out.write(f"<tr><td>{s['name']}</td><td>{s['offset']}</td><td>{new_m.get(s['name'], 'N/A')} bits</td></tr>")
    out.write("</table></div>")
for fn in sorted(list(set(old_f.keys()) - set(new_f.keys()))):
    f = old_f[fn]
    out.write(f"<div class='card bg-r'><b>REMOVED FRAME: {fn}</b> (ID: {f['id']})<table>")
    for s in f["signals"]: out.write(f"<tr><td>{s['name']}</td><td>{s['offset']}</td><td>{old_m.get(s['name'], 'N/A')} bits</td></tr>")
    out.write("</table></div>")
for fn in sorted(list(set(old_f.keys()) & set(new_f.keys()))):
    o_f, n_f = old_f[fn], new_f[fn]
    f_chg, s_chg = [], []
    if o_f["id"] != n_f["id"]: f_chg.append(f"<tr><td><b>Frame ID</b></td><td>~~{o_f['id']}~~</td><td><b>{n_f['id']}</b></td></tr>")
    if o_f["len"] != n_f["len"]: f_chg.append(f"<tr><td><b>Length</b></td><td>~~{o_f['len']}~~</td><td><b>{n_f['len']}</b></td></tr>")
    osgs, nsgs = {s["name"]: s["offset"] for s in o_f["signals"]}, {s["name"]: s["offset"] for s in n_f["signals"]}
    for s in sorted(list(set(nsgs.keys()) - set(osgs.keys()))): s_chg.append(f"<tr class='bg-a'><td><b>{s}</b></td><td>ADDED</td><td>Bit Offset: {nsgs[s]} | Width: {new_m.get(s, 'N/A')}b</td></tr>")
    for s in sorted(list(set(osgs.keys() - nsgs.keys()))): s_chg.append(f"<tr class='bg-r'><td><b>{s}</b></td><td>REMOVED</td><td>Was: {osgs[s]} | Width: {old_m.get(s, 'N/A')}b</td></tr>")
    for s in sorted(list(set(osgs.keys() & nsgs.keys()))):
        sm = []
        if osgs[s] != nsgs[s]: sm.append(f"Offset: ~~{osgs[s]}~~ &rarr; <b>{nsgs[s]}</b>")
        if old_m.get(s) != new_m.get(s): sm.append(f"Width: ~~{old_m.get(s)}~~ &rarr; <b>{new_m.get(s)}</b>b")
        if sm: s_chg.append(f"<tr><td><b>{s}</b></td><td style='color:#953800;font-weight:bold;'>MODIFIED</td><td>{' | '.join(sm)}</td></tr>")
    if f_chg or s_chg:
        out.write(f"<div class='card' style='border-left:4px solid #0969da;'><b>CHANGED FRAME: {fn}</b>")
        if f_chg: out.write(f"<table>{''.join(f_chg)}</table>")
        if s_chg: out.write(f"<table>{''.join(s_chg)}</table>")
        out.write("</div>")
out.write("<h2>4. LIN Schedule Table Sequencing Delays Map</h2>")
a_sched, r_sched, c_sched = sorted(list(set(new_s.keys()) - set(old_s.keys()))), sorted(list(set(old_s.keys()) - set(new_s.keys()))), sorted(list(set(old_s.keys()) & set(new_s.keys())))
for sn in a_sched: out.write(f"<div class='card bg-a'><b>[+] Added Schedule: {sn}</b><br>{new_s[sn]}</div>")
for sn in r_sched: out.write(f"<div class='card bg-r'><b>[-] Removed Schedule: {sn}</b><br>{old_s[sn]}</div>")
for sn in c_sched:
    if old_s[sn] != new_s[sn]: out.write(f"<div class='card' style='border-left:4px solid #e1a41e;'><b>[~] Modified Schedule Delay: {sn}</b><br><small style='color:red;'>Old: {old_s[sn]}</small><br><small style='color:green;font-weight:bold;'>New: {new_s[sn]}</small></div>")
out.write("</div></body></html>")
out.close()

# ==============================================================================
# 3. WRITE EYE-CATCHING STYLIZED EXCEL TABULAR WORKBOOK
# ==============================================================================
xls = open(EXCEL_REPORT, "w", encoding="utf-8")
xls.write("<html><head><meta charset='UTF-8'><style>\n")
xls.write("table{border-collapse:collapse; font-family:'Segoe UI',sans-serif; font-size:13px;}\n")
xls.write("th,td{border:1px solid #d0d7de; padding:6px 12px; text-align:left;}\n")
xls.write("th{background-color:#24292E; color:#ffffff; font-weight:bold;}\n")
xls.write(".bg-even{background-color:#F6F8FA;}\n")
xls.write(".bdg-add{background-color:#DAFBE1; color:#1A7F37; font-weight:bold; text-align:center;}\n")
xls.write(".bdg-rem{background-color:#FFEBE9; color:#CF222E; font-weight:bold; text-align:center;}\n")
xls.write(".bdg-mod{background-color:#FFF8E7; color:#953800; font-weight:bold; text-align:center;}\n")
xls.write("</style></head><body>\n")
xls.write("<table><thead><tr><th>CATEGORY</th><th>ELEMENT TARGET</th><th>EVENT STATUS</th><th>CHANGELOG CONFIGURATION DETAILS</th></tr></thead><tbody>\n")

r_idx = 0
def app_r(c, n, st, d):
    global r_idx
    r_idx += 1
    row_cls = " class='bg-even'" if r_idx % 2 == 0 else ""
    bdg_cls = "bdg-add" if "ADD" in st else ("bdg-rem" if "REM" in st else "bdg-mod")
    xls.write(f"<tr{row_cls}><td>{c}</td><td><b>{n}</b></td><td class='{bdg_cls}'>{st}</td><td>{d}</td></tr>\n")

# Populating Rows Data Maps
for n in sorted(list(set(new_n) - set(old_n))): app_r("Node", n, "ADDED", "Slave node mapped to network cluster architecture definitions.")
for n in sorted(list(set(old_n) - set(new_n))): app_r("Node", n, "REMOVED", "Slave node dropped from cluster topology specifications.")
for fn in sorted(list(set(new_f.keys()) - set(old_f.keys()))): app_r("Frame", fn, "ADDED", f"ID: {new_f[fn]['id']} | Payload Length: {new_f[fn]['len']} Bytes")
for fn in sorted(list(set(old_f.keys()) - set(new_f.keys()))): app_r("Frame", fn, "REMOVED", "Frame baseline identifier dropped from data layout matrix.")
