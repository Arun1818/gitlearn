#!/usr/bin/env python3

import datetime
import json
import logging
import os
import sys
import click
import jinja2


class ToolLogger:

    def __init__(self, name, log_file=None):
        fmt_console = "%(levelname)-9s | %(message)s"
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(logging.Formatter(fmt_console))
        self.logger.addHandler(stdout_handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
        raise Exception(msg)


logger = ToolLogger(name="dbc-diff")

message_properties = {
    "frame_id": "hex",
    "is_extended_frame": "basic",
    "is_fd": "basic",
    "length": "basic",
    "send_type": "basic",
    "cycle_time": "basic",
    "senders": "list",
}

signal_properties = {
    "minimum": "basic",
    "maximum": "basic",
    "start": "basic",
    "length": "basic",
    "byte_order": "basic",
    "is_signed": "basic",
    "initial": "str",
    "invalid": "basic",
    "unit": "basic",
    "scale": "basic",
    "offset": "basic",
    "is_float": "basic",
    "choices": "dict",
    "spn": "basic",
    "receivers": "list",
}


def is_node_relevant(message, node_name="cutom_node"):
    if message is None:
        return False

    if hasattr(message, "senders") and message.senders:
        if any(node_name == str(sender) for sender in message.senders):
            return True

    if hasattr(message, "signals") and message.signals:
        for sig in message.signals:
            if hasattr(sig, "receivers") and sig.receivers:
                if any(node_name == str(rcv) for rcv in sig.receivers):
                    return True

    return False


def dbc_loader(dbc_file: str):
    import cantools

    messages = {}
    version = None
    if dbc_file is not None:
        dbc = cantools.database.load_file(dbc_file, strict=False)
        for dbc_message in dbc.messages:
            signals = {}
            for signal in dbc_message.signals:
                signals[signal.name] = signal
            setattr(dbc_message, "msg_signals", signals)
            messages[dbc_message.name] = dbc_message
        version = (
            "unknown"
            if dbc.version is None or len(dbc.version) == 0
            else dbc.version
        )
    return messages, version


def converter(value, from_type):
    if value is None:
        return None
    elif from_type == "hex":
        return f"{hex(value)}"
    elif from_type == "str":
        return str(value)
    elif from_type == "dict":
        res = {}
        for k, v in value.items():
            res[int(k)] = str(v)
        return dict(sorted(res.items()))
    elif from_type == "list":
        return ",".join(value)
    return value


def compare_dictionaries(old: dict, new: dict) -> (dict, dict, dict):
    old_set = set(old.keys())
    new_set = set(new.keys())
    same = old_set & new_set
    deleted = old_set - new_set
    added = new_set - old_set
    return sorted(added), sorted(same), sorted(deleted)


def build_change(action, change, signals=None):
    if signals is not None:
        return {"action": action, action: change, "signals": signals}
    return {"action": action, action: change}


def build_action(action, item, properties, signals=None):
    properties_list = []
    for item_property, from_type in properties.items():
        value = converter(getattr(item, item_property), from_type)
        if action == "deleted" and value is not None:
            properties_list.append(
                {"name": item_property, "old": value, "new": None}
            )
        elif action == "added" and value is not None:
            properties_list.append(
                {"name": item_property, "old": None, "new": value}
            )
    return build_change(action, properties_list, signals)


def compare_properties(old_object, new_object, properties: dict) -> list:
    changes_list = []
    for name, from_type in properties.items():
        old_prop = converter(getattr(old_object, name), from_type)
        new_prop = converter(getattr(new_object, name), from_type)
        if old_prop != new_prop:
            changes_list.append(
                {"name": name, "old": old_prop, "new": new_prop}
            )
    return changes_list


def compare_messages(old_message, new_message, node_name="cutom_node"):
    msg_changes = compare_properties(
        old_message, new_message, message_properties
    )
    sig_changes = {}
    added, same, deleted = compare_dictionaries(
        old_message.msg_signals, new_message.msg_signals
    )

    is_sender = hasattr(old_message, "senders") and any(
        node_name == str(s) for s in old_message.senders
    )

    for name in same:
        sig_old = old_message.msg_signals[name]
        sig_new = new_message.msg_signals[name]

        is_receiver = (
            hasattr(sig_old, "receivers")
            and any(node_name == str(r) for r in sig_old.receivers)
        ) or (
            hasattr(sig_new, "receivers")
            and any(node_name == str(r) for r in sig_new.receivers)
        )

        if is_sender or is_receiver:
            diff_list = compare_properties(
                sig_old, sig_new, signal_properties
            )
            if len(diff_list) > 0:
                sig_changes[name] = build_change("changed", diff_list)

    for name in deleted:
        sig_old = old_message.msg_signals[name]
        if is_sender or (
            hasattr(sig_old, "receivers")
            and any(node_name == str(r) for r in sig_old.receivers)
        ):
            sig_changes[name] = build_action(
                "deleted", sig_old, signal_properties
            )

    for name in added:
        sig_new = new_message.msg_signals[name]
        if is_sender or (
            hasattr(sig_new, "receivers")
            and any(node_name == str(r) for r in sig_new.receivers)
        ):
            sig_changes[name] = build_action(
                "added", sig_new, signal_properties
            )

    return msg_changes, sig_changes


def message_signals(action: str, signals: dict, node_name="cutom_node") -> dict:
    sig_changes = {}
    for name, signal in signals.items():
        if hasattr(signal, "receivers") and any(
            node_name == str(r) for r in signal.receivers
        ):
            sig_changes[name] = build_action(action, signal, signal_properties)
    return sig_changes


def compare_dbc(old_path, new_path, node_name="cutom_node") -> (dict, dict):
    old_dbc, old_ver = dbc_loader(old_path)
    new_dbc, new_ver = dbc_loader(new_path)
    dbc_report = {}
    versions = {}
    added, same, deleted = compare_dictionaries(old_dbc, new_dbc)

    for name in same:
        if not (
            is_node_relevant(old_dbc.get(name), node_name)
            or is_node_relevant(new_dbc.get(name), node_name)
        ):
            continue
        msg_diff, sig_diff = compare_messages(
            old_dbc[name], new_dbc[name], node_name
        )
        if len(msg_diff) > 0 or len(sig_diff) > 0:
            dbc_report[name] = build_change("changed", msg_diff, sig_diff)

    for name in deleted:
        if is_node_relevant(old_dbc.get(name), node_name):
            sig_diffs = message_signals(
                "deleted", old_dbc[name].msg_signals, node_name
            )
            dbc_report[name] = build_action(
                "deleted", old_dbc[name], message_properties, sig_diffs
            )

    for name in added:
        if is_node_relevant(new_dbc.get(name), node_name):
            sig_diffs = message_signals(
                "added", new_dbc[name].msg_signals, node_name
            )
            dbc_report[name] = build_action(
                "added", new_dbc[name], message_properties, sig_diffs
            )

    if new_path is not None:
        versions["new_version"] = new_ver
    if old_path is not None:
        versions["old_version"] = old_ver
    versions["same_version"] = old_ver == new_ver
    return dbc_report, versions


def enum_files(folder: str, ext: str) -> dict:
    populated_files = {}
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(ext):
                path = os.path.join(root, file)
                if file in populated_files:
                    logger.error(f"Duplicate DBC found: {path}")
                populated_files[file] = path
    return populated_files


def write_json_report(output_path: str, data: dict) -> str:
    if not output_path.endswith(".json"):
        output_path += ".json"
    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.truncate()
        out_file.write(json.dumps(data, indent=4))
    return output_path


def get_report(
    old_files: dict, new_files: dict, unchanged: bool, node_name="cutom_node"
) -> dict:
    compare_report = {}
    added, same, deleted = compare_dictionaries(old_files, new_files)
    for f in added:
        rep, ver = compare_dbc(None, new_files[f], node_name)
        if rep:
            compare_report[f] = build_change("added", rep) | ver
    for f in deleted:
        rep, ver = compare_dbc(old_files[f], None, node_name)
        if rep:
            compare_report[f] = build_change("deleted", rep) | ver
    for f in same:
        rep, ver = compare_dbc(old_files[f], new_files[f], node_name)
        if len(rep) > 0 or not ver["same_version"]:
            compare_report[f] = build_change("changed", rep) | ver
        elif unchanged:
            compare_report[f] = build_change("unchanged", rep) | ver
    return compare_report


def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))


