try:
    from instagrapi import Client
    from instagrapi.types import Story
    import time
    import random
    import getpass
    import os
    import json
    from datetime import datetime
    from pathlib import Path
    import shutil
    import tempfile
    import subprocess
    import ctypes
    import sys
    from urllib.parse import unquote
except ImportError as e:
    import sys
    print(f"❌ Import error: {e}")
    print("Make sure you installed: pip install instagrapi")
    input("Press ENTER to exit...")
    sys.exit(1)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate_to_admin():
    if os.name != 'nt':
        return False
    if is_admin():
        return True
    print("🔒 Requesting administrator privileges for network operations...")
    try:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([f'"{arg}"' if ' ' in arg else arg for arg in sys.argv[1:]])
        ret = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script}"', None, 1
        )
        if ret > 32:
            return True
        else:
            print("❌ User denied UAC elevation or elevation failed")
            return False
    except Exception as e:
        print(f"❌ Failed to elevate privileges: {e}")
        return False

if os.name == 'nt' and not is_admin():
    print("   ⚠️ NOT RUNNING AS ADMINISTRATOR")
    print("   Requesting administrator privileges for MAC address rotation...")
    if elevate_to_admin():
        sys.exit(0)
    else:
        print("   Failed to get admin privileges. MAC rotation will be skipped.")
        time.sleep(2)

def randomize_process_name():
    return True

def stealth_sleep(base_time):
    jitter = random.uniform(0.8, 1.2)
    actual_time = base_time * jitter
    time.sleep(actual_time)
    return actual_time

def get_active_network_adapter():
    try:
        ps_cmd = "Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | Select-Object -First 1 -ExpandProperty Name"
        result = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True, check=True)
        adapter_name = result.stdout.strip()
        if not adapter_name:
            raise Exception("No active network adapter found")
        return adapter_name
    except Exception as e:
        print(f"⚠️ Failed to get active network adapter: {e}")
        return None

def generate_random_mac():
    first_byte = random.randint(0, 255) & 0xFE
    mac_bytes = [first_byte] + [random.randint(0, 255) for _ in range(5)]
    return ''.join(f'{b:02X}' for b in mac_bytes)

def change_mac_address():
    if os.name != 'nt':
        print("⚠️ MAC address change is only supported on Windows")
        return False
    if not is_admin():
        print("⚠️ MAC address change requires Administrator privileges. Skipping...")
        return False
    print("🔄 Attempting to change MAC address of network adapter...")
    adapter = get_active_network_adapter()
    if not adapter:
        print("❌ No active network adapter found, skipping MAC change")
        return False
    new_mac = generate_random_mac()
    print(f"📡 Active adapter: {adapter}, New MAC: {new_mac}")
    try:
        ps_cmd = f'Set-NetAdapterAdvancedProperty -Name "{adapter}" -RegistryKeyword "NetworkAddress" -RegistryValue "{new_mac}" -ErrorAction Stop'
        subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True, check=True)
        restart_cmd = f'Restart-NetAdapter -Name "{adapter}" -ErrorAction Stop'
        subprocess.run(["powershell", "-Command", restart_cmd], capture_output=True, text=True, check=True)
        print(f"✅ MAC address changed successfully to {new_mac}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to change MAC address: {e.stderr.strip()}")
        return False
    except Exception as e:
        print(f"❌ Error changing MAC address: {e}")
        return False

def clear_temp_files():
    print("🧹 Clearing bot temporary files...")
    temp_dirs = [
        str(BOT_DATA_DIR / "temp"),
        str(Path.home() / ".insta-botter" / "temp"),
    ]
    for temp_dir in temp_dirs:
        if not os.path.exists(temp_dir):
            continue
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass
    BOT_DATA_DIR.mkdir(exist_ok=True)
    print("✅ Bot temporary files cleared")

BOT_DATA_DIR = Path.home() / ".insta-botter"
SESSION_FILE = str(BOT_DATA_DIR / "instagram_session.json")
TRACKING_FILE = str(BOT_DATA_DIR / "follow_tracking.json")
USER_TRACKING_FILE = str(BOT_DATA_DIR / "user_tracking.json")
FOLDER_META_FILE = str(BOT_DATA_DIR / "folder_meta.json")

