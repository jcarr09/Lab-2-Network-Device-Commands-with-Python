# Instructions — Lab 2 — Network Device Commands with Python

## Objectives

- Use Netmiko to establish SSH sessions to Cisco network devices.
- Collect credentials securely using `input()` and `getpass.getpass()`.
- Execute IOS 'show' commands and capture output programmatically.
- Parse command output with ntc-templates for structured data.
- Use f-strings to generate readable terminal or file output.
- Implement error handling and logging for reliability and grading.

## Prerequisites

- Python 3.11 (via the provided dev container)
- Accounts: GitHub, Cisco DevNet
- Devices/Sandboxes: Cisco DevNet Always-On Catalyst 8k/9k Sandbox
- Technical: - Python basics: functions, classes, exceptions, and file I/O.
- Understanding of SSH and network device access concepts.
- GitHub workflow: clone, commit, push, and pull request.
- Access to Cisco DevNet Always-On Sandbox and credentials.
- Basic familiarity with Netmiko and TextFSM templates.
- VS Code with dev container or local Python environment.

## Table of Contents

1. [Overview](#overview)
2. [Resources](#resources)
3. [Deliverables](#deliverables)
4. [Step 1 — Clone the Repository](#step-1--clone-the-repository)
5. [Step 2 — Open Dev Container](#step-2--open-dev-container)
6. [Step 3 — Collect Credentials Securely](#step-3--collect-credentials-securely)
7. [Step 4 — Connect to Device with Netmiko](#step-4--connect-to-device-with-netmiko)
8. [Step 5 — Run Show Commands](#step-5--run-show-commands)
9. [Step 6 — Parse Output with NTC Templates](#step-6--parse-output-with-ntc-templates)
10. [Step 7 — Generate Report and Summary](#step-7--generate-report-and-summary)
11. [Step 8 — Implement the Direct Execution Check](#step-8---implement-the-direct-execution-check)
12. [Step 9 — Refactor, Log, and Submit](#step-9--refactor-log-and-submit)
13. [FAQ](#faq)
14. [🔧 Troubleshooting & Pro Tips](#-troubleshooting--pro-tips)
15. [Grading Breakdown](#grading-breakdown)
16. [Autograder Notes](#autograder-notes)
17. [Submission Checklist](#submission-checklist)

## Overview

In this lab, you'll connect to a Cisco Catalyst 8k device in the Cisco DevNet Always-On Sandbox using the Netmiko 
library. You'll authenticate securely using user input and `getpass`, execute several "show" commands, capture and 
parse their output with `ntc-templates`, and generate clean, structured summaries using f-strings. You'll log every 
step so the autograder can validate markers and ensure safe, idempotent network automation practices.


> **Before you begin:** Ensure your Cisco DevNet Always-On Catalyst 8k sandbox is active and reachable. 
> Open the provided dev container or a local environment with Netmiko installed via requirements.txt. 
> Confirm connectivity with a simple ping to the device before proceeding.

## Resources

- [Cisco DevNet Always-On Sandboxes](https://developer.cisco.com/site/sandbox/)
- [Netmiko Documentation](https://ktbyers.github.io/netmiko/)
- [NTC Templates (TextFSM)](https://github.com/networktocode/ntc-templates)
- [getpass — Secure password input](https://docs.python.org/3/library/getpass.html)
- [Python logging](https://docs.python.org/3/library/logging.html)

## Deliverables

- `src/` contains: Any helper modules if used.
- `logs/lab.log` contains required Netmiko connection and parsing markers.
- Outputs (raw CLI or parsed data) saved under `data/raw/` or `data/reports/`.
- Pull request open to main branch with all artifacts committed.
- Grading: **75 points**

Follow these steps in order.

> **Logging Requirement:** Write progress to `logs/lab.log` as you complete each step.

## Step 1 — Clone the Repository

**Goal:** Get your starter files locally.

**What to do:**  
Clone your GitHub Classroom repo and `cd` into it.
Review the provided folder layout and add required directories.

**You're done when:**  

- Repository opened and visible in VS Code or terminal.
- You have created a `logs/`, `data/raw`, `data/reports` directory if missing.

## Step 2 — Open Dev Container

**Goal:** Verify environment setup.

**What to do:**
Open the repo inside the dev container and wait for the image to finish loading.
Run `pip list` to verify Netmiko and ntc-templates are installed.

**You're done when:**

- Python 3.11+ confirmed.
- Both Netmiko and ntc-templates packages are listed.
- `[STEP 2] Dev Container Started` logged to `logs/lab.log`.

## Step 3 — Collect Credentials Securely

**Goal:** Prompt user for username and password safely.

**What to do:**

In your script, use:

- `username = input("Enter username: ")`
- `password = getpass.getpass("Enter password: ")`
Never hardcode credentials or commit them to GitHub.
Log `CREDENTIALS_COLLECTED` after both values are accepted.

**You're done when:**  

- Password entry masked in terminal.
- Log file includes `CREDENTIALS_COLLECTED`.

**Log marker to add:**  
`[CREDENTIALS_COLLECTED]`

## Step 4 — Connect to Device with Netmiko

**Goal:** Establish an SSH connection to the Catalyst 8k.

**What to do:**  

Use `ConnectHandler()` from Netmiko with parameters:

- device_type: "cisco_ios"
- host, username, password
Wrap your connection in try/except to handle `AuthenticationException`, `NetMikoTimeoutException`, `SSHException`, and `Exception`.
Log `CONNECT_OK` or `CONNECT_FAIL` accordingly.

**You're done when:**  

- SSH connection succeeds and hostname banner returned.
- Log includes either `CONNECT_OK` or `CONNECT_FAIL`.

**Log marker to add:**  
`[CONNECT_OK, CONNECT_FAIL]`

## Step 5 — Run Show Commands

**Goal:** Collect output from the device.

**What to do:**  
Execute a few key commands such as:

- `show version`
- `show ip interface brief`
- `show inventory`
Write each output to a separate file under `data/raw/`.
Log `CMD_RUN:<command>` for each command executed.

**You're done when:**  

- Command outputs saved under `data/raw/`.
- Log file includes three or more `CMD_RUN` markers.

**Log marker to add:**  
`[CMD_RUN]`

## Step 6 — Parse Output with NTC Templates

**Goal:** Convert unstructured CLI output into structured data.

**What to do:**  
Import `ntc_templates.parse_output()` or TextFSM-based helpers.
Parse each output and verify structured keys/values.
Log `PARSE_OK:<command>` or `PARSE_FAIL:<command>` accordingly.

**You're done when:**  

- Parsed data validated (non-empty lists or dicts).
- Log includes all `PARSE_OK` markers for executed commands.

**Log marker to add:**  
`[PARSE_OK]`

## Step 7 — Generate Report and Summary

**Goal:** Use f-strings to summarize parsed device info.

**What to do:**  
Extract key facts like hostname, model, version, and interface states.
Compose a formatted message using f-strings and print it to the terminal.
Optionally save to `data/reports/device_summary.txt`.
Log `REPORT_SAVED` once the file is written.

**You're done when:**  

- Device summary printed and/or saved.
- Log includes `REPORT_SAVED`.

**Log marker to add:**  
`[REPORT_SAVED]`

## Step 8 — Implement the Direct Execution Check

**Goal:** Require that the code is executed directly from the `main.py` file

**What to do:**
Implement the Direct Execution Check.
Include a log message before the `main()` function for `[LAB2-START]`.
Include a log message after the `main()` function for `[LAB2-END]`.

**You're done when:**

- Your main function only executes if called directly.

**Log Marker:**
`[LAB2-START, LAB2-END]`

## Step 9 — Refactor, Log, and Submit

**Goal:** Ensure consistent structure and final submission.

**What to do:**  
Verify main program flow under `if __name__ == "__main__":`.
Close SSH session gracefully and log `LAB2_END`.
Commit all changes, push to GitHub, and open a pull request.

**You're done when:**  

- PR opened with complete code and logs.
- Autograder markers found in `logs/lab.log`.

## FAQ

**Q:** What if my connection times out?  
**A:** Verify the sandbox is active and use the correct IP or hostname. Increase `timeout=10` if needed.

**Q:** Why do I get empty parsed output?  
**A:** Ensure the command matches an existing NTC template exactly—no aliases.

**Q:** Can I print instead of saving a report?  
**A:** Yes, printing to terminal is fine as long as `REPORT_SAVED` is logged.

## 🔧 Troubleshooting & Pro Tips

**Connection Failures**  
*Symptom:* AuthenticationException or SSHException raised.  
*Fix:* Double-check credentials and host reachability; ensure SSH is enabled.

**Template Parsing Errors**  
*Symptom:* Returned list is empty.  
*Fix:* Command syntax must exactly match template definitions.

**File Writing Errors**  
*Symptom:* FileNotFoundError when saving under data/.  
*Fix:* Ensure directories exist and use relative paths from repo root.

**Logging Not Written**  
*Symptom:* `logs/lab.log` missing or empty.  
*Fix:* Call `logging.basicConfig(filename='logs/lab.log', level=logging.INFO)` once at startup.

## Grading Breakdown

| Step | Requirement | Points |
|---|---|---|
| Step 2 | Dev Container opened; packages verified | 5 |
| Step 3 | Credentials collected securely (`getpass` used) | 5 |
| Step 4 | Successful connection to device (`CONNECT_OK`) | 10 |
| Step 5 | Three or more commands executed (`CMD_RUN` markers) | 10 |
| Step 6 | All outputs parsed successfully (`PARSE_OK` markers) | 10 |
| Step 7 | Readable report printed/saved (`REPORT_SAVED`) | 10 |
| Step 4–7 | Handled exceptions gracefully and logged results | 5 |
| Step 8 | Lab Start message logged (`LAB2-START`) | 5 |
| Step 8 | Lab End message logged (`LAB2-END`) | 5 |
| Step 9 | Modular code structure (main.py entrypoint; helpers in src/) | 5 |
| Step 9 | Commit, push, and PR opened; logs present with start/end markers | 5 |
| **Total** |  | **75** |

## Autograder Notes

- Log file: `logs/lab.log`
- Required markers: `LAB2_START`, `CREDENTIALS_COLLECTED`, `CONNECT_OK`, `CMD_RUN`,
  `PARSE_OK`, `REPORT_SAVED`, `LAB2_END`

## Submission Checklist

- [ ] `logs/lab.log` exists and includes LAB2_START/LAB2_END and all required markers.
- [ ] Netmiko connection succeeds; output saved and parsed.
- [ ] NTC templates applied correctly with structured output.
- [ ] Device summary printed or saved with REPORT_SAVED logged.
- [ ] Code follows modular structure and uses secure credential handling.
- [ ] All work pushed and pull request open before deadline.
