import os
import subprocess
import random
import string
import ctypes
import sys
import csv
import io
import time

ESC = chr(27)

if os.name == 'nt':
    try:
        k = ctypes.windll.kernel32
        h = k.GetStdHandle(-11)
        m = ctypes.c_ulong()
        k.GetConsoleMode(h, ctypes.byref(m))
        m.value |= 0x0004
        k.SetConsoleMode(h, m)
    except:
        pass

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def red(t):
    return ESC + '[91m' + str(t) + ESC + '[0m'

def green(t):
    return ESC + '[92m' + str(t) + ESC + '[0m'

def yellow(t):
    return ESC + '[93m' + str(t) + ESC + '[0m'

def run_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except Exception as e:
        return '', 'Command failed: ' + str(e), -1

def run_live_cmd(cmd):
    print(yellow(f"Running: {cmd}"))
    subprocess.run(cmd, shell=True)

def header(t):
    clear()
    print(str(t).center(50))
    print('-' * 50)
    print()

def success(msg):
    print()
    print('=' * 50)
    print(green('SUCCESS: ') + str(msg))
    print('=' * 50)
    time.sleep(5)

def error(msg):
    print()
    print('=' * 50)
    print(red('ERROR: ') + str(msg))
    print('=' * 50)

def warning(msg):
    print(red('WARNING: ') + str(msg))

def note(msg):
    print('NOTE: ' + str(msg))

def backup(module, original, new):
    backup_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Multi-Tools_Backup.txt')
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(backup_path, 'a') as f:
            f.write(f"[{timestamp}] {module}\nOriginal: {original}\nNew: {new}\n" + "-"*50 + "\n")
    except:
        pass

def pause():
    input('\nPress Enter to continue...')

# ==========================================
# WINDOWS HWID SPOOFER FUNCTIONS
# ==========================================

def get_adapters():
    cmd = "powershell -C \"Get-NetAdapter | ?{$_.Name -like '*Ethernet*'} | select Name,InterfaceDescription | ConvertTo-Csv -NoType\""
    out, _, rc = run_cmd(cmd)
    if not out or rc != 0:
        return []
    adapters = []
    try:
        reader = csv.reader(io.StringIO(out))
        h = next(reader, None)
        if h and 'Name' in h:
            ni = h.index('Name')
            di = h.index('InterfaceDescription')
            for row in reader:
                if len(row) > max(ni, di):
                    adapters.append(row[ni].strip() + ' - ' + row[di].strip())
    except Exception as e:
        print('get_adapters error:', e)
    return adapters

def get_disks():
    cmd = "powershell -C \"Get-Disk | select Number,FriendlyName,PartitionStyle,Signature,Guid | ConvertTo-Csv -NoType\""
    out, _, rc = run_cmd(cmd)
    if not out or rc != 0:
        return []
    disks = []
    try:
        reader = csv.reader(io.StringIO(out))
        h = next(reader, None)
        if not h:
            return []
        ni = h.index('Number')
        fi = h.index('FriendlyName')
        pi = h.index('PartitionStyle')
        si = h.index('Signature')
        gi = h.index('Guid')
        for row in reader:
            if len(row) > max(ni, fi, pi, si, gi):
                num = row[ni]
                letters = []
                out2, _, _ = run_cmd("powershell -C \"Get-Partition -DiskNumber " + str(num) + " | ?{$_.DriveLetter} | select -Expand DriveLetter\"")
                for l in out2.split('\n'):
                    l = l.strip().upper()
                    if l and len(l) == 1:
                        lt = l + ':'
                        if lt not in letters:
                            letters.append(lt)
                disks.append({
                    'num': num,
                    'name': row[fi],
                    'style': row[pi],
                    'sig': row[si].upper() if row[si] else 'N/A',
                    'guid': row[gi].upper() if row[gi] else 'N/A',
                    'letters': ', '.join(letters) if letters else 'None'
                })
    except Exception as e:
        print('get_disks error:', e)
    return disks

def get_uuid():
    out, _, _ = run_cmd("powershell -C \"Get-CimInstance Win32_ComputerSystemProduct | select -Expand UUID\"")
    return out.upper() if out else 'N/A'