DEVICE_SETTINGS = {
    "app_version": "340.0.0.23.111",
    "ios_version": "17.4.1",
    "ios_release": "17.4.1",
    "dpi": "3.00",
    "resolution": "1179x2556",
    "manufacturer": "Apple",
    "device": "iPhone 14 Pro",
    "model": "iPhone 14 Pro",
    "cpu": "arm64",
    "version_code": "473485148",
    "user_agent": "Instagram 340.0.0.23.111 iPhone (iPhone 14 Pro; iOS 17_4_1; en_US; en-US; scale=3.00; 1179x2556; 473485148)"
}

def clear_screen():
    subprocess.run(['cls' if os.name == 'nt' else 'clear'], shell=True)

def delete_folder_permanently(path):
    try:
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
            if os.name == 'nt':
                try:
                    ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x0007)
                except:
                    pass
            print(f"🗑️ Permanently deleted: {path}")
    except Exception as e:
        print(f"⚠️ Error deleting folder: {e}")

def init_bot_data_dir(current_username=None, keep_session=False):
    global BOT_DATA_DIR, SESSION_FILE, TRACKING_FILE, USER_TRACKING_FILE, FOLDER_META_FILE
    BOT_DATA_DIR.mkdir(exist_ok=True)
    now = time.time()
    should_reset = False
    reason = ""
    if os.path.exists(FOLDER_META_FILE):
        try:
            with open(FOLDER_META_FILE, "r") as f:
                meta = json.load(f)
            created_time = meta.get("created_time", now)
            if now - created_time > 172800:
                should_reset = True
                reason = "48h folder age limit reached"
        except Exception:
            should_reset = True
            reason = "Corrupted meta file"
    else:
        should_reset = True
        reason = "First run or meta file missing"
    if not should_reset and current_username:
        try:
            with open(USER_TRACKING_FILE, "r") as f:
                user_data = json.load(f)
            last_user = user_data.get("last_username", "")
            if last_user and last_user != current_username:
                should_reset = True
                reason = f"Different user detected (was: {last_user}, now: {current_username})"
        except Exception:
            pass
    if should_reset:
        print("┌" + "─"*36 + "┐")
        print("│" + " "*6 + "🔄 RESETTING BOT DATA 🔄" + " "*6 + "│")
        print("└" + "─"*36 + "┘")
        print(f"   Reason: {reason}")
        if keep_session and os.path.exists(SESSION_FILE):
            import shutil
            temp_session = SESSION_FILE + ".tmp"
            shutil.copy2(SESSION_FILE, temp_session)
            delete_folder_permanently(str(BOT_DATA_DIR))
            BOT_DATA_DIR.mkdir(exist_ok=True)
            shutil.move(temp_session, SESSION_FILE)
        else:
            delete_folder_permanently(str(BOT_DATA_DIR))
            BOT_DATA_DIR.mkdir(exist_ok=True)
        meta = {"created_time": now, "created_date": str(datetime.now())}
        with open(FOLDER_META_FILE, "w") as f:
            json.dump(meta, f, indent=2)
        print("   ✅ Bot data reset complete!")
    if current_username:
        user_data = {"last_username": current_username, "last_login": str(datetime.now())}
        with open(USER_TRACKING_FILE, "w") as f:
            json.dump(user_data, f, indent=2)
    BOT_DATA_DIR.mkdir(exist_ok=True)

def wait_with_stop(delay):
    for _ in range(delay):
        time.sleep(1)
        if os.name == 'nt':
            try:
                import msvcrt
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key == b'0':
                        return "exit"
                    elif key in (b'\r', b'\n'):
                        return "menu"
            except ImportError:
                pass
        else:
            try:
                import select
                import sys
                if select.select([sys.stdin], [], [], 0)[0]:
                    key = sys.stdin.read(1)
                    if key == '0':
                        return "exit"
                    elif key in ('\r', '\n'):
                        return "menu"
            except (ImportError, OSError):
                pass
    return None

def press_to_continue():
    print("\nPress ENTER to return to menu or 0 to EXIT program...")
    choice = input("> ").strip()
    if choice == "0":
        return "exit"
    return "menu"

def load_tracking():
    if os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, "r") as f:
            data = json.load(f)
            if "followed" not in data:
                data["followed"] = []
            return data
    return {"followed": []}

