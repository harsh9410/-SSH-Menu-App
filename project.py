import streamlit as st
import paramiko
import subprocess

# SSH connection
def ssh_connect(ip, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)
        st.session_state["ssh"] = ssh
        st.sidebar.success("SSH connected successfully.")
        return True
    except paramiko.AuthenticationException:
        st.sidebar.error("Authentication failed.")
    except paramiko.SSHException as e:
        st.sidebar.error(f"SSH error: {e}")
    except Exception as e:
        st.sidebar.error(f"Failed to connect: {e}")
    return False

def run_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode(), stderr.read().decode()

def ping_host(ip):
    try:
        result = subprocess.run(["ping", "-c", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception:
        return False

# Sidebar
st.sidebar.title("Remote Linux/Docker Login")
ip = st.sidebar.text_input("IP Address")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Test Connection"):
    if ping_host(ip):
        st.sidebar.success("Host is reachable.")
    else:
        st.sidebar.error("Host unreachable.")

if st.sidebar.button("Connect"):
    if not ip or not username or not password:
        st.sidebar.warning("Please fill in all fields.")
    else:
        ssh_connect(ip, username, password)

# Tabs
tabs = st.tabs(["Home", "Linux Commands", "Docker Commands"])

# Home
with tabs[0]:
    st.title("Streamlit Dashboard")
    st.markdown("""
Connect via SSH, run Linux & Docker commands, and use an ML job prediction model.
""")

# Linux Commands
with tabs[1]:
    st.header("Linux Commands")
    if "ssh" in st.session_state:
        ssh = st.session_state["ssh"]

        linux_commands = {
            "1. Date": "date",
            "2. Cal": "cal",
            "3. Ifconfig": "ifconfig",
            "4. List Files (ls)": "ls",
            "5. Show Hostname": "hostname",
            "6. Current User": "whoami",
            "7. System Uptime": "uptime",
            "8. Memory Usage": "free -m",
            "9. View Processes": "ps aux",
            "10. Real-time Monitor": "top -b -n 1",
            "11. Disk Usage": "df -h",
            "12. OS & Kernel Info": "uname -a",
            "13. View /etc/shadow": "cat /etc/shadow",
            "14. View /etc/passwd": "cat /etc/passwd",
            "15. View /etc/group": "cat /etc/group"
        }

        selected_command = st.selectbox("Choose Linux Command", list(linux_commands.keys()))
        if st.button("Run Linux Command"):
            out, err = run_command(ssh, linux_commands[selected_command])
            if out:
                st.code(out)
            elif err:
                st.error(err)
            else:
                st.success("Command executed successfully.")

        st.subheader("Run Custom Linux Command")
        custom_cmd = st.text_input("Enter custom Linux command")
        if st.button("Run Custom Command"):
            out, err = run_command(ssh, custom_cmd)
            if out:
                st.code(out)
            elif err:
                st.error(err)
            else:
                st.success("Command executed successfully.")
    else:
        st.warning("Please connect via SSH from the sidebar first.")

# Docker Commands
with tabs[2]:
    st.header("Docker Commands")
    if "ssh" in st.session_state:
        ssh = st.session_state["ssh"]

        docker_commands = {
            "16. Show Docker Version": "docker --version",
            "17. Docker Info": "docker info",
            "18. List All Containers": "docker ps -a",
            "24. List Docker Images": "docker images",
            "27. Remove All Containers": "docker rm $(docker ps -a -q)"
        }

        selected_docker = st.selectbox("Choose Docker Command", list(docker_commands.keys()))
        if st.button("Run Docker Command"):
            out, err = run_command(ssh, docker_commands[selected_docker])
            if out:
                st.code(out)
            elif err:
                st.error(err)
            else:
                st.success("Command executed successfully.")

        st.subheader("Docker Actions")

        image = st.text_input("Docker image to run (e.g. ubuntu)")
        if st.button("19. Run New Container"):
            if image:
                out, err = run_command(ssh, f"docker run -dit {image}")
                st.code(out)
            else:
                st.warning("Enter image name.")

        cid = st.text_input("Container ID or Name")

        if st.button("20. Start Container"):
            out, err = run_command(ssh, f"docker start {cid}")
            st.code(out)
        if st.button("21. Attach to Container"):
            out, err = run_command(ssh, f"docker attach {cid}")
            st.code(out)
        if st.button("22. Stop Container"):
            out, err = run_command(ssh, f"docker stop {cid}")
            st.code(out)
        if st.button("23. Remove Container"):
            out, err = run_command(ssh, f"docker rm {cid}")
            st.code(out)

        pull_image = st.text_input("Image name to pull")
        if st.button("25. Pull Docker Image"):
            out, err = run_command(ssh, f"docker pull {pull_image}")
            st.code(out)

        remove_image = st.text_input("Image name or ID to remove")
        if st.button("26. Remove Docker Image"):
            out, err = run_command(ssh, f"docker rmi {remove_image}")
            st.code(out)
    else:
        st.warning("Please connect via SSH from the sidebar first.")

