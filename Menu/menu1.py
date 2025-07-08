import subprocess
import threading
import speech_recognition as sr
import streamlit as st
import platform

st.set_page_config(page_title="Remote SSH Command Executor", layout="wide")

# SSH credentials
st.sidebar.title("🔧 SSH Configuration")
ip_address = st.sidebar.text_input("IP Address", value="192.168.103.91")
username = st.sidebar.text_input("Username", value="root")

# Command menu
menu = commands = {
    "1. Show date (date)": "date",
    "2. Show time (date +%T)": "date +%T",
    "3. List directory (ls -l)": "ls -l",
    "4. Current user (whoami)": "whoami",
    "5. System info (uname -a)": "uname -a",
    "6. Running tasks (top -b -n 1 | head -15)": "top -b -n 1 | head -15",
    "7. IP config (ip a)": "ip a",
    "8. Active connections (ss -tuln)": "ss -tuln",
    "9. ARP table (ip neigh)": "ip neigh",
    "10. All users (cut -d: -f1 /etc/passwd)": "cut -d: -f1 /etc/passwd",
    "11. Logged in users (who)": "who",
    "12. Environment variables (printenv)": "printenv",
    "13. List services (systemctl list-units --type=service --state=running)": "systemctl list-units --type=service --state=running",
    "14. Running processes (ps aux --sort=-%mem | head -10)": "ps aux --sort=-%mem | head -10",
    "15. Installed packages (dpkg -l | head -20 || rpm -qa | head -20)": "dpkg -l | head -20 || rpm -qa | head -20",
    "16. Battery status (acpi -b || echo 'No battery info')": "acpi -b || echo 'No battery info'",
    "17. Disk usage (df -h)": "df -h",
    "18. Startup programs (ls /etc/init.d/)": "ls /etc/init.d/",
    "19. BIOS info (dmidecode -t bios)": "dmidecode -t bios",
    "20. CPU info (lscpu)": "lscpu",
    "21. Memory info (free -h)": "free -h",
    "22. Motherboard info (dmidecode -t baseboard)": "dmidecode -t baseboard",
    "23. Network adapters (lshw -class network)": "lshw -class network",
    "24. Uptime (uptime)": "uptime",
    "25. Routing table (ip route)": "ip route",
    "26. Kernel version (uname -r)": "uname -r",
    "27. Last reboot time (who -b)": "who -b",
    "28. Check open ports (netstat -tuln)": "netstat -tuln",
    "29. Firewall status (ufw status || systemctl status firewalld)": "ufw status || systemctl status firewalld",
    "30. List USB devices (lsusb)": "lsusb",
    "31. List PCI devices (lspci)": "lspci",
    "32. Mounted file systems (mount | column -t)": "mount | column -t",
    "33. Recent system logs (journalctl -n 20)": "journalctl -n 20",
    "34. Authentication log (auth.log or secure)": "cat /var/log/auth.log | tail -n 20 || cat /var/log/secure | tail -n 20",
    "35. Failed login attempts (lastb | head -10)": "lastb | head -10",
    "36. Sudo usage log (grep sudo in auth.log)": "cat /var/log/auth.log | grep sudo || journalctl _COMM=sudo",
    "37. CPU temperature (sensors)": "sensors || echo 'sensors not available'",
    "38. Kernel messages (dmesg | tail -n 20)": "dmesg | tail -n 20",
    "39. Active timers (systemctl list-timers)": "systemctl list-timers",
    "40. Crontab entries (crontab -l)": "crontab -l",
    "41. Top memory apps (ps sorted by %mem)": "ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head -10",
    "42. Top CPU apps (ps sorted by %cpu)": "ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -10",
    "43. Swap usage (swapon --show)": "swapon --show",
    "44. Loaded kernel modules (lsmod)": "lsmod",
    "45. SELinux status (getenforce)": "getenforce || echo 'Not installed'",
    "46. AppArmor status (aa-status)": "aa-status || echo 'Not installed'",
    "47. Open files (lsof | head -20)": "lsof | head -20",
    "48. Hostname (hostname)": "hostname",
    "49. Timezone (timedatectl)": "timedatectl",
    "50. System boot time (uptime -s)": "uptime -s",

    # Docker Commands
    "51. Docker version": "docker --version",
    "52. List Docker containers (all)": "docker ps -a",
    "53. List running Docker containers": "docker ps",
    "54. List Docker images": "docker images",
    "55. Show Docker system info": "docker info",
    "56. Show Docker networks": "docker network ls",
    "57. Show Docker volumes": "docker volume ls",
    "58. Inspect a Docker container (docker inspect <container_id>)": "docker inspect CONTAINER_ID",
    "59. Start a Docker container (docker start <container_id>)": "docker start CONTAINER_ID",
    "60. Stop a Docker container (docker stop <container_id>)": "docker stop CONTAINER_ID"
}