def save_tracking(data):
    with open(TRACKING_FILE, "w") as f:
        json.dump(data, f, indent=2)

def save_follow(tracking, user_id, username):
    if any(e["user_id"] == user_id and not e["unfollowed"] for e in tracking["followed"]):
        return
    tracking["followed"].append({
        "user_id": user_id,
        "username": username,
        "followed_at": str(datetime.now()),
        "unfollowed": False
    })
    save_tracking(tracking)

def simulate_human_activity(cl, user_id, username):
    try:
        if random.random() < 0.7:
            try:
                user_medias = cl.user_medias(user_id, amount=2)
                if user_medias:
                    num_likes = random.randint(1, min(2, len(user_medias)))
                    for i in range(num_likes):
                        try:
                            cl.media_like(user_medias[i].id)
                            print(f"❤️ Liked a post from @{username}")
                            stealth_sleep(random.uniform(1, 3))
                        except:
                            pass
            except:
                pass
        if random.random() < 0.5:
            try:
                stories = cl.user_stories(user_id)
                if stories:
                    story_ids = [s.id for s in stories[:3]]
                    cl.story_seen(story_ids, user_id)
                    print(f"👁️ Viewed stories from @{username}")
                    stealth_sleep(random.uniform(1, 2))
            except:
                pass
    except Exception:
        pass

def scroll_feed(cl):
    try:
        print("📱 Scrolling feed...")
        feed = cl.feed_posts(amount=5)
        for post in feed:
            stealth_sleep(random.uniform(2, 4))
        print("✅ Feed scroll done")
    except:
        pass

def simulate_explore(cl, target_hashtag):
    try:
        print("🔍 Simulating Explore section browsing...")
        related_tags = cl.hashtag_related(target_hashtag)
        if related_tags:
            num_tags = random.randint(1, 2)
            tags_to_browse = random.sample(related_tags, min(num_tags, len(related_tags)))
            for tag in tags_to_browse:
                try:
                    cl.hashtag_info(tag.name)
                    print(f"👀 Browsed related hashtag: #{tag.name}")
                    stealth_sleep(random.uniform(2, 4))
                except Exception:
                    pass
        print("✅ Explore simulation completed")
        stealth_sleep(random.uniform(1, 2))
    except Exception:
        pass

def simulate_notification_check(cl):
    if random.random() < 0.3:
        try:
            print("🔔 Checking notifications...")
            cl.account_notifications()
            print("✅ Notifications checked")
            stealth_sleep(random.uniform(1, 3))
        except Exception:
            pass

def show_menu(logged_in=True):
    valid_choices = ["0", "1", "2", "3", "4"]
    if not logged_in:
        valid_choices.append("5")
    while True:
        clear_screen()
        print()
        print("=" * 50)
        print("           INSTA-BOTTER - MAIN MENU")
        print("=" * 50)
        print()
        print("  1. Start Hashtag Follower Bot")
        print("  2. Check and Unfollow ALL followed")
        print("  3. Info / Safety")
        print("  4. Exit from account")
        if not logged_in:
            print("  5. Login with Cookies")
        print()
        print("  0. EXIT PROGRAM")
        print()
        print("-" * 50)
        print()
        choice = input("  Choose (0-5): ").strip()
        if choice in valid_choices:
            return choice
        print()
        print("  ❌ Invalid option! Try again.")
        time.sleep(2)

