<div align="center">

# 🛠️ Multi-Tools: HWID Spoofer & System Utilities

[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=flat-square&logo=instagram&logoColor=white)](https://www.instagram.com/blackhat.emi)
![OS: Windows 10/11](https://img.shields.io/badge/OS-Windows%2010%20%7C%2011-0078D6?style=flat-square&logo=windows&logoColor=white)
![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat-square&logo=python&logoColor=white)
![Stage: Beta](https://img.shields.io/badge/Stage-Beta-FF8C00?style=flat-square)
![License: MIT](https://img.shields.io/badge/License-MIT-success?style=flat-square)

<p align="center">

  <img src="--/one.gif" alt="Multi-Tools Vibe" width="600">

</p>

</div>

---

## ⚠️ Disclaimer

> **This tool modifies system-level identifiers. Use at your own risk.**

*   Modifying disk IDs can prevent Windows from booting.
*   Changing MAC addresses may briefly disrupt network connectivity.
*   Altering system GUIDs can affect software licensing and activation.
*   **Always create a system backup or restore point before proceeding.**

---

## ✨ Features

**HWID Spoofer** - Comprehensive modification of hardware identifiers:
*   **🌐 Ethernet MAC Address Changer:** Registry-level modification and adapter reset.
*   **🏷️ Hostname Changer:** Randomized or custom computer name updates.
*   **💾 Disk ID Modifier:** Supports both MBR Signatures and GPT GUIDs.
*   **🔑 Machine GUID Spoofer:** Updates the Windows Cryptography GUID.
*   **💻 SMBIOS UUID Override:** Software-level system UUID masking.

---

## ⚙️ Requirements

*   **Operating System:** Windows 10 / 11
*   **Python:** 3.7 or higher
*   **PowerShell:** 5.1 or higher
*   **Privileges:** Administrator rights *(automatically requested by the script)*

---

## 🚀 Installation & Usage

1. **Clone the repository**

```bash
git clone [https://github.com/ollarethe4k-dotcom/Multi-Tools.git](https://github.com/ollarethe4k-dotcom/Multi-Tools.git)
```

```bash
cd Multi-Tools
```

---

## 🔍 Feature Details

### 1. Ethernet MAC Changer
Modifies the MAC address in the registry and cycles the adapter.
*   **Logic:** Updates `HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}`.
*   **Note:** The network connection will drop for approximately 3-5 seconds during the reset phase.

### 2. Disk ID Changer
*   **MBR:** Modifies the 8-character hex signature.
*   **GPT:** Modifies the unique GUID.
*   **Mechanism:** Takes the disk **Offline**, applies the new ID, and brings it back **Online** to force Windows to recognize the change.
*   **⚠️ WARNING:** Changing the ID of the `C:` drive is highly risky and may lead to "Inaccessible Boot Device" errors.

### 3. Security & Stealth
*   **Defender Exclusion:** The tool automatically attempts to add its working directory and the Python executable to the Windows Defender exclusion list to prevent "Access Denied" errors during low-level writes.
*   **Input Validation:** All ID formats are strictly validated before being written to the system.

---

## 🛠️ Troubleshooting

### Disk remains "Offline" or "Missing"
If a disk does not automatically reappear in File Explorer after a change:
1. Open **Disk Management** (`diskmgmt.msc`).
2. Locate the disk (it will be marked as *Offline* with a black arrow).
3. Right-click the Disk Name (e.g., *Disk 1*) and select **Online**.

### Access Denied Errors
Even with built-in exclusions, some third-party Antivirus software may aggressively block the script's low-level execution.
*   **Solution:** Temporarily disable "Real-time Protection" or "Tamper Protection" during the operation.

---

## 🤝 Collaboration & Code Contributions

We are in active development and welcome contributions that improve the tool's technical depth. Specifically, we are looking for:

*   **Forensic Consistency:** Help us implement advanced *timestomping* techniques to maintain registry and file system consistency after ID modifications.
*   **AV Compatibility:** Propose methods to refine dynamic exclusion logic.
*   **Optimization:** Improve PowerShell execution speed to minimize the "offline" window for hardware devices.

**Got a suggestion or found an issue?**
*   **Suggestions:** We accept proposals for new hardware obfuscation features via Pull Requests.
*   **Issue Reporting:** If a function fails (e.g., a Disk ID remains offline), please open an Issue so we can refine the error-handling logic.

---

## 📜 License

This project is distributed under the **MIT License**.
Refer to the [LICENSE](LICENSE) file for detailed information.

<div align="center">
  <i>Multi-Tools_v1.1</i>
</div>
