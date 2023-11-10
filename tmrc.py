##################################################
# TMRC - Tor Middle Relay Creator                #
# By DamballahOueddo                             #
# V0.1                                           #
# https://github.com/damballah/tmrc              #
# mail : gh@damb1.go.yj.fr                       #
# opgpk:A2E8C4FF178B3DBF480D8FF9F796D16A7367DEBB #
##################################################

import os
import time
import shutil
import subprocess

def GetRightof(s, char):
    return s.split(char, 1)[-1]

def GetLeftOf(s, char):
    return s.split(char, 1)[0]

def GetBetween(s, left, right):
    return s.split(left, 1)[-1].split(right, 1)[0]

def print_all_chars(s):
    for c in s:
        if ord(c) < 32 or ord(c) == 127:  # Si c'est un caractère de contrôle
            print(f'\\x{ord(c):02x}', end='')
        else:
            print(c, end='')
    print()

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if error:
        print(f"Une erreur s'est produite : {error}")
    else:
        print(f"Sortie de la commande : {output.decode()}")

def getCmdOutput(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    return result.stdout.decode()

def replaceWordInFile(filename, old_word, new_word):
    with open(filename, 'r') as file:
        filedata = file.read()
        new_data = filedata.replace(old_word, new_word)
    with open(filename, 'w') as file:
        file.write(new_data)

def readVersion(filename):
    with open(filename, 'r') as file:
        filedata = file.read()
    return filedata

def copy_file(source, destination):
    shutil.copy2(source, destination)

def append_to_file(filename, text):
    with open(filename, 'a') as file:
        file.write(text + '\n')

def delete_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)
    else:
        print(f"Erreur : {filename} n'existe pas.")

def create_nixrun():
    bash_script = """#!/bin/bash
    sleep 5
    nyx
    """
    with open('runnix.sh', 'w') as file:
        file.write(bash_script)
    os.chmod('runnix.sh', 0o755)
    
# Local files folder and name of the files
fLocalFolder = "./files/"
lFileUpgr = "50unattended-upgrades"
lFileTorLst = "tor.list"
lFileTorParam = "torrc"

#  Destination folders and name of the files
dFileUpgr = "/etc/apt/apt.conf.d/" + lFileUpgr
dFileTorLst = "/etc/apt/sources.list.d/" + lFileTorLst
dFileTorParam = "/etc/tor/" + lFileTorParam

# VersionOfDistrib
vDistrib=""

# start of script

# Get information about the administrator and the configuration of the Middle Tor Relay
finish=False
while not finish==True:
    os.system('clear')
    print("*********************************")
    print("* TOR MIDDLE RELAY CREATOR V0.1 *")
    print("*      By DamballahOueddo       *")
    print("*********************************")
    print("")
    nickname = input("Please enter a nickname for your Tor Middle Relay : ")
    adminEmail = input("Enter email of the administrator : ")
    portOfRelay = input("By default the port of your middle relay is 433, please enter a different or not (just press enter) : ")

    # Control port
    if portOfRelay == "":
        portOfRelay = "443"

    maxBandwith = input("And for finish, enter the maximum bandwith you want to share to , like this, for exemple = 500 GB : ")
    print("")
    print("Nickname = " + nickname)
    print("Admin email = " + adminEmail)
    print("Port of Relay = " + portOfRelay)
    print("Bandwith max = " + maxBandwith)
    print("")
    formResponse = input("Do you agree with everything you have said? [Y/N]")
    if formResponse == "Y":
        finish=True
    elif formResponse == "N":
        finish=False

print("")
print("Next step is on the way...")

print("")
print("Step 1 - update")
run_command("apt update")

print("")
print("Step 2 - install unattended upgrades")
run_command("apt-get install unattended-upgrades apt-listchanges")

print("")
print("Step 3 - copy 50unattended-upgrades to the destination folder")
f1 = fLocalFolder + lFileUpgr
f2 = dFileUpgr
cmd = "cp " + f1 + " " + f2
run_command(cmd)

print("")
print("Step 4 - Test the configuration")
run_command("unattended-upgrade --debug")

print("")
print("Step 5 - install apt-transport-https")
run_command("apt install apt-transport-https")

print("")
print("Step 6 - get the version of distribution in a file")
run_command("rm version.txt")
run_command("lsb_release -c > version.txt")

vDistrib = readVersion("version.txt")
vDistrib = GetRightof(vDistrib,":").strip()
print("")
print("Distrib version : " + vDistrib)

print("")
print("Step 7 - delete the version.txt file")
run_command("rm version.txt")

print("")
print("Step 8 - Write a torlist file in the good directory with grab of the version of distrib")
TorLst = dFileTorLst
L1="deb [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] https://deb.torproject.org/torproject.org" + " " + vDistrib + " " + "main"
L2="deb-src [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] https://deb.torproject.org/torproject.org" + " " + vDistrib + " " + "main"
append_to_file(TorLst,L1)
append_to_file(TorLst,L2)
print("TorProject keyrings add to the file -> /etc/apt/sources.list.d/tor.list")

print("")
print("Step 9 - Get the good version of Tor with the gpg key")
run_command("wget -qO- https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --dearmor | tee /usr/share/keyrings/tor-archive-keyring.gpg >/dev/null")

print("")
print("Step 10 - apt update and apt install tor deb.torproject.org-keyring")
run_command("apt update")
run_command("apt install tor deb.torproject.org-keyring")

print("")
print("Step 11 - Copying the local torrc file to the destination folder and configure the tor middle node")
f1 = fLocalFolder + lFileTorParam
f2 = dFileTorParam
cmd = "cp " + f1 + " " + f2
run_command(cmd)

print("")
print("Configure torrc file...")
replaceWordInFile(f2,"{nickname}",nickname)
replaceWordInFile(f2,"{mailinfo}",adminEmail)
replaceWordInFile(f2,"{port}",portOfRelay)
replaceWordInFile(f2,"{bandwith}",maxBandwith)

print("")
print("Enabled Tor as service...")
run_command("systemctl enable tor")

print("")
print("Restart Tor as service...")
run_command("systemctl restart tor")

print("")
print("Open the port : " + portOfRelay + " ...")
cmd1="sudo apt install ufw"
cmd2="sudo ufw allow " + portOfRelay
run_command(cmd1)
run_command(cmd2)

print("")
print("Installation of NYX monitoring for Tor Relay...")
run_command("yes | apt install nyx")
print("###########################")
print("###   SETUP IS FINISH   ###")
print("###########################")
print("")
print("#### DON'T FORGET TO OPEN THE PORT : " + portOfRelay + " of your  gateway or router ####")
print("")
print("To run NYX now, type: nyx en press ENTER")
print("")
print("Thank's you and have fun ;)")
print("")