def get_script_name():
    base = os.path.basename(os.path.realpath(__file__))
    return os.path.splitext(base)[0]


def generate_from_template(temp_name, temp_params, output_path):
    loader = jinja2.FileSystemLoader(get_script_path())
    env = jinja2.Environment(
        loader=loader, trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template(temp_name)
    content = template.render(temp_params)
    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.truncate()
        out_file.write(content)
        logger.info(f"Generated: {output_path}")


@click.command(context_settings={"ignore_unknown_options": True})
@click.option("--old", "-f", required=True, type=click.Path(exists=True))
@click.option("--new", "-t", required=True, type=click.Path(exists=True))
@click.option("--unchanged", "-u", is_flag=True, default=False)
@click.option("--reports", "-r", required=True, type=str)
@click.option("--node", "-d", default="cutom_node", type=str)
@click.option("--info", "-i")
@click.option("--name", "-n", type=str)
@click.option("--output", "-o", type=click.Path(exists=True))
def main(old, new, unchanged, reports, node, info, name, output):
    old_base = None
    if os.path.isdir(old):
        old_files = enum_files(old, ".dbc")
    elif os.path.isfile(old):
        old_base = os.path.basename(old)
        old_files = {old_base: old}

    if os.path.isdir(new):
        new_files = enum_files(new, ".dbc")
    elif os.path.isfile(new):
        new_base = os.path.basename(new)
        if old_base is not None and old_base != new_base:
            new_base = f"{old_base} -> {new_base}"
            old_files[new_base] = old_files.pop(old_base)
        new_files = {new_base: new}

    compare_report = get_report(old_files, new_files, unchanged, node)
    rep_name = get_script_name() if name is None else name
    rep_path = get_script_path() if output is None else output

    # Clean string literal representation to ensure no newline-wrapping issues
    chars_to_strip = " \n\r\t"
    for tag in reports.split(","):
        ext = tag.strip(chars_to_strip)
        save_path = os.path.join(rep_path, f"{rep_name}.{ext}")
        t_name = f"{get_script_name()}.{ext}.jinja2"

        if ext == "json":
            write_json_report(save_path, compare_report)
        else:
            if info is None:
                info = str(datetime.datetime.now())
            generate_from_template(
                t_name,
                {"dbc_files": compare_report, "build_info": info},
                save_path,
            )


if __name__ == "__main__":
    main()
