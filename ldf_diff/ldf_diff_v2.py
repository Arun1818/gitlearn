import os, sys, re, traceback

O_FILE, N_FILE, R_FILE, E_FILE = 'SFB_BMS2-5682.ldf', 'Upfitter-6x_LIN_20260722_v1.0.0 1.ldf', 'ldf_diff_report.html', 'ldf_diff_error_log.html'

print("Checking LDF targets...")
if not os.path.exists(O_FILE) or not os.path.exists(N_FILE):
    print("❌ EXECUTION FAILED: Base or Target LDF file missing in this directory.")
    sys.exit(1)

print("Compiling comparison assets...")
try:
    with open(O_FILE, 'r', encoding='utf-8', errors='ignore') as f: txt_o = f.read()
    with open(N_FILE, 'r', encoding='utf-8', errors='ignore') as f: txt_n = f.read()

    def parse_ldf(c):
        nds, frms, meta = [], {}, {}
        nm = re.search(r'Nodes\s*\{(.*?)\}', c, re.DOTALL)
        if nm:
            sm = re.search(r'Slaves\s*:\s*([^;]+);', nm.group(1))
            if sm: nds = [n.strip() for n in sm.group(1).split(',')]
        sb = re.search(r'Signals\s*\{(.*?)\}', c, re.DOTALL)
        if sb:
            for s, w in re.findall(r'(\w+)\s*:\s*(\d+)\s*,', sb.group(1)): meta[s] = w
        for fn, fid, fpb, fln, inn in re.findall(r'(\w+)\s*:\s*(\w+)\s*,\s*(\w+)\s*,\s*(\d+)\s*\{(.*?)\}', c, re.DOTALL):
            sgs = [{"name": s, "offset": int(o)} for s, o in re.findall(r'(\w+)\s*,\s*(\d+)\s*;', inn)]
            frms[fn] = {"id": fid, "pub": fpb, "len": fln, "signals": sorted(sgs, key=lambda x: x["offset"])}
        return nds, frms, meta

    old_n, old_f, old_m = parse_ldf(txt_o)
    new_n, new_f, new_m = parse_ldf(txt_n)

    out = open(R_FILE, "w", encoding="utf-8")
    out.write("<!DOCTYPE html><html><head><style>body{font-family:sans-serif;margin:30px;background:#f6f8fa;} .box{max-width:1000px;margin:0 auto;background:#fff;padding:30px;border:1px solid #d0d7de;border-radius:8px;} .card{background:#f8f9fa;border:1px solid #e1e4e8;border-radius:6px;padding:15px;margin-bottom:15px;} table{width:100%;border-collapse:collapse;margin:8px 0;font-size:13px;} th,td{padding:8px;border:1px solid #d0d7de;} th{background:#eaeef2;} .bg-a{background:#dafbe1;color:#1a7f37;} .bg-r{background:#ffebe9;color:#cf222e;}</style></head><body><div class='box'><h2>LDF Change Report</h2>")
    out.write(f"<p><b>OLD:</b> {O_FILE}<br><b>NEW:</b> {N_FILE}</p><h3>1. Nodes Architecture</h3><ul>")
    
    for n in sorted(list(set(new_n) - set(old_n))): out.write(f"<li class='bg-a'>[+] Added Node: {n}</li>")
    for n in sorted(list(set(old_n) - set(new_n))): out.write(f"<li class='bg-r'>[-] Removed Node: {n}</li>")
    out.write("</ul><h3>2. Frame Architecture & Nested Signals Matrix</h3>")

    for fn in sorted(list(set(new_f.keys()) - set(old_f.keys()))):
        f = new_f[fn]
        out.write(f"<div class='card bg-a'><b>ADDED FRAME:</b> {fn} (ID: {f['id']}, Size: {f['len']}B)<table>")
        for s in f["signals"]: out.write(f"<tr><td>{s['name']}</td><td>Offset: {s['offset']}</td><td>{new_m.get(s['name'],'N/A')} bits</td></tr>")
        out.write("</table></div>")

    for fn in sorted(list(set(old_f.keys()) - set(new_f.keys()))):
        f = old_f[fn]
        out.write(f"<div class='card bg-r'><b>REMOVED FRAME:</b> {fn} (ID: {f['id']})<table>")
        for s in f["signals"]: out.write(f"<tr><td>{s['name']}</td><td>Offset: {s['offset']}</td><td>{old_m.get(s['name'],'N/A')} bits</td></tr>")
        out.write("</table></div>")

    for fn in sorted(list(set(old_f.keys()) & set(new_f.keys()))):
        of, nf = old_f[fn], new_f[fn]
        fc, sc = [], []
        if of["id"] != nf["id"]: fc.append(f"<tr><th>ID</th><td>{of['id']}</td><td>{nf['id']}</td></tr>")
        if of["len"] != nf["len"]: fc.append(f"<tr><th>Length</th><td>{of['len']}B</td><td>{nf['len']}B</td></tr>")
        
        osgs = {s["name"]: s["offset"] for s in of["signals"]}
        nsgs = {s["name"]: s["offset"] for s in nf["signals"]}
        
        for s in sorted(list(set(nsgs.keys()) - set(osgs.keys()))): sc.append(f"<tr class='bg-a'><td>{s}</td><td>ADDED</td><td>Offset: {nsgs[s]} | Width: {new_m.get(s,'N/A')}b</td></tr>")
        for s in sorted(list(set(osgs.keys() - nsgs.keys()))): sc.append(f"<tr class='bg-r'><td>{s}</td><td>REMOVED</td><td>Was: {osgs[s]} | Width: {old_m.get(s,'N/A')}b</td></tr>")
        for s in sorted(list(set(osgs.keys() & nsgs.keys()))):
            sm = []
            if osgs[s] != nsgs[s]: sm.append(f"Offset: {osgs[s]} &rarr; {nsgs[s]}")
            if old_m.get(s) != new_m.get(s): sm.append(f"Width: {old_m.get(s)}b &rarr; {new_m.get(s)}b")
            if sm: sc.append(f"<tr><td>{s}</td><td>MODIFIED</td><td>{' | '.join(sm)}</td></tr>")

        if fc or sc:
            out.write(f"<div class='card' style='border-left:4px solid #0969da;'><b>CHANGED FRAME: {fn}</b>")
            if fc: out.write(f"<table><tr><th>Field</th><th>Old</th><th>New</th></tr>{''.join(fc)}</table>")
            if sc: out.write(f"<table><tr style='background:#eaeef2;'><th>Signal Name</th><th>Status</th><th>Configuration Details</th></tr>{''.join(sc)}</table>")
            out.write("</div>")

    out.write("</div></body></html>")
    out.close()

    print("\n" + "="*80)
    print(" ✅ EXECUTION DONE: Report is generated successfully!")
    print(f" -> Please open: {R_FILE}")
    print("="*80 + "\n")

except Exception as e:
    with open(E_FILE, "w", encoding="utf-8") as ef:
        ef.write(f"<html><body><h2>❌ Crash Report Traceback</h2><pre>")
        traceback.print_exc(file=ef)
        ef.write("</pre></body></html>")
    print("\n" + "!"*80)
    print(" ❌ EXECUTION FAILED: An unexpected error occurred during processing.")
    print(f" -> Detailed traceback log saved to: {E_FILE}")
    print("!"*80 + "\n")
    sys.exit(1)
