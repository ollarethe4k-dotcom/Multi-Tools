<div align="center">

# 🛠️ Multi-Tools: HWID Spoofer & System Utilities

[![Static Badge](https://img.shields.io/badge/Target_OS-Windows%20%7C%20Linux-0078D6?style=for-the-badge&logo=gnumetadatacleaner&logoColor=white)]()
[![Static Badge](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Static Badge](https://img.shields.io/badge/Stage-Beta-FF8C00?style=for-the-badge&logo=rocket)]()
[![Static Badge](https://img.shields.io/badge/License-MIT-success?style=for-the-badge&logo=opensourceinitiative&logoColor=white)]()
![GitHub stars](https://img.shields.io/github/stars/ollarethe4k-dotcom/Multi-Tools?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/ollarethe4k-dotcom/Multi-Tools?style=flat-square&color=blue)

<p align="center">
  <img src="--/one.gif" alt="Multi-Tools Vibe" width="600">
</p>

</div>

---

## ⚠️ Disclaimer

> This tool modifies system-level identifiers and BIOS keys. 
> Use at your own risk.

* Modifying **Disk IDs** can prevent Windows from booting if applied to the primary drive.
* **Linux MOK** setup involves enrolling keys into your BIOS/UEFI; you must follow the on-screen instructions during reboot.
* Changing MAC addresses may briefly disrupt network connectivity during the adapter reset phase.
* **Always create a system restore point or a full backup before proceeding.**

---

## ✨ Features (v1.2)

### 🖥️ HWID Spoofer (Windows Only)
Advanced hardware obfuscation through registry modifications and PowerShell automation:

* **🌐 MAC Address Changer**: Modifies the physical address in the registry (`NetworkAddress`) and automatically restarts the Ethernet adapter.
* **🏷️ Hostname Changer**: Updates the computer name using randomized strings or custom user input.
* **💾 Disk ID Modifier**: Full support for **MBR Signatures** and **GPT GUIDs**, managing Offline/Online states to force system updates.
* **🔑 Machine GUID Spoofer**: Generates and applies a new cryptographic `MachineGuid`.
* **💻 SMBIOS UUID Override**: Masks the system UUID within the `HARDWARE\DESCRIPTION\System` registry hive.

### 🐧 Linux MOK Integration

Automation for Secure Boot management, ideal for researchers and dual-boot environments:

* **🔐 Automated MOK Setup**: Automatically generates X.509 key pairs (`MOK.der`) and registers them via `mokutil`.
* **📦 Distro Support**: Automated scripts for Debian/Ubuntu/Kali (apt), Fedora/RHEL (dnf), and Arch Linux (pacman).
* **🛡️ Secure Boot Helper**: Enables booting custom kernels while maintaining Secure Boot integrity.

---

## ⚙️ Requirements

* **Operating Systems**: Windows 10/11 or Linux Distributions (Debian, Ubuntu, Fedora, RHEL).
* **Python**: Version 3.7 or higher.
* **Privileges**: 
    * **Windows**: Administrator rights (automatically requested via `runas`).
    * **Linux**: Root access required (`sudo`).

---

## 🚀 Installation & Usage

### Prerequisites
Verify Python 3.7+ is installed:
- **Windows**: Run `python --version` or `py --version` in terminal
- **Linux**: Run `python3 --version` in terminal
If missing, install from [python.org](https://www.python.org/downloads/)
(Windows: check "Add Python to PATH" during install).

### 1. Clone the repository

```bash
git clone https://github.com/ollarethe4k-dotcom/Multi-Tools.git
```
```bash
cd Multi-Tools
```

### 2. Run the script

Windows (Administrator terminal):

```bash
python Multi-Tools_v1.2.py
```
 
Or use Python launcher if above fails:
  
```bash
py Multi-Tools_v1.2.py
```

 
Linux (root privileges):
```bash
sudo python3 Multi-Tools_v1.2.py
```

---

## 🔍 Technical Details

### Stealth & Security

* **Defender Exclusion**: The script automatically attempts to add its directory and the Python executable to the Windows Defender exclusion list using `Add-MpPreference`.
* **Input Validation**: Every identifier (MAC, GUID, Disk Signature) is strictly validated before being written to prevent registry corruption.
* **Power Automation**: Utilizes temporary `.ps1` scripts to bypass execution restrictions and apply deep network hardware changes.

### Disk Management

* The script identifies disks using `Get-Disk` and distinguishes between MBR (8-character hex) and GPT (Full GUID) partition styles.
* It implements wait cycles (`Start-Sleep`) to ensure the OS correctly registers hardware state changes after toggling drives online.

---

## 🛠️ Troubleshooting

### Linux MOK Error

If the `mokutil --import` command fails, ensure **Secure Boot** is enabled in your BIOS and that the password entered during the script is reused correctly in the MOKManager interface upon reboot.

### Access Denied (Windows)

If you encounter permission errors despite having admin rights, verify that **Tamper Protection** in Windows Security is not blocking PowerShell calls to the registry.

---

<div align="center">

## 🤝 Collaboration & Contributions

**We encourage community involvement to advance the project.** 

</div>

1. **Fork the Repository**: Create a personal copy of the project by clicking the `Fork` button.
2. **Branch Management**: Create a dedicated branch for your feature (`git checkout -b feature/AdvancedModule`).
3. **Code Quality**: Ensure your code is production-ready and follows the existing logic structure.
4. **Submission**: Push your changes and open a **Pull Request** for technical review.

---

<div align="center">

## 🗺️ Future Roadmap & Implementation Goals

</div>

1. **💾 Kernel-Level Integration**: Shifting from registry-based modification to WDM drivers to manage hardware identifiers at Ring-0, ensuring persistence against deep-system scans.
2. **🕰️ Forensic Integrity (Timestomping)**: Development of logic to restore original registry "Last Write Time" timestamps, maintaining system consistency and preventing forensic detection.
3. **🛡️ Anti-Virtualization Modules**: Implementation of advanced techniques to mitigate environment detection (VMware/VirtualBox) for researchers operating within virtualized sandboxes.
4. **🖥️ Display & Peripheral Obfuscation**: Expanding the toolkit to include Monitor EDID masking and USB Serial Descriptor randomization for HID and storage devices.

---

<div align="center">

### 💡 Feedback & Technical Support
For bug reports or architectural suggestions, please open a formal **Issue** or start a **Discussion**.  

---

## 📜 License

This project is distributed under the **MIT License**. See the `LICENSE` file for more details.

<div align="center">
  <i>Multi-Tools v1.2</i>
</div>