def gen_guid():
    parts = [8, 4, 4, 4, 12]
    return '-'.join([''.join(random.choices('0123456789ABCDEF', k=p)) for p in parts])

def get_mguid():
    out, _, _ = run_cmd("powershell -C \"Get-ItemProperty 'HKLM:\\SOFTWARE\\Microsoft\\Cryptography' MachineGuid -ErrorAction SilentlyContinue | select -Expand MachineGuid\"")
    return out.upper() if out else 'N/A'

def mac_changer():
    while True:
        header('MAC CHANGER')
        print('NOTE:    Modifies MAC address in registry and resets adapter.')
        print('         Adapter will briefly disconnect and reconnect.')
        print()
        print()
        adapters = get_adapters()
        if not adapters:
            print('No Ethernet adapters found')
            pause()
            break
        for i, a in enumerate(adapters, 1):
            print(str(i) + '. ' + str(a))
        print()
        print(red('0. BACK'))
        print()
        c = input('Choice: ')
        if c == '0':
            break
        try:
            idx = int(c) - 1
            if 0 <= idx < len(adapters):
                name = adapters[idx].split(' - ')[0]
                old = get_mac_addr(name)
                new = gen_mac()
                if not validate_mac(new):
                    error('Generated invalid MAC, retrying...')
                    time.sleep(1)
                    continue
                header('CHANGE MAC')
                print('Adapter:', adapters[idx])
                print('Old:', old)
                print('New:', new)
                backup('MAC Address', old, new)
                if input('\nApply? (y/n): ').lower() == 'y':
                    if set_mac(name, new):
                        success('MAC changed!')
                        note('Adapter was reset')
                        break
                    else:
                        error('Failed to change MAC')
                        pause()
            else:
                print(red('Invalid number'))
                time.sleep(0.5)
        except:
            print(red('Invalid input'))
            time.sleep(0.5)

def get_mac_addr(name):
    esc = name.replace("'", "''")
    out, _, _ = run_cmd("powershell -C \"Get-NetAdapter -Name '" + esc + "' | select -Expand MacAddress\"")
    return out or 'Error'

def gen_mac():
    m = [random.randint(0, 255) for _ in range(6)]
    m[0] = (m[0] & 0xFE) | 0x02
    return ':'.join('{:02X}'.format(x) for x in m)

def validate_mac(mac):
    clean = mac.replace(':', '').replace('-', '').upper()
    if len(clean) != 12:
        return False
    if not all(c in '0123456789ABCDEF' for c in clean):
        return False
    first_byte = int(clean[:2], 16)
    if first_byte & 0x01:
        return False
    return True

def set_mac(name, mac):
    clean = mac.replace(':', '')
    esc = name.replace("'", "''")
    ps = "$a=Get-NetAdapter -Name '" + esc + "' -ErrorAction SilentlyContinue;if($a){$guid=$a.InterfaceGuid;$base='HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}';Get-ChildItem $base -ErrorAction SilentlyContinue|%{$p=$_.PSPath;$ncid=Get-ItemPropertyValue $p NetCfgInstanceId -ErrorAction SilentlyContinue;if($ncid -eq $guid){Set-ItemProperty $p NetworkAddress '" + clean + "' -ErrorAction SilentlyContinue}};Disable-NetAdapter $a -Confirm:$false;Start-Sleep 3;Enable-NetAdapter $a -Confirm:$false;Write 'OK'}"
    tf = 'tmp_mac.ps1'
    try:
        with open(tf, 'w') as f:
            f.write(ps)
        out, _, rc = run_cmd('powershell -EP Bypass -F "' + tf + '"')
        return rc == 0 or 'OK' in out
    finally:
        try:
            os.remove(tf)
        except:
            pass