def check_unfollow_all(cl, tracking, start_time):
    clear_screen()
    print("\n🔍 Unfollowing ALL users followed by bot...")
    try:
        users_to_unfollow = [e for e in tracking["followed"] if not e["unfollowed"]]
        if not users_to_unfollow:
            print("\n❌ No users to unfollow. You haven't followed anyone yet!")
            if press_to_continue() == "exit":
                sys.exit(0)
            clear_screen()
            return
        unfollow_count = 0
        for entry in tracking["followed"]:
            if time.monotonic() - start_time > 27000:
                print("\n⏰ Max 7.5h runtime reached. Stopping unfollow...")
                break
            if entry["unfollowed"]:
                continue
            user_id = entry["user_id"]
            try:
                print(f"\n👉 Unfollow: @{entry['username']}")
                cl.user_unfollow(user_id)
                entry["unfollowed"] = True
                unfollow_count += 1
                delay = random.randint(15, 25)
                print(f"⏳ Waiting {delay}s before next unfollow... (Press ENTER for menu, 0 to exit)")
                result = wait_with_stop(delay)
                if result == "exit":
                    print("\n👋 Closing bot. Bye!")
                    sys.exit(0)
                elif result == "menu":
                    break
            except Exception as e:
                print(f"❌ Unfollow error: {e}")
                print("⏳ Waiting 30s before retrying...")
                stealth_sleep(30)
        save_tracking(tracking)
        print(f"\n🏁 Unfollow completed: {unfollow_count} users")
        if press_to_continue() == "exit":
            sys.exit(0)
        clear_screen()
    except Exception as e:
        print(f"\n💥 Error: {e}")
        if press_to_continue() == "exit":
            sys.exit(0)
        clear_screen()

def start_bot(cl, start_time):
    clear_screen()
    while True:
        hashtag_target = input("\n👉 Enter hashtag (without #): ").strip()
        if hashtag_target:
            break
        print("\n❌ Hashtag cannot be empty! Try again.")
        time.sleep(1)
        clear_screen()
    tracking = load_tracking()
    simulate_explore(cl, hashtag_target)
    print(f"\n🔍 Searching posts with #{hashtag_target}...")
    try:
        medias = cl.hashtag_medias_recent(hashtag_target, amount=100)
        if not medias:
            print(f"\n❌ No recent posts found for #{hashtag_target}")
            if press_to_continue() == "exit":
                sys.exit(0)
            clear_screen()
            return
        counter = 0
        feed_scroll_counter = 0
        stopped = False
        for media in medias:
            if time.monotonic() - start_time > 27000:
                print("\n⏰ Max 7.5h runtime reached. Stopping follow bot...")
                stopped = True
                break
            if stopped:
                break
            user_id = media.user.pk
            username_target = media.user.username
            if any(e["user_id"] == user_id and not e["unfollowed"] for e in tracking["followed"]):
                continue
            try:
                simulate_notification_check(cl)
                simulate_human_activity(cl, user_id, username_target)
                print(f"\n👉 Follow: @{username_target}")
                cl.user_follow(user_id)
                counter += 1
                save_follow(tracking, user_id, username_target)
                print(f"✨ Success! Total followed: {counter}")
                delay = random.choice([15, 30, 40, 60, 120])
                feed_scroll_counter += 1
                if feed_scroll_counter % random.randint(5, 10) == 0:
                    scroll_feed(cl)
                    simulate_notification_check(cl)
                print(f"⏳ Waiting {delay}s before next follow... (Press ENTER for menu, 0 to exit)")
                result = wait_with_stop(delay)
                if result == "exit":
                    print("\n👋 Closing bot. Bye!")
                    sys.exit(0)
                elif result == "menu":
                    stopped = True
            except Exception as e:
                print(f"❌ Error following @{username_target}: {e}")
                print("⏳ Waiting 30s before retrying...")
                stealth_sleep(30)
        if stopped:
            print(f"\n🛑 Stopped! Followed {counter} users.")
            clear_screen()
            return "stopped"
        else:
            print(f"\n🏁 Done! Followed {counter} users.")
        if press_to_continue() == "exit":
            sys.exit(0)
        clear_screen()
    except Exception as e:
        error_str = str(e)
        print(f"\n💥 Error: {e}")
        if "login_required" in error_str.lower():
            print("\n⚠️ Session expired! Please re-login.")
            if os.path.exists(SESSION_FILE):
                try:
                    os.remove(SESSION_FILE)
                except:
                    pass
            stealth_sleep(2)
            clear_screen()
            return "session_expired"
        print("⏳ Waiting 30s before retrying...")
        stealth_sleep(30)
        if press_to_continue() == "exit":
            sys.exit(0)
        clear_screen()

def logout_account(cl):
    try:
        cl.logout()
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        print("\n✅ Logged out successfully!")
        if press_to_continue() == "exit":
            sys.exit(0)
        clear_screen()
        return True
    except Exception as e:
        print(f"\n❌ Logout error: {e}")
        if press_to_continue() == "exit":
            sys.exit(0)
        clear_screen()
        return False

