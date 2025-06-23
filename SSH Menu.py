import os
print("""
---------------------------------------------------
Linux menu based project - Run any command of linux
---------------------------------------------------
1.Date command
2.Cal command
3.Ifconfig
4.ls
5.cat /etc/passwd
6.cat /etc/group
7.cat /etc/shadow
8.Show system hostname
9.Current user
10.System uptime
11.Memory usage
12.View running processes
13.Real-time process monitor
14.Disk space usage
15.OS & kernel info

""")
user = input("Enter username :")
choice = input("Enter your choice :")
if choice == "1" :
    ip= input("Enter your remote ip :")
    os.system(f"ssh {user}@{ip} date ")

if choice == "2" :
    ip= input("Enter your remote ip :")
    os.system(f"ssh {user}@{ip} cal")

if choice == "3" :
    ip= input("Enter your remote ip :")
    os.system(f"ssh {user}@{ip} ifconfig")

if choice == "4" :
    ip= input("Enter your remote ip ")
    os.system(f"ssh {user}@{ip} ls")

if choice == "5" :
    ip= input("Enter your remote ip ")
    os.system(f"ssh {user}@{ip} cat /etc/passwd")

if choice == "6" :
    ip= input("Enter your remote ip ")
    os.system(f"ssh {user}@{ip} cat /etc/group")
if choice == "7" :
    ip= input("Enter your remote ip ")
    os.system(f"ssh {user}@{ip} cat /etc/shadow")
if choice == "8" :
    ip= input("Enter your remote ip ")
    os.system(f"ssh {user}@{ip} hostname")
if choice == "9" :
    ip= input("Enter your remote ip ")
    os.system(f"ssh {user}@{ip} whoami")
if choice == "10" :
    ip= input("Enter your remote ip ")
    os.system(f"ssh {user}@{ip} uptime")
if choice == "11" :
    ip= input("Enter your remote ip ")
    os.system(f"ssh {user}@{ip} free -m")
if choice == "12" :
    ip= input("Enter your remote ip ")
    os.system(f"ssh {user}@{ip} ps aux")
if choice == "13" :
    ip= input("Enter your remote ip ")
    os.system(f"ssh {user}@{ip} top")
if choice == "14" :
    ip= input("Enter your remote ip ")
    os.system(f"ssh {user}@{ip} df -h")
if choice == "15" :
    ip= input("Enter your remote ip ")
    os.system(f"ssh {user}@{ip} uname -a")
if choice == "16" :
    ip= input("Enter your remote ip ")
    os.system(f"ssh {user}@{ip} history")









    