def hostname_spoofer():
    while True:
        header('HOSTNAME SPOOFER')
        print('NOTE:    Changes computer name. A restart is required.')
        print('         Network shares and domain membership may be affected.')
        print()
        print()
        out, _, _ = run_cmd("powershell -C \"(Get-ComputerInfo).CsName\"")
        print('Current:', out or 'Unknown')
        print()
        print('1. Random Name')
        print('2. Custom Name')
        print()
        print(red('0. BACK'))
        print()
        c = input('Choice: ')
        if c == '1':
            name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            header('CHANGE HOSTNAME')
            print('New:', name)
            if input('\nApply? (y/n): ').lower() == 'y':
                _, err, rc = run_cmd("powershell -C \"Rename-Computer -New '" + name + "' -Force\"")
                if rc == 0:
                    success('Hostname changed!')
                    note('Restart required')
                    break
                else:
                    error(err)
                    pause()
        elif c == '2':
            name = input('\nNew name: ')
            if name:
                header('CHANGE HOSTNAME')
                print('New:', name)
                if input('\nApply? (y/n): ').lower() == 'y':
                    esc = name.replace("'", "''")
                    _, err, rc = run_cmd("powershell -C \"Rename-Computer -New '" + esc + "' -Force\"")
                    if rc == 0:
                        success('Hostname changed!')
                        note('Restart required')
                        break
                    else:
                        error(err)
                        pause()
        elif c == '0':
            break

def mgid_spoofer():
    while True:
        header('MACHINE GUID')
        print('NOTE:    Changes the Machine GUID in Windows registry.')
        print('         Some software licenses are tied to this value.')
        print()
        print()
        cur = get_mguid()
        print('Current:', cur)
        print()
        print('1. Generate New GUID')
        print()
        print(red('0. BACK'))
        print()
        c = input('Choice: ')
        if c == '1':
            new = gen_guid()
            header('CHANGE GUID')
            print('Old:', cur)
            print('New:', new)
            backup('Machine GUID', cur, new)
            if input('\nApply? (y/n): ').lower() == 'y':
                _, err, rc = run_cmd("powershell -C \"Set-ItemProperty 'HKLM:\\SOFTWARE\\Microsoft\\Cryptography' MachineGuid '" + new + "' -Force\"")
                if rc == 0:
                    success('Machine GUID changed!')
                    note('Restart required')
                    break
                else:
                    error(err)
                    pause()
        elif c == '0':
            break

def uuid_spoofer():
    while True:
        header('SMBIOS UUID')
        print('NOTE:    Software-level only, firmware unchanged.')
        print('         Does not modify BIOS/UEFI firmware settings.')
        print()
        print()
        cur = get_uuid()
        print('Current:', cur)
        print()
        print('1. Generate New UUID')
        print()
        print(red('0. BACK'))
        print()
        c = input('Choice: ')
        if c == '1':
            new = gen_guid()
            header('CHANGE UUID')
            print('Old:', cur)
            print('New:', new)
            if input('\nApply? (y/n): ').lower() == 'y':
                ps = "$p='HKLM:\\HARDWARE\\DESCRIPTION\\System';if(-not(Test-Path $p)){New-Item $p -F|Out-Null};Set-ItemProperty $p SystemUuid '" + new + "' -Type String -Force"
                _, err, rc = run_cmd('powershell -C "' + ps + '"')
                if rc == 0:
                    success('UUID override applied!')
                    note('Restart required')
                    break
                else:
                    error(err)
                    pause()
        elif c == '0':
            break

def disk_changer():
    while True:
        header('DISK ID CHANGER')
        print('WARNING: Changing disk ID may cause boot failure!')
        print('         Ensure you have a backup before proceeding.')
        print()
        print('NOTE:    Antivirus may block this operation.')
        print('         Temporarily disable antivirus if you get Access Denied.')
        print()
        disks = get_disks()
        if not disks:
            print('No disks found')
            pause()
            break
        print('{:<3} {:<25} {:<6} {:<15} {}'.format('ID', 'Model', 'Type', 'Letters', 'ID'))
        print('-' * 85)
        for i, d in enumerate(disks, 1):
            cur = d['sig'] if d['style'] == 'MBR' else d['guid']
            lett = '[' + d['letters'] + ']'
            print('{:<3} {:<25} {:<6} {:<15} {}'.format(str(i), d['name'][:24], d['style'], lett, cur))
        print()
        print(red('0. BACK'))
        print()
        c = input('Choice: ')
        if c == '0':
            break
        try:
            idx = int(c) - 1
            if 0 <= idx < len(disks):
                d = disks[idx]
                header('CHANGE DISK ID')
                print('Disk: {} [{}]'.format(d['name'], d['letters']))
                print('Style:', d['style'])
                cur = d['sig'] if d['style'] == 'MBR' else d['guid']
                print('Current:', cur)
                if d['style'] == 'MBR':
                    new = ''.join(random.choices('0123456789ABCDEF', k=8))
                else:
                    new = gen_guid()
                print('New:', new)
                if 'C:' in d['letters']:
                    warning('You selected the system drive (C:)!')
                    warning('Changing its ID may prevent Windows from booting.')
                    print()
                backup('Disk ID', cur, new)
                if input('\nApply? (y/n): ').lower() == 'y':
                    if d['style'] == 'MBR':
                        _, err, rc = run_cmd("powershell -C \"Set-Disk -Number " + str(d['num']) + " -Signature 0x" + new + '"')
                    else:
                        rc, err = set_disk_guid(d['num'], new)
                    if rc == 0:
                        success('Disk ID changed!')
                        note('Restart required')
                        break
                    else:
                        error(err)
                        pause()
            else:
                print(red('Invalid number'))
                time.sleep(0.5)
        except Exception as e:
            print(red('Error: ' + str(e)))
            time.sleep(0.5)