def challenge_code_handler(username, choice=None):
    while True:
        print(f"\n🔐 Instagram requires verification for @{username}")
        print("Choices:")
        print("1. Email verification")
        print("2. SMS verification")
        print("3. Enter 2FA code")
        choice = input("Select verification method (1-3): ").strip()
        if choice == "1":
            print("Check your email for the verification code.")
            code = input("Enter email verification code: ").strip()
            if code:
                return code
        elif choice == "2":
            print("Check your phone for the verification code.")
            code = input("Enter SMS verification code: ").strip()
            if code:
                return code
        elif choice == "3":
            code = input("Enter 2FA code: ").strip()
            if code:
                return code
        print("❌ Invalid choice or empty code. Please try again.")

def login_with_cookies(cl, username):
    clear_screen()
    print("\n" + "="*40)
    print("COOKIE-BASED LOGIN")
    print("="*40)
    print()
    print("How to get cookies:")
    print("1. Open Chrome/Edge -> https://instagram.com")
    print("2. Log in manually")
    print("3. Press F12 -> Application -> Cookies -> https://www.instagram.com")
    print("4. Copy values of 'sessionid' and 'csrftoken' cookies")
    print()
    sessionid = input("Enter sessionid cookie value: ").strip()
    print()
    csrftoken = input("Enter csrftoken cookie value: ").strip()
    print()

    if not sessionid or not csrftoken:
        print("❌ Both sessionid and csrftoken are required!")
        time.sleep(2)
        return False, None

    sessionid = unquote(sessionid)

    try:
        cl.login_by_sessionid(sessionid)
        cl.dump_settings(SESSION_FILE)
        user_info = cl.account_info()
        actual_username = user_info.username

        if actual_username != username:
            print(f"⚠️ Warning: logged in as @{actual_username}, but you entered @{username}")

        print(f"\n✅ Cookie login successful for @{actual_username}!")
        time.sleep(1)
        return True, actual_username

    except Exception as e:
        print(f"\n❌ Cookie login failed: {e}")
        time.sleep(2)
        return False, None

def do_login(existing_client=None):
    cl = existing_client if existing_client else Client()
    if not existing_client:
        cl.challenge_code_handler = challenge_code_handler

    username = None

    if os.path.exists(SESSION_FILE) and not existing_client:
        try:
            print("🔄 Trying to restore previous session...")
            cl.load_settings(SESSION_FILE)
            user_info = cl.account_info()
            username = user_info.username
            init_bot_data_dir(username, keep_session=True)
            print(f"✅ Session restored for @{username}")
            time.sleep(1)
            clear_screen()
            return cl, username
        except Exception as e:
            print(f"⚠️ Session restore failed: {e}")
            if os.path.exists(SESSION_FILE):
                try:
                    os.remove(SESSION_FILE)
                    print("🗑️ Removed invalid session file")
                except Exception:
                    pass

    clear_screen()
    print()
    print("=" * 50)
    print("           INSTAGRAM LOGIN")
    print("=" * 50)
    print()
    print("  TIP: Verify your account at https://instagram.com")
    print("       before using this tool.")
    print()
    print("-" * 50)
    print()

    username = input("  Username: ").strip()
    while not username:
        print()
        print("  ❌ Username cannot be empty!")
        print()
        username = input("  Username: ").strip()

    print()
    password = getpass.getpass("  Password: ")
    while not password:
        print()
        print("  ❌ Password cannot be empty!")
        print()
        password = getpass.getpass("  Password: ")

    print()
    print("-" * 50)
    print()

    try:
        init_bot_data_dir(username)
        print("  🔑 Logging in as @" + username + "...")
        print()
        cl.login(username, password)
        cl.dump_settings(SESSION_FILE)
        print("  ✅ Login successful for @" + username + "!")
        stealth_sleep(2)
        clear_screen()
        return cl, username

    except Exception as e:
        print()
        print("  💥 Login failed: " + str(e))
        print()
        print("  Trying cookie login instead...")
        time.sleep(1)

        cl2 = Client()
        cl2.challenge_code_handler = challenge_code_handler
        success, actual_username = login_with_cookies(cl2, username)
        if success:
            username = actual_username if actual_username else username
            init_bot_data_dir(username)
            cl2.dump_settings(SESSION_FILE)
            print()
            print("  ✅ Cookie login successful for @" + username + "!")
            stealth_sleep(2)
            clear_screen()
            return cl2, username
        else:
            print()
            print("  ❌ All login methods failed.")
            time.sleep(2)
            clear_screen()
            return None, None

