#!/usr/bin/env python3
import datetime, json, os, click, cantools

MESSAGE_PROPERTIES = {"frame_id": "hex", "is_extended_frame": "basic", "is_fd": "basic", "length": "basic", "senders": "list"}
SIGNAL_PROPERTIES = {"start": "basic", "length": "basic", "byte_order": "basic", "is_signed": "basic", "initial": "str", "scale": "basic", "offset": "basic", "receivers": "list", "choices": "dict"}

def is_node_transmitter(message, node_name="UCIM_UCIM2"):
    return message and message.senders and any(node_name == str(s) for s in message.senders)

def is_signal_relevant(signal, message, node_name="UCIM_UCIM2"):
    if is_node_transmitter(message, node_name): return True
    return signal and signal.receivers and any(node_name == str(r) for r in signal.receivers)

def detect_e2e_signals(signals_dict):
    e2e_groups = {}
    for name in signals_dict.keys():
        # Match standard E2E component layouts
        if any(x in name for x in ["_No_Crc", "_No_Cnt", "CrcOffset"]):
            # Split off trailing component names to identify the unified base prefix name
            parts = name.split("_No_") if "_No_" in name else name.split("Crc")
            base_prefix = parts[0] if parts and parts[0] else name
            e2e_groups.setdefault(base_prefix, []).append(name)
    return e2e_groups

def converter(value, from_type):
    if value is None: return None
    if from_type == "hex": return f"{hex(value)}"
    if from_type == "str": return str(value)
    if from_type == "dict": return {int(k): str(v) for k, v in value.items()}
    if from_type == "list": return ",".join(sorted(value))
    return value

def compare_dictionaries(old: dict, new: dict):
    old_set, new_set = set(old.keys()), set(new.keys())
    return sorted(new_set - old_set), sorted(old_set & new_set), sorted(old_set - new_set)

def get_all_attributes(item):
    if hasattr(item, "dbc") and item.dbc and isinstance(item.dbc, dict) and "attributes" in item.dbc:
        return {k: str(v) for k, v in item.dbc["attributes"].items()}
    return {}

def compare_properties(old_obj, new_obj, properties_dict):
    changes = []
    for name, from_type in properties_dict.items():
        old_val = converter(getattr(old_obj, name, None), from_type)
        new_val = converter(getattr(new_obj, name, None), from_type)
        if old_val != new_val: changes.append({"property": name, "old": old_val, "new": new_val})
    return changes

def compare_attributes(old_obj, new_obj):
    changes = []
    old_attrs, new_attrs = get_all_attributes(old_obj), get_all_attributes(new_obj)
    added, same, deleted = compare_dictionaries(old_attrs, new_attrs)
    for k in added: changes.append({"attribute": k, "old": None, "new": new_attrs[k]})
    for k in deleted: changes.append({"attribute": k, "old": old_attrs[k], "new": None})
    for k in same:
        if old_attrs[k] != new_attrs[k]: changes.append({"attribute": k, "old": old_attrs[k], "new": new_attrs[k]})
    return changes

