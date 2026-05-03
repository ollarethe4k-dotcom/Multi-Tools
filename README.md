# 🛠️ Multi-Tools v1.0 | HWID Spoofer and System Utilities 
# ⚠️ IMPORTANT NOTICES WINDOWS ONLY: This tool is designed exclusively for Windows 10 and 11.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<p align="center">
  <img src="--/one.gif" alt="Multi-Tools Vibe" width="600">
</p>

UNDER DEVELOPMENT (Beta): This tool is currently in active development. While core features are functional, users may encounter bugs or unexpected behavior.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
💡 COLLABORATION & FEEDBACK
We welcome suggestions! If you have ideas to improve the tool or encounter issues:

Suggestions: We accept proposals for new hardware obfuscation features.

Issue Reporting: If a function fails (e.g., a Disk ID remains offline), please report it so we can refine the error-handling logic.

Code Contributions: Help us make "timestomping" or AV bypass procedures even more silent.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
⚠️ DISCLAIMER
This tool modifies system-level identifiers. Use at your own risk.

Modifying disk IDs can prevent Windows from booting.  

Changing MAC addresses may briefly disrupt network connectivity.  

Altering system GUIDs can affect software licensing and activation.  

Always create a system backup or restore point before proceeding.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Features
HWID Spoofer - Comprehensive modification of hardware identifiers:

Ethernet MAC Address Changer: Registry-level modification and adapter reset.  

Hostname Changer: Randomized or custom computer name updates.  

Disk ID Modifier: Supports both MBR Signatures and GPT GUIDs.  

Machine GUID Spoofer: Updates the Windows Cryptography GUID.  

SMBIOS UUID Override: Software-level system UUID masking.  

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Requirements
Operating System: Windows 10/11.  

Python: 3.7 or higher.  

Privileges: Administrator rights (automatically requested by the script).  

PowerShell: 5.1 or higher.  

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Installation & Usage
Download Multi_Tools_11.py.  

Run the script via terminal (Administrator elevation will be requested automatically):  

Bash
python Multi_Tools_11.py
Navigation
Main Menu: Access the HWID Spoofer module. 

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Feature Details
1. Ethernet MAC Changer
Modifies the MAC address in the registry and cycles the adapter.

Logic: Updates HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}.  

Note: The connection will drop for approximately 3-5 seconds during the reset.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2. Disk ID Changer
MBR: Modifies the 8-character hex signature.  

GPT: Modifies the unique GUID.  

Mechanism: Takes the disk Offline, applies the new ID, and brings it back Online to force Windows to recognize the change.  

WARNING: Changing the ID of the C: drive is highly risky and may lead to "Inaccessible Boot Device" errors.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
3. Security & Stealth
Defender Exclusion: The tool automatically attempts to add its working directory and the Python executable to the Windows Defender exclusion list to prevent "Access Denied" errors during low-level writes.  

Input Validation: All ID formats are validated before being written to the system.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Troubleshooting
Disk remains "Offline" or "Missing"
If a disk does not automatically reappear in File Explorer after a change:

Open Disk Management (diskmgmt.msc).

Locate the disk (marked as Offline).

Right-click the Disk Name and select Online.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Access Denied
Even with the built-in exclusions, some third-party Antivirus software may block the script.

Solution: Temporarily disable "Real-time Protection" or "Tamper Protection" during the operation. 

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Version
Multi-Tools v1.1 

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 📜 License | This project is distributed under the MIT License.
Refer to the [LICENSE](LICENSE) file for detailed information.
