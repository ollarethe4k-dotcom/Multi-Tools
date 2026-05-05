<div align="center">

# 🛠️ Multi-Tools: HWID Spoofer & System Utilities

[![Static Badge](https://img.shields.io/badge/Target_OS-Windows%20%7C%20Linux-0078D6?style=for-the-badge&logo=gnumetadatacleaner&logoColor=white)]()
[![Static Badge](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Static Badge](https://img.shields.io/badge/License-MIT-success?style=for-the-badge&logo=opensourceinitiative&logoColor=white)]()
![GitHub last commit](https://img.shields.io/github/last-commit/ollarethe4k-dotcom/Multi-Tools?style=flat-square&color=blue)


<p align="center">
  <img src="--/one.gif" alt="Multi-Tools Vibe" width="600">
</p>

</div>

---

## ⚠️ Disclaimer

> **This tool modifies system-level identifiers. Use at your own risk.**

- Modifying **Disk IDs** can prevent Windows from booting if applied to the primary drive
- **Linux MOK** setup involves enrolling keys into your BIOS/UEFI; follow on-screen instructions during reboot
- Changing MAC addresses may briefly disrupt network connectivity during adapter reset
- **All changes are automatically logged** to `Multi-Tools_Backup.txt` on your Desktop
- **Always create a system restore point or full backup before proceeding**

---

## ✨ What's New in v1.3

### 🆕 Major Improvements
- **Dual Method Disk ID**: Now uses PowerShell `Set-Disk` with `Diskpart` fallback for better compatibility
- **Auto Backup System**: All critical changes (MAC, Disk ID, Machine GUID) logged with timestamps
- **MAC Validation**: Prevents invalid MAC addresses from being applied
- **Cross-Platform Detection**: Run on Windows to get Linux instructions, or directly on Linux for automation
- **Improved Error Handling**: Detailed error messages and troubleshooting hints

---

## 📋 Features

### 🖥️ HWID Spoofer (Windows Only)
Advanced hardware obfuscation through registry modifications and PowerShell automation:

| Feature | Description |
|---------|-------------|
| 🌐 **MAC Address Changer** | Modifies registry (`NetworkAddress`) and restarts Ethernet adapter automatically |
| 🏷️ **Hostname Changer** | Updates computer name with randomized strings or custom input |
| 💾 **Disk ID Modifier** | Dual method (PowerShell + Diskpart) for MBR Signatures and GPT GUIDs |
| 🔑 **Machine GUID Spoofer** | Generates and applies new cryptographic `MachineGuid` in registry |
| 💻 **SMBIOS UUID Override** | Masks system UUID in `HARDWARE\DESCRIPTION\System` registry hive |

### 🐧 Linux MOK Integration (Cross-Platform)
Automation for Secure Boot management, ideal for researchers and dual-boot environments:

| Feature | Description |
|---------|-------------|
| 🔐 **Automated MOK Setup** | Generates X.509 key pairs and registers via `mokutil` |
| 📦 **Distro Support** | Debian/Ubuntu/Kali (apt), Fedora/RHEL (dnf), Arch Linux (pacman) |
| 🛡️ **Secure Boot Helper** | Enables custom kernels while maintaining Secure Boot integrity |
| 💻 **Cross-Platform** | Run on Windows to get instructions, or directly on Linux for full automation |

---

## ⚙️ Requirements

### Operating Systems
- **Windows**: 10/11 (Administrator rights required)
- **Linux**: Debian, Ubuntu, Kali, Fedora, RHEL, Arch (Root access required)

### Software
- **Python**: Version 3.7 or higher
- **Windows**: PowerShell 5.1+ (included by default)
- **Linux**: `mokutil`, `openssl`, `sbsigntool` (auto-installed by script)

---

## 🚀 Installation & Usage

### Step 0: Check Python
Verify Python 3.7+ is installed:

**Windows:**
```bash
python --version
```
or
```bash
py --version
```

**Linux:**
```bash
python3 --version
```

If missing, download from [python.org](https://www.python.org/downloads/)  
*Windows: Check "Add Python to PATH" during install*

---

### 🪟 WINDOWS INSTALLATION

#### Step 1: Download the Script
Clone the repository:
```bash
git clone https://github.com/ollarethe4k-dotcom/Multi-Tools.git
cd Multi-Tools
```

Or download `Multi-Tools_v1.3.py` to any folder.

#### Step 2: Run the Script
Double-click the file **or** run from terminal (Administrator auto-requested):

```bash
python Multi-Tools_v1.3.py
```

If that fails, try:
```bash
py Multi-Tools_v1.3.py
```

**What happens on first run:**
1. Script requests Administrator privileges (auto-elevates)
2. Adds Defender exclusions for the script folder and Python
3. Shows the main menu

#### Step 3: Use the Tools
- Select **1** for HWID Spoofer (Windows only)
- Select **2** for Linux MOK Setup (shows instructions)

---

### 🐧 LINUX INSTALLATION

#### Step 1: Copy the Script
Copy `Multi-Tools_v1.3.py` to your Linux system (USB drive, download, etc.)

#### Step 2: Run with Root Privileges
```bash
sudo python3 Multi-Tools_v1.3.py
```

**What happens on first run:**
1. Script detects your Linux distribution
2. Auto-installs required packages (`mokutil`, `openssl`, etc.)
3. Generates MOK key pair
4. Guides you through BIOS enrollment

#### Step 3: Complete MOK Setup
After running the script:
1. **Reboot** your PC
2. In the blue **MOKManager** screen, select "Enroll MOK"
3. Enter the password you set during script run
4. Reboot again

---

## 🔍 How It Works

### HWID Spoofer (Windows)
```
Registry Modifications:
├── MAC Address → HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e972...}
├── Hostname → Through PowerShell Rename-Computer
├── Disk ID → PowerShell Set-Disk OR Diskpart (fallback)
├── Machine GUID → HKLM\SOFTWARE\Microsoft\Cryptography
└── SMBIOS UUID → HKLM\HARDWARE\DESCRIPTION\System
```

### Linux MOK Setup
```
Distribution Detection:
├── Debian/Ubuntu/Kali → apt install mokutil sbsigntool openssl
├── Fedora/RHEL → dnf install mokutil openssl + kmodgenca
└── Arch Linux → pacman -S mokutil sbsigntool openssl

Key Generation:
├── Private Key → MOK.priv
└── Public Key → MOK.der → mokutil --import
```

### Auto Backup System
All changes logged to: `C:\Users\[YourUser]\Desktop\Multi-Tools_Backup.txt`
```
Format:
[2026-05-04 16:30:00] MAC Address
Original: 00-11-22-33-44-55
New: 02-11-22-33-44-66
--------------------------------------------------
```

---

## 🛠️ Troubleshooting

### ❌ "Access Denied" (Windows)
**Solution:**
1. Ensure you're running as Administrator (script auto-requests, but check)
2. Disable **Tamper Protection** in Windows Security → Virus & Threat Protection → Manage Settings
3. Temporarily disable third-party antivirus
4. Check if Windows is protecting the disk (BitLocker, etc.)

### ❌ Disk ID Change Failed (v1.3)
**The script uses dual method (PowerShell + Diskpart fallback)**

**Solutions:**
- Ensure the disk doesn't have volumes in use (pagefile, system files)
- Try unmounting volumes first
- Check if Windows is protecting the disk
- Review detailed error output shown by the script
- Try on a non-system disk first

### ❌ Linux MOK Import Fails
**Solution:**
1. Ensure **Secure Boot** is enabled in BIOS
2. Reboot and enter BIOS/UEFI settings
3. Set "Secure Boot" to "Enabled" or "Custom"
4. Run script again and set a simple password (e.g., "12345678")
5. During MOKManager, use the **same password**

### ❌ Python Not Found
**Windows:** Reinstall Python with "Add Python to PATH" checked  
**Linux:** `sudo apt install python3` / `sudo dnf install python3` / `sudo pacman -S python`

---

## 🤝 Contributing

We encourage community involvement!

1. **Fork** the repository
2. **Branch**: `git checkout -b feature/YourFeature`
3. **Code**: Follow existing logic and style
4. **Test**: Ensure it works on your system
5. **Submit**: Open a Pull Request

---

## 🗺️ Future Roadmap

1. **💾 Kernel-Level Integration**: Ring-0 WDM drivers for persistence against deep-system scans
2. **🕰️ Forensic Integrity**: Restore registry "Last Write Time" timestamps (timestomping)
3. **🛡️ Anti-Virtualization**: Mitigate VMware/VirtualBox detection for sandbox research
4. **🖥️ Display & Peripheral**: Monitor EDID masking and USB Serial Descriptor randomization

---

## 💡 Support

- **Bug Reports**: Open an [Issue](https://github.com/ollarethe4k-dotcom/Multi-Tools/issues)
- **Discussions**: Start a [Discussion](https://github.com/ollarethe4k-dotcom/Multi-Tools/discussions)
- **Contributions**: Submit a Pull Request

---

## 📜 License

This project is distributed under the **MIT License**.  
See the `LICENSE` file for more details.

---

<div align="center">
  <b>Multi-Tools v1.3</b><br>
</div>