def compare_messages(old_msg, new_msg, node_name="UCIM_UCIM2"):
    msg_changes = []
    if is_node_transmitter(old_msg, node_name) or is_node_transmitter(new_msg, node_name):
        msg_changes = compare_properties(old_msg, new_msg, MESSAGE_PROPERTIES) + compare_attributes(old_msg, new_msg)

    sig_report = {}
    old_sigs, new_sigs = {s.name: s for s in old_msg.signals}, {s.name: s for s in new_msg.signals}
    added, same, deleted = compare_dictionaries(old_sigs, new_sigs)
    old_e2e, new_e2e = detect_e2e_signals(old_sigs), detect_e2e_signals(new_sigs)
    
    # Process systematic deletion of E2E group frameworks
    for prefix, sigs in list(old_e2e.items()):
        if prefix not in new_e2e and all(s in deleted for s in sigs):
            if any(is_signal_relevant(old_sigs[s], old_msg, node_name) for s in sigs):
                sig_report[f"E2E_GROUP_REMOVED: {prefix}"] = {
                    "action": "architectural_removal", 
                    "details": f"Systematic removal of End-to-End protection framework layer ({', '.join(sigs)})"
                }
            # 🚀 FIX: We NO LONGER call deleted.remove(s) here. 
            # Leaving them in 'deleted' ensures they generate standard parameter comparison tables!

    # Process systematic additions of E2E group frameworks
    for prefix, sigs in list(new_e2e.items()):
        if prefix not in old_e2e and all(s in added for s in sigs):
            if any(is_signal_relevant(new_sigs[s], new_msg, node_name) for s in sigs):
                sig_report[f"E2E_GROUP_ADDED: {prefix}"] = {
                    "action": "architectural_addition", 
                    "details": f"Systematic addition of End-to-End protection framework layer ({', '.join(sigs)})"
                }
            # Leaving them in 'added' ensures they get full parameter tables too

    for name in added:
        sig = new_sigs[name]
        if is_signal_relevant(sig, new_msg, node_name):
            props = [{"property": p, "old": None, "new": converter(getattr(sig, p, None), t)} for p, t in SIGNAL_PROPERTIES.items()]
            sig_report[name] = {"action": "added", "changes": props + compare_attributes(None, sig)}

    for name in deleted:
        sig = old_sigs[name]
        if is_signal_relevant(sig, old_msg, node_name):
            props = [{"property": p, "old": converter(getattr(sig, p, None), t), "new": None} for p, t in SIGNAL_PROPERTIES.items()]
            sig_report[name] = {"action": "deleted", "changes": props + compare_attributes(sig, None)}

    for name in same:
        s_old, s_new = old_sigs[name], new_sigs[name]
        if is_signal_relevant(s_old, old_msg, node_name) or is_signal_relevant(s_new, new_msg, node_name):
            diffs = compare_properties(s_old, s_new, SIGNAL_PROPERTIES) + compare_attributes(s_old, s_new)
            filtered = []
            for d in diffs:
                if d.get("property") == "receivers":
                    if (node_name in (d.get("old") or "")) != (node_name in (d.get("new") or "")): filtered.append(d)
                else: filtered.append(d)
            if filtered: sig_report[name] = {"action": "changed", "changes": filtered}

    return msg_changes, sig_report

def compare_node_global_properties(old_dbc, new_dbc, node_name="UCIM_UCIM2"):
    old_node = next((n for n in old_dbc.nodes if n.name == node_name), None) if hasattr(old_dbc, 'nodes') else None
    new_node = next((n for n in new_dbc.nodes if n.name == node_name), None) if hasattr(new_dbc, 'nodes') else None
    if old_node and new_node: return compare_attributes(old_node, new_node)
    if old_node and not new_node: return [{"property": "Node Status", "old": "Present", "new": "Deleted"}]
    if not old_node and new_node: return [{"property": "Node Status", "old": "Absent", "new": "Added"}]
    return []

def compare_dbc(old_path, new_path, node_name="UCIM_UCIM2"):
    old_dbc = cantools.database.load_file(old_path, strict=False) if old_path else None
    new_dbc = cantools.database.load_file(new_path, strict=False) if new_path else None
    report = {"node_global_changes": compare_node_global_properties(old_dbc, new_dbc, node_name) if old_dbc and new_dbc else [], "messages": {}}
    
    old_msgs = {m.name: m for m in old_dbc.messages} if old_dbc else {}
    new_msgs = {m.name: m for m in new_dbc.messages} if new_dbc else {}
    added, same, deleted = compare_dictionaries(old_msgs, new_msgs)

    # Process modified or persistent message content layers
    for name in same:
        msg_diff, sig_diff = compare_messages(old_msgs[name], new_msgs[name], node_name)
        if msg_diff or sig_diff: 
            report["messages"][name] = {"status": "changed", "message_level_changes": msg_diff, "signal_level_changes": sig_diff}
            
    # Process dropped frames completely
    for name in deleted:
        if is_node_transmitter(old_msgs[name], node_name): 
            report["messages"][name] = {"status": "deleted", "details": "Message removed from network architecture."}
            
    # Process newly introduced frames completely
    for name in added:
        if is_node_transmitter(new_msgs[name], node_name): 
            report["messages"][name] = {"status": "added", "details": "Message introduced to network architecture."}
            
    return report

