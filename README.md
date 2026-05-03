<div align="center">

# 🛠️ Multi-Tools: HWID Spoofer & System Utilities

![OS: Windows 10/11](https://img.shields.io/badge/OS-Windows%2010%20%7C%2011-0078D6?style=flat-square&logo=windows&logoColor=white)
![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat-square&logo=python&logoColor=white)
![Stage: Beta](https://img.shields.io/badge/Stage-Beta-FF8C00?style=flat-square)
![License: MIT](https://img.shields.io/badge/License-MIT-success?style=flat-square)

<p align="center">

  <img src="--/one.gif" alt="Multi-Tools Vibe" width="600">

</p>

*A specialized Windows system administration tool designed for security researchers to modify hardware identifiers and test device-based security implementations.*

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