def set_disk_guid(num, guid):
    clean = guid.strip('{}')
    ps = "$d=Get-Disk " + str(num) + ";$d|Set-Disk -Offline:$true -Confirm:$false;Start-Sleep 2;$d|Set-Disk -Guid '" + clean + "';Start-Sleep 1;$d|Set-Disk -Offline:$false -Confirm:$false;Write 'OK'"
    out, err, rc = run_cmd('powershell -C "' + ps + '"')
    if rc == 0 and 'OK' in out:
        return 0, ''
    if 'access' in out.lower() or 'access' in err.lower():
        return rc, 'ANTIVIRUS BLOCKING: Temporarily disable ALL antivirus (including Windows Defender real-time protection) and retry.'
    return rc, err or out

# ==========================================
# LINUX MOK SETUP FUNCTIONS
# ==========================================

def detect_distro():
    try:
        with open("/etc/os-release") as f:
            content = f.read().lower()
            if "arch" in content:
                return "arch"
            elif "kali" in content or "ubuntu" in content or "debian" in content:
                return "debian"
            elif "fedora" in content or "rhel" in content or "centos" in content:
                return "fedora"
    except:
        pass
    return "unknown"

def setup_debian():
    print("\n1. Installing required packages...")
    run_live_cmd("apt update && apt install -y mokutil sbsigntool openssl")
    print("\n2. Generating MOK key pair...")
    key_priv = "MOK.priv"
    key_der = "MOK.der"
    run_live_cmd(f'openssl req -new -x509 -newkey rsa:2048 -keyout {key_priv} -outform DER -out {key_der} -days 36500 -subj "/CN=Your MOK/" -nodes')
    print("\n3. Enrolling MOK public key (Enter a secure password when prompted)...")
    run_live_cmd(f"mokutil --import {key_der}")
    print("\n4. Next steps:")
    print("   a. Reboot your PC")
    print("   b. In the blue MOKManager screen, select 'Enroll MOK'")
    print("   c. Enter the password set in step 3")
    print("   d. Reboot again")

def setup_fedora():
    print("\n1. Installing required packages...")
    run_live_cmd("dnf install -y mokutil openssl")
    print("\n2. Generating MOK key pair with kmodgenca...")
    run_live_cmd("kmodgenca -a")
    run_live_cmd("mokutil --import /etc/pki/tls/certs/ca.crt")
    print("\n3. Next steps:")
    print("   a. Reboot your PC")
    print("   b. In the blue MOKManager screen, select 'Enroll MOK'")
    print("   c. Follow the instructions to enter the key")
    print("   d. Reboot again")

def setup_arch():
    print("\n1. Installing required packages...")
    run_live_cmd("pacman -Syu --noconfirm mokutil sbsigntool openssl")
    print("\n2. Generating MOK key pair...")
    run_live_cmd('openssl req -new -x509 -newkey rsa:2048 -keyout MOK.priv -outform DER -out MOK.der -days 36500 -subj "/CN=Your MOK/" -nodes')
    print("\n3. Enrolling MOK public key...")
    run_live_cmd("mokutil --import MOK.der")
    print("\n4. Next steps:")
    print("   a. Reboot your PC")
    print("   b. In the blue MOKManager screen, select 'Enroll MOK'")
    print("   c. Enter the password you set")
    print("   d. Reboot again")

