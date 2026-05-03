<div align="center">

# 🛠️ Multi-Tools: HWID Spoofer & System Utilities

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

1. Download the script to your local machine.
2. Run the script via terminal. Administrator elevation will be requested automatically if not already present.

```bash
python Multi_Tools_11.py
```



---

## 🔍 Feature Details

### 1. Ethernet MAC Changer
Modifies the MAC address in the registry and cycles the adapter[cite: 2].
*   **Logic:** Updates `HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}`[cite: 2].
*   **Note:** The network connection will drop for approximately 3-5 seconds during the reset phase[cite: 2].

### 2. Disk ID Changer
*   **MBR:** Modifies the 8-character hex signature[cite: 2].
*   **GPT:** Modifies the unique GUID[cite: 2].
*   **Mechanism:** Takes the disk **Offline**, applies the new ID, and brings it back **Online** to force Windows to recognize the change[cite: 2].
*   **⚠️ WARNING:** Changing the ID of the `C:` drive is highly risky and may lead to "Inaccessible Boot Device" errors[cite: 2].

### 3. Security & Stealth
*   **Defender Exclusion:** The tool automatically attempts to add its working directory and the Python executable to the Windows Defender exclusion list to prevent "Access Denied" errors during low-level writes[cite: 2].
*   **Input Validation:** All ID formats are strictly validated before being written to the system[cite: 2].

---

## 🛠️ Troubleshooting

### Disk remains "Offline" or "Missing"
If a disk does not automatically reappear in File Explorer after a change[cite: 2]:
1. Open **Disk Management** (`diskmgmt.msc`)[cite: 2].
2. Locate the disk (it will be marked as *Offline* with a black arrow)[cite: 2].
3. Right-click the Disk Name (e.g., *Disk 1*) and select **Online**[cite: 2].

### Access Denied Errors
Even with built-in exclusions, some third-party Antivirus software may aggressively block the script's low-level execution[cite: 2].
*   **Solution:** Temporarily disable "Real-time Protection" or "Tamper Protection" during the operation[cite: 2].

---

## 🤝 Collaboration & Code Contributions

We are in active development and welcome contributions that improve the tool's technical depth. Specifically, we are looking for[cite: 2]:

*   **Forensic Consistency:** Help us implement advanced *timestomping* techniques to maintain registry and file system consistency after ID modifications[cite: 2].
*   **AV Compatibility:** Propose methods to refine dynamic exclusion logic, ensuring the tool operates smoothly alongside modern EDR/Antivirus heuristics during legitimate research[cite: 2].
*   **Optimization:** Improve PowerShell execution speed to minimize the "offline" window for hardware devices[cite: 2].

**Got a suggestion or found an issue?**
*   **Suggestions:** We accept proposals for new hardware obfuscation features via Pull Requests[cite: 2].
*   **Issue Reporting:** If a function fails (e.g., a Disk ID remains offline), please open an Issue so we can refine the error-handling logic[cite: 2].

---

## 📜 License

This project is distributed under the **MIT License**[cite: 2].
Refer to the [LICENSE](LICENSE) file for detailed information[cite: 2].

<div align="center">
  <i>Multi-Tools v1.1</i>
</div>
