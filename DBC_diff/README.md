# 📋 DBC Database Difference Generator Playbook

An engineering utility designed to parse, analyze, and map structural deltas between two CAN/CAN FD Network Database (`.dbc`) files. The tool extracts global attribute modifications, shifts in message structures, bit-level modifications, and automatically categorizes Functional Safety **End-to-End (E2E) protection envelope drops** across target interfaces.

---

## 🛠️ Section 1: Environmental Setup

Before executing the tool, ensure your workspace is provisioned with Python and the required system packages.

### 1. Check Python Installation
Open a command prompt or terminal window and execute:
```bash
python --version
```
*Note: Ensure Python 3.10 or a newer version is installed on your local computer.*

### 2. Install Package Dependencies
Navigate into your target script folder directory and execute the package installer using the provided configuration file:
```bash
pip install -r requirements.txt
```

---

## 🚀 Section 2: How to Execute the Script

The diff engine supports **two distinct operating layout variations** depending on whether you want a highly isolated ECU-level focus or a wide-open bus infrastructure matrix view.

### Option A: Hyper-Targeted Node Filtering (Isolating an ECU)
Use this option when you only care about the explicit interfaces changing for a single electronic control unit. The tool automatically removes the structural noise from all other independent nodes on the bus.

Execute the following exact command format inside your shell profile:
```cmd
python dbcdiff.py -f .\<add old dbc name.dbc> -t .\<add new dbc name.dbc> -o report -d <node name>
```
*   **`-f` (`--old`)**: Point this to your baseline archive database.
*   **`-t` (`--new`)**: Point this to the newly modified update database.
*   **`-o` (`--output-base`)**: The base name string for output files (omitting extension).
*   **`-d` (`--node`)**: The precise string name of the target node filter environment.

### Option B: Wide-Open Global Audit (All Network Deltas)
If you completely omit the `-d` option argument from the command line array, **the strict isolation rules are automatically bypassed**. The tool will process the entire database, catching additions, modifications, and drops across every single node on the network container (e.g., `GWM`, `APIM`, `GENERIC`, etc.):

```cmd
python dbcdiff.py -f .\<add old dbc name.dbc> -t .\<add new dbc name.dbc> -o report
```

---

## 📊 Section 3: Reading the Output Dashboard

When execution wraps up successfully, two files are created side-by-side inside your directory:
1.  **`report.json`**: The raw data tree for automated pipeline handling or secondary software tools.
2.  **`report.html`**: An eye-catching, interactive visualization report dashboard for design audits.

### Visual Clues and Status Color-Coding:
*   **🟥 Red Indicators (`DELETED`)**: Signals or message structures completely dropped from the network layout. To maximize readability, the tool suppresses empty, messy property tables for dropped data rows.
*   **🟩 Green Indicators (`ADDED`)**: Newly introduced interface elements. A streamlined specification sheet shows the exact new values, omitting irrelevant blank columns.
*   **🟨 Yellow Indicators (`CHANGED`)**: Existing interface points modified. Displays a clear side-by-side comparison (`Param | Old | New`) tracking parameter shifts like bit bounds, scale adjustments, or initial constants.
*   **⚠️ E2E Architectural Structural Shift Cards**: Big red-bordered warning alerts displayed right at the top of a message layout change log. These notify you immediately if rolling counters or CRC protection fields were stripped out as a systematic block change.