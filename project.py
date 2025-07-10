import streamlit as st
import paramiko
import time
import os
import base64
import subprocess
import datetime
import pyautogui
import pywhatkit
from gtts import gTTS
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

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
tabs = st.tabs(["Home", "Linux Commands", "Docker Commands", "Job Prediction App" ,"Automation App"])

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

# Job Prediction Tab
with tabs[3]:
    st.header("Job Selection Prediction App")
    try:
        data = pd.read_csv("dataset.csv")

        le_qualification = LabelEncoder()
        le_internship = LabelEncoder()
        le_referral = LabelEncoder()
        le_result = LabelEncoder()

        data["Qualification"] = le_qualification.fit_transform(data["Qualification"])
        data["Internship"] = le_internship.fit_transform(data["Internship"])
        data["Referral"] = le_referral.fit_transform(data["Referral"])
        data["Job_Result"] = le_result.fit_transform(data["Job_Result"])

        x = data[[
            "Qualification", "Internship", "Comm_Skill", "Tech_Skill_Level",
            "Certifications", "Interview_Score", "Resume_Score", "Referral"
        ]]
        y = data["Job_Result"]

        model = LinearRegression()
        model.fit(x, y)

        st.subheader("Candidate Information")
        qualification = st.selectbox("Qualification", le_qualification.classes_.tolist())
        internship = st.selectbox("Internship", le_internship.classes_.tolist())
        referral = st.selectbox("Referral", le_referral.classes_.tolist())
        comm_skill = st.number_input("Communication Skill", min_value=0)
        tech_skill = st.number_input("Technical Skill Level", min_value=0)
        certifications = st.number_input("Certifications", min_value=0)
        interview_score = st.number_input("Interview Score", min_value=0)
        resume_score = st.number_input("Resume Score", min_value=0)

        if st.button("Predict Job Result"):
            q = le_qualification.transform([qualification])[0]
            i = le_internship.transform([internship])[0]
            r = le_referral.transform([referral])[0]

            input_data = [[
                q, i, comm_skill, tech_skill,
                certifications, interview_score, resume_score, r
            ]]

            prediction = model.predict(input_data)[0]
            result_label = le_result.inverse_transform([int(round(prediction))])[0]

            if "Not Selected" in result_label:
                st.error(f"Predicted Result: {result_label}")
            elif "Selected" in result_label:
                st.success(f"Predicted Result: {result_label}")
            else:
                st.info(f"Predicted Result: {result_label}")
    except Exception as e:
        st.error(f"Error loading dataset or model: {e}")

        # Automation App
with tabs[4]:
    st.header("🤖 Automation Web App")
    st.markdown("Choose an action: Date, Calendar or WhatsApp")

    def speak(text):
        tts = gTTS(text)
        tts.save("speak.mp3")
        with open("speak.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            audio_html = f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
        os.remove("speak.mp3")

    def extract_number(text):
        words_to_digits = {
            "one": 1, "two": 2, "three": 3, "four": 4,
            "five": 5, "six": 6, "seven": 7,
            "eight": 8, "nine": 9, "ten": 10
        }
        if text.isdigit():
            return int(text)
        return words_to_digits.get(text.lower(), 1)

    choice = st.selectbox("What do you want to do?", ["--Select--", "Date", "Calendar", "WhatsApp"])

    if choice == "Date":
        current_date = datetime.date.today()
        st.success(f"📅 Today's Date: {current_date}")
        speak(f"Today's date is {current_date}")

    elif choice == "Calendar":
        try:
            output = os.popen("cal").read()
            st.text(f"📆 Calendar:\n{output}")
            speak("Showing calendar")
        except Exception as e:
            st.error("Could not display calendar.")
            st.text(str(e))

    elif choice == "WhatsApp":
        st.info("📲 This will open WhatsApp Web and send your message")

        number = st.text_input("Enter mobile number with country code", value="+91")
        message = st.text_input("Enter the message to send")
        repeat_count_text = st.text_input("How many times should I send the message?", value="1")

        if st.button("Send WhatsApp Message"):
            if number.strip() and message.strip():
                repeat_count = extract_number(repeat_count_text)
                if repeat_count < 1:
                    repeat_count = 1

                try:
                    speak("Opening WhatsApp Web")
                    st.success("Opening WhatsApp Web... Please scan the QR code if needed.")

                    pywhatkit.sendwhatmsg_instantly(number, "Hi", wait_time=15, tab_close=False)
                    speak("WhatsApp Web opened. Sending your message now")

                    time.sleep(20)  # Let WhatsApp Web load properly

                    for i in range(repeat_count):
                        pyautogui.write(message)
                        pyautogui.press("enter")
                        time.sleep(0.5)

                    st.success(f"✅ Message sent {repeat_count} times successfully!")
                    speak(f"Message sent {repeat_count} times")

                except Exception as e:
                    st.error(f"❌ Failed to send WhatsApp messages: {e}")
                    speak("Failed to send message")
            else:
                st.warning("⚠️ Please enter both phone number and message.")