# Only show these features if on Windows
if platform.system() == "Windows":
    st.sidebar.title("📱 Windows Features")

    st.sidebar.markdown("### 💬 Send WhatsApp Message")
    phone_number = st.sidebar.text_input("Phone Number (with +)", "+91")
    message = st.sidebar.text_area("Message", "Hello from Python!")
    if st.sidebar.button("Send WhatsApp Message"):
        try:
            import pywhatkit as kit
            kit.sendwhatmsg_instantly(phone_number, message)
            st.sidebar.success("Message sent!")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

    st.sidebar.markdown("---")

    st.sidebar.markdown("### 🔍 Google Search")
    search_query = st.sidebar.text_input("Search Query", "python")
    if st.sidebar.button("Search Now"):
        try:
            import pywhatkit as kit
            kit.search(search_query)
            st.sidebar.success("Search executed!")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

    st.sidebar.markdown("---")

    st.sidebar.markdown("### 📖 Wikipedia Scraper")
    wiki_url = st.sidebar.text_input("Wikipedia URL", "https://en.wikipedia.org/wiki/Hello_(Adele_song)")
    if st.sidebar.button("Scrape Wikipedia"):
        try:
            import requests
            from bs4 import BeautifulSoup
            response = requests.get(wiki_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(strip=True)
            st.text_area("Extracted Text", text[:1000], height=300)
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

    st.sidebar.markdown("---")

    st.sidebar.markdown("### 📸 Instagram Photo Upload")
    insta_username = st.sidebar.text_input("Instagram Username", "")
    insta_password = st.sidebar.text_input("Instagram Password", "", type="password")
    image_path = st.sidebar.text_input("Image Path", "gg.jpg")
    caption = st.sidebar.text_area("Caption", "Hello from Python! 🌟")

    if st.sidebar.button("Upload to Instagram"):
        try:
            from instagrapi import Client
            cl = Client()
            cl.login(insta_username, insta_password)
            cl.photo_upload(path=image_path, caption=caption)
            st.sidebar.success("Photo uploaded!")
        except Exception as e:
            st.sidebar.error(f"Instagram Error: {e}")


# Run SSH command
def run_remote_command(command):
    ssh_command = ["ssh", f"{username}@{ip_address}", command]
    try:
        result = subprocess.run(ssh_command, capture_output=True, text=True)
        stdout = result.stdout if result.stdout else "[!] No output."
        stderr = result.stderr if result.stderr else ""
        return stdout, stderr
    except Exception as e:
        return "", f"[!] Exception occurred: {e}"

# Voice input handling
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            return command
        except sr.UnknownValueError:
            return "[!] Could not understand audio."
        except sr.RequestError as e:
            return f"[!] Recognition error: {e}"

# Streamlit UI

st.title("🖥️ Remote Linux Command Executor via SSH")
st.markdown("---")

col1, col2 = st.columns([3, 1])

with col1:
    selected_command = st.selectbox("Choose a command to run:", list(menu.keys()))
    if st.button("Execute Selected Command"):
        with st.spinner("Running command..."):
            stdout, stderr = run_remote_command(menu[selected_command])
        st.code(stdout)
        if stderr:
            st.error(stderr)

with col2:
    st.markdown("#### 🎤 Voice Command")
    if st.button("Speak a command"):
        voice_text = listen_for_command()
        if voice_text.startswith("[!]"):
            st.warning(voice_text)
        else:
            matched = None
            for key in menu:
                if voice_text in key.lower():
                    matched = key
                    break
            if matched:
                st.success(f"Matched voice command: {matched}")
                with st.spinner("Running command..."):
                    stdout, stderr = run_remote_command(menu[matched])
                st.code(stdout)
                if stderr:
                    st.error(stderr)
            else:
                st.warning(f"Command '{voice_text}' not recognized.")