def linux_mok_integration():
    header('LINUX MOK SETUP (SECURE BOOT)')
    if os.name == 'nt':
        print(yellow("SYSTEM STATUS: RUNNING ON WINDOWS"))
        print("-" * 50)
        print("This module is designed to configure the Linux Kernel.")
        print("Windows cannot access Linux kernel settings or BIOS MOK keys.")
        print()
        print(green("INSTRUCTIONS TO PROCEED:"))
        print(f"1. Copy this file ({os.path.basename(__file__)}) to a USB drive.")
        print("2. Reboot your PC and start your LINUX OS.")
        print("3. Open the Terminal in Linux.")
        print(f"4. Run: sudo python3 {os.path.basename(__file__)}")
        print("5. Select this option (2) again to start the auto-config.")
        print("-" * 50)
        print("PURPOSE: Enable Linux to boot safely with SECURE BOOT ENABLED.")
        pause()
    else:
        if os.geteuid() != 0:
            print(red("ERROR: Root privileges required!"))
            print(yellow(f"Please run: sudo python3 {os.path.basename(__file__)}"))
            pause()
            return
        print(green("SYSTEM STATUS: LINUX DETECTED (ROOT ACCESS CONFIRMED)"))
        print("This tool will now automate the Machine Owner Key (MOK) setup.")
        print()
        c = input('Do you want to start the MOK automation? (y/n): ')
        if c.lower() == 'y':
            distro = detect_distro()
            if distro == 'debian':
                setup_debian()
                success("MOK Setup Complete! Please REBOOT to finalize in BIOS.")
            elif distro == 'fedora':
                setup_fedora()
                success("MOK Setup Complete! Please REBOOT to finalize in BIOS.")
            elif distro == 'arch':
                setup_arch()
                success("MOK Setup Complete! Please REBOOT to finalize in BIOS.")
            else:
                error("Unsupported Distribution. This script supports Debian/Ubuntu or Fedora/RHEL.")
        else:
            print("\nOperation cancelled.")
        pause()

# ==========================================
# MAIN MENU
# ==========================================

def home():
    while True:
        header('Multi-Tools (Win/Linux)')
        if os.name == 'nt':
            print('1. HWID SPOOFER (Windows)')
        else:
            print(yellow('1. HWID SPOOFER (Not available on Linux)'))
        print('2. LINUX MOK SETUP (Secure Boot)')
        print()
        print(red('0. EXIT'))
        print()
        c = input('Choice: ')
        if c == '1':
            if os.name == 'nt':
                hwid_menu()
            else:
                print(red("\nHWID Spoofer only works on Windows!"))
                time.sleep(2)
        elif c == '2':
            linux_mok_integration()
        elif c == '0':
            break

def hwid_menu():
    while True:
        header('HWID SPOOFER')
        print('1. Ethernet MAC')
        print('2. Hostname')
        print('3. Disk ID')
        print('4. Machine GUID')
        print('5. SMBIOS UUID')
        print()
        print(red('0. BACK'))
        print()
        c = input('Choice: ')
        if c == '1':
            mac_changer()
        elif c == '2':
            hostname_spoofer()
        elif c == '3':
            disk_changer()
        elif c == '4':
            mgid_spoofer()
        elif c == '5':
            uuid_spoofer()
        elif c == '0':
            break

if __name__ == '__main__':
    if os.name == 'nt':
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, '"' + sys.argv[0] + '"', None, 1)
            sys.exit()
        try:
            folder = os.path.dirname(os.path.abspath(__file__))
            esc = folder.replace("'", "''")
            subprocess.run("powershell -C \"Add-MpPreference -ExclusionPath '" + esc + "';Add-MpPreference -ExclusionProcess '" + sys.executable.replace("'", "''") + "'\"", shell=True, capture_output=True)
        except Exception as e:
            pass
    else:
        if os.geteuid() != 0:
            print(red("\nERROR: You must run this script as Administrator on Linux."))
            print(yellow("Try using: sudo python3 " + os.path.basename(__file__) + "\n"))
            sys.exit(1)
    home()