def main():
    print()
    print("=" * 50)
    print("        INSTA-BOTTER v1.1 - STARTING")
    print("=" * 50)
    print()
    print("  Running startup tasks...")
    print()
    randomize_process_name()
    change_mac_address()
    clear_temp_files()
    clear_screen()
    start_time = time.monotonic()
    cl, username = do_login()
    if not cl or not username:
        print()
        input("  Press ENTER to exit...")
        sys.exit(1)
    while True:
        if time.monotonic() - start_time > 27000:
            clear_screen()
            print()
            print("=" * 50)
            print("        RUNTIME LIMIT REACHED")
            print("=" * 50)
            print()
            print("  Max 7.5 hours reached!")
            print()
            print("  1. Exit bot")
            print("  2. Restart with new session (new MAC + cleanup)")
            print()
            while True:
                restart = input("  Choose (1-2): ").strip()
                if restart in ("1", "2"):
                    break
                print("  ❌ Invalid option! Try again.")
                time.sleep(1)
            if restart == "2":
                print()
                print("  🔄 Restarting with fresh session...")
                stealth_sleep(2)
                os.execv(sys.executable, [sys.executable] + sys.argv)
                return
            else:
                print()
                print("  👋 Closing bot. Bye!")
                break
        choice = show_menu(logged_in=bool(username))
        if choice == "1":
            result = start_bot(cl, start_time)
            if result == "session_expired":
                print("\n⚠️ Session expired! Re-logging in...")
                cl, username = do_login()
                if not cl:
                    input("\nPress ENTER to exit...")
                    sys.exit(1)
                clear_screen()
        elif choice == "2":
            tracking = load_tracking()
            check_unfollow_all(cl, tracking, start_time)
        elif choice == "3":
            clear_screen()
            print("\nSAFETY INFO\n")
            print("- Human-like activity: likes, story views")
            print("- Random delays: 15-120s between follows")
            print("- Unfollow ALL users via option 2")
            print("- Tracking saved to file")
            print("- Device: iPhone 14 Pro")
            print("- Max runtime: 7.5 hours\n")
            print("LOGIN INFO\n")
            print("- Verify account in browser first")
            print("- Cookie login = most reliable\n")
            print("WARNING: Use at your own risk\n")
            choice = input("Press ENTER to return to menu or 0 to exit: ").strip()
            if choice == "0":
                print("Closing bot. Bye!")
                sys.exit(0)
            clear_screen()
        elif choice == "4":
            logout_account(cl)
            cl, username = do_login()
            if not cl:
                input("\nPress ENTER to exit...")
                sys.exit(1)
            clear_screen()
        elif choice == "5":
            print("\n" + "="*40)
            print("COOKIE LOGIN")
            print("="*40)
            print()
            
            username_input = input("Username: ").strip()
            while not username_input:
                print("❌ Username cannot be empty!")
                username_input = input("Username: ").strip()
            
            print()
            
            cl = Client()
            cl.challenge_code_handler = challenge_code_handler
            success, actual_username = login_with_cookies(cl, username_input)
            if success:
                username = actual_username if actual_username else username_input
                print(f"\n✅ Logged in as @{username}!")
                init_bot_data_dir(username)
                stealth_sleep(2)
            else:
                print("\n❌ Cookie login failed.")
            
            if press_to_continue() == "exit":
                sys.exit(0)
            clear_screen()
        elif choice == "0":
            print("\n👋 Closing bot. Bye!")
            break
        else:
            print("\n❌ Invalid option! Try again.")
            stealth_sleep(2)
            clear_screen()

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code != 0:
            print(f"\nScript exited with code: {e.code}")
    except Exception as e:
        print(f"\n💥 Critical error: {e}")
        import traceback
        traceback.print_exc()
    except:
        print("\n💥 Unknown error occurred!")
        import traceback
        traceback.print_exc()
    finally:
        print("\n" + "="*40)
        print("Script ended. Window will stay open.")
        print("="*40)
        input("Press ENTER to close...")
