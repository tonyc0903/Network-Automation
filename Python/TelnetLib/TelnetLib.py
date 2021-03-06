
"""
Program 1: 
    Telnet into Router to apply loopback and ospf configuration
"""
from getpass import getpass
import telnetlib

HOST = "192.168.122.71"
user = input("Enter your telnet username: ")
password = getpass("Enter your password: ")

tn = telnetlib.Telnet(HOST)

tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.write(b"enable\n")
tn.write(b"cisco\n")
tn.write(b"conf t\n")

loopbackAddresses = [b"ip address 1.1.1.1 255.255.255.255\n", b"ip address 2.2.2.2 255.255.255.255\n"]
for index, value in enumerate(loopbackAddresses):
    tn.write(b"int loopback " + str(index).encode('ascii') + b"\n")
    tn.write(loopbackAddresses[index].encode('ascii') + b"\n")
    #  tn.write(loopbackAddresses[n] + b"\n")

tn.write(b"end\n")
tn.write(b"exit\n")

print(tn.read_all().decode('ascii'))


"""
Program 2:
    Telnet into switches to create vlan interfaces
"""
from getpass import getpass
import telnetlib

HOST = ""
user = input("Enter your telnet username: ")
password = getpass("Enter your passowrd: ")

f = open('myswitches')

for IP in f:
    IP = IP.strip()
    print ("Configuring Switch " + (IP))
    HOST = IP
    tn = telnetlib.Telnet(HOST)
    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
       tn.read_until(b"Password: ")
       tn.write(password.encode('ascii') + b"\n")
    tn.write(b"enable\n")
    tn.write(b"cisco\n")
    tn.write(b"conf t\n")

    for n in range (2,31):
    tn.write(b"vlan " + str(n).encode('ascii') + b"\n")
    tn.write(b"name Python_VLAN_" + str(n).encode('ascii') + b"\n")

    tn.write(b"end\n")
    tn.write(b"wr\n")
    tn.write(b"exit\n")

print(tn.read_all().decode('ascii'))


"""
Program 3:
    Backup switches configs 
"""
import getpass
import telnetlib

user = input('Enter your telnet username: ')
password = getpass.getpass()

f = open('myswitches')

for IP in f:
    IP=IP.strip()
    print ('Get running config from Switch ' + (IP))
    HOST = IP
    tn = telnetlib.Telnet(HOST)
    tn.read_until(b'Username: ')
    tn.write(user.encode('ascii') + b'\n')
    if password:
        tn.read_until(b'Password: ')
        tn.write(password.encode('ascii') + b'\n')  
    tn.write(b"terminal length 0\n")
    tn.write(b"show run\n")
    tn.write(b'exit\n')

    readoutput = tn.read_all()
    saveoutput = open("switch " + HOST, "w")
    saveoutput.write(readoutput.decode('ascii'))
    saveoutput.write("\n")
    saveoutput.close