def save_html_report(report_data, file_path, node_name, old_file, new_file):
    global_html = "<table><tr><th>Attribute</th><th>Old</th><th>New</th></tr>" + "".join(f"<tr><td><strong>{c.get('property') or c.get('attribute', 'Unknown')}</strong></td><td class='old-val'>{c.get('old')}</td><td class='new-val'>{c.get('new')}</td></tr>" for c in report_data["node_global_changes"]) + "</table>" if report_data.get("node_global_changes") else "<p class='no-changes'>No global node properties changed.</p>"
    msg_html, has_rel = "", False
    
    if report_data.get("messages"):
        for m_name, m_data in report_data["messages"].items():
            if m_data["status"] == "changed" and not m_data.get("message_level_changes") and not m_data.get("signal_level_changes"): continue
            has_rel = True
            msg_html += f"<div class='card'><h3><span class='badge badge-{m_data['status']}'>{m_data['status'].upper()}</span> Message: {m_name}</h3>"
            if "details" in m_data: msg_html += f"<p><em>{m_data['details']}</em></p>"
            if m_data.get("message_level_changes"):
                msg_html += "<h4>Message Header Changes</h4><table><tr><th>Property</th><th>Old</th><th>New</th></tr>" + "".join(f"<tr><td>{c.get('property') or c.get('attribute', 'Unknown')}</td><td class='old-val'>{c.get('old')}</td><td class='new-val'>{c.get('new')}</td></tr>" for c in m_data["message_level_changes"]) + "</table>"
            if m_data.get("signal_level_changes"):
                msg_html += "<h4>Layout Changes</h4>"
                
                # FIRST: Print unified E2E alerts at the top
                for s_name, s_data in m_data["signal_level_changes"].items():
                    action = s_data.get("action", "modified")
                    if action in ["architectural_removal", "architectural_addition"]:
                        msg_html += f"""
                        <div class='alert alert-e2e' style='background-color: #fef2f2; border: 1px solid #fca5a5; color: #991b1b; padding: 15px; border-radius: 6px; margin: 10px 0;'>
                            <strong>❌ E2E Signal Group Removed:</strong> <span style='font-family: monospace; font-size: 15px;'>{s_name}</span>
                            <br><span style='font-size: 13px; color: #7f1d1d; margin-top: 5px; display: inline-block;'>{s_data['details']}</span>
                        </div>
                        """
                
                # SECOND: Print data signals based on your precise data requirements
                for s_name, s_data in m_data["signal_level_changes"].items():
                    action = s_data.get("action", "modified")
                    if action in ["architectural_removal", "architectural_addition"]: 
                        continue
                        
                    msg_html += f"<div class='sig-block' style='margin-top: 15px;'>"
                    msg_html += f"<h5>Signal: {s_name} <span class='badge badge-{action}'>{action}</span></h5>"
                    
                    # RULE 1: Purely deleted signals get no details table
                    if action == "deleted":
                        msg_html += "</div>"
                        continue
                        
                    if s_data.get("changes"):
                        # RULE 3: Purely added signals get a 2-column table (Param and New only)
                        if action == "added":
                            msg_html += "<table><tr><th>Param</th><th>New Configuration Value</th></tr>"
                            for chg in s_data["changes"]:
                                p = chg.get("property") or chg.get("attribute", "Unknown")
                                msg_html += f"<tr><td>{p}</td><td class='new-val'>{chg.get('new')}</td></tr>"
                            msg_html += "</table>"
                        
                        # RULE 2: Modified/Changed signals keep the full side-by-side layout
                        else:
                            msg_html += "<table><tr><th>Param</th><th>Old</th><th>New</th></tr>"
                            for chg in s_data["changes"]:
                                p = chg.get("property") or chg.get("attribute", "Unknown")
                                msg_html += f"<tr><td>{p}</td><td class='old-val'>{chg.get('old')}</td><td class='new-val'>{chg.get('new')}</td></tr>"
                            msg_html += "</table>"
                            
                    msg_html += "</div>"
            
    if not has_rel: msg_html = f"<p class='no-changes'>No modifications detected for node '{node_name}'.</p>"
    
    html_template = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>DBC Delta Report</title><style>body {{ font-family: sans-serif; background-color: #f8f9fa; color: #333; padding: 30px; }} .container {{ max-width: 1200px; margin: 0 auto; }} h1 {{ color: #1e293b; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }} .meta {{ color: #64748b; font-size: 14px; margin-bottom: 30px; }} .card {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }} table {{ width: 100%; border-collapse: collapse; margin: 8px 0 15px 0; font-size: 14px; }} th, td {{ padding: 8px 12px; border: 1px solid #e2e8f0; text-align: left; }} th {{ background-color: #f1f5f9; }} .old-val {{ background-color: #fef2f2; color: #991b1b; }} .new-val {{ background-color: #f0fdf4; color: #166534; }} .no-changes {{ color: #64748b; font-style: italic; background: #f1f5f9; padding: 15px; border-radius: 6px; }} .badge {{ font-size: 11px; padding: 3px 8px; border-radius: 12px; font-weight: bold; color: white; }} .badge-changed, .badge-modified {{ background-color: #d97706; }} .badge-added {{ background-color: #16a34a; }} .badge-deleted {{ background-color: #dc2626; }} .alert-e2e {{ background-color: #fff7ed; border: 1px solid #ffedd5; color: #c2410c; padding: 12px; border-radius: 6px; margin: 10px 0; }} .sig-block {{ background: #f8fafc; border: 1px solid #edf2f7; border-radius: 6px; padding: 12px; margin-top: 10px; }}</style></head><body><div class="container"><h1>Network Comparison Matrix</h1><div class="meta">Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Target Node: <strong>{node_name}</strong><br>Old DB: {os.path.basename(old_file)}<br>New DB: {os.path.basename(new_file)}</div><h2>1. Node Configuration Settings Matrix</h2>{global_html}<h2>2. Message Interface Delta Log</h2>{msg_html}</div></body></html>"""
    
    with open(file_path, "w", encoding="utf-8") as f: f.write(html_template)


@click.command()
@click.option("--old", "-f", required=True, type=click.Path(exists=True))
@click.option("--new", "-t", required=True, type=click.Path(exists=True))
@click.option("--report-formats", "-r", default="html,json")
@click.option("--output-base", "-o", default="report")
@click.option("--node", "-d", default="UCIM_UCIM2")
def main(old, new, report_formats, output_base, node):
    if isinstance(output_base, str) and output_base.lower().endswith(('.json', '.html')): 
        output_base = os.path.splitext(output_base)[0]
    report = compare_dbc(old, new, node)
    formats = [fmt.strip().lower() for fmt in report_formats.split(",")]
    report["messages"] = {k: v for k, v in report["messages"].items() if v["status"] != "changed" or v.get("message_level_changes") or v.get("signal_level_changes")}
    
    if "json" in formats:
        with open(f"{output_base}.json", "w", encoding="utf-8") as f: json.dump(report, f, indent=4)
        print(f"✔ JSON generated: {output_base}.json")
    if "html" in formats:
        save_html_report(report, f"{output_base}.html", node, old, new)
        print(f"✔ HTML generated: {output_base}.html")


if __name__ == "__main__":
    main()
