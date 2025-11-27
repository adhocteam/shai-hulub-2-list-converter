# Shai-Hulud 2.0 Vulnerability Scanner Helper

This repository contains tools to assist in detecting and mitigating the **Shai-Hulud 2.0** npm supply chain attack (November 2025). It provides a utility to convert between different vulnerability list formats (TXT and CSV) to ensure compatibility with various scanning tools, such as `shai-hulud-2-check`.

## 🚨 About Shai-Hulud 2.0

**Date:** November 2025  
**Severity:** Critical  
**Ecosystem:** npm (Node.js)

The Shai-Hulud 2.0 worm is a sophisticated supply chain attack targeting the npm ecosystem. Unlike typical malware that executes upon application startup, this worm utilizes malicious `preinstall` scripts to execute immediately when a developer runs `npm install`.

### Key Behaviors:
1.  **Bun Runtime Injection:** The malware checks for the [Bun](https://bun.sh) runtime. If missing, it downloads a script (`setup_bun.js`) to install it, using it to execute the main payload (`bun_environment.js`) in a detached background process.
2.  **Credential Exfiltration:** It scans local storage for secrets, including:
    * Cloud Credentials (AWS, GCP, Azure)
    * GitHub Personal Access Tokens (PATs)
    * NPM Publishing Tokens
3.  **Worm Propagation:** It uses stolen credentials to:
    * Create public GitHub repositories (often named "Shai-Hulud" or "The Second Coming") to dump stolen secrets.
    * Republish infected versions of other npm packages maintained by the victim.
    * Inject malicious GitHub Actions workflows.

---

## 🛡️ Mitigation Measures

If you suspect infection or use affected packages:

1.  **Stop Builds:** Immediately halt all CI/CD pipelines.
2.  **Clean Environment:**
    ```bash
    # Remove node_modules and clean cache
    rm -rf node_modules
    npm cache clean --force
    ```
3.  **Audit Dependencies:** Use the scripts provided in this repo or [shai-hulud-2-check](https://github.com/opctim/shai-hulud-2-check) to scan your lockfiles against the known malicious package list.
4.  **Rotate Credentials:** Revoke and rotate **all** credentials present on the machine (SSH keys, Cloud API keys, GitHub tokens, npm tokens).
5.  **Check GitHub Activity:** Look for unauthorized repositories created under your account or new workflows (e.g., `.github/workflows/discussion.yaml`).

---

## 🛠️ Tool Usage: Vulnerability List Converter

Different security researchers are publishing lists of compromised packages in different formats. 
* **DataDog** and **opctim/shai-hulud-2-check** use **CSV**.
* **Cobenian** and other researchers often use **TXT**.

This script, `vuln_converter.py`, converts between these formats so you can use any source list with your preferred scanner.

### Prerequisites
* Python 3.x

### 1. Convert TXT to CSV (Default)
Useful if you have a simple list (e.g., from a blog post) and need to use it with `shai-hulud-2-check`.

**Input Format (TXT):**
```text
package-name@1.0.0
@scope/package@2.1.0
