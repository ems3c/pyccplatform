import libvirt
import sys
import random
import json
import time
from ssh import start_socket

conn = None
try:
    conn = libvirt.open("qemu:///system")
except libvirt.libvirtError as e:
    print(repr(e), sys.stderr)
    sys.exit(1)

def CreateNewVIrtualMachine(name, ram, vcpu):    
        def getrandom(x, z):
            return random.randint(x, z)

        f  = open("freebsd.xml", "r")
        file_content = f.read().replace("{vmname}", str(name))
        new_placement = file_content.replace("{r_one}", str(getrandom(1, 9)))
        final_placement = new_placement.replace("{r_two}", str(getrandom(1, 9)))
        placement = final_placement.replace("{ram}", str(ram))
        place_cpu = placement.replace("{cpu}", vcpu)

        if conn.defineXML(str(place_cpu)) != None:           
            dom = conn.lookupByName(name)
            '''We are going to start the virtual machine'''
            dom.create()
            f.close()
            
         
def getIPaddress():
    try:
        dom = conn.lookupByName("freebsd")
        ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
        '''Call this latter start_socket(ip)'''
    except libvirt.libvirtError as e:
        sys.stderr.write("Error")
    return ifaces['vtnet0']['addrs'][0]['addr']
#print(getIPaddress())

def GetDomainState(domainname):
    dom = conn.lookupByName(domainname)
    state, reason = dom.state()
    if state == libvirt.VIR_DOMAIN_RUNNING:
        print("Domain is Active and running")
        
    elif state == libvirt.VIR_DOMAIN_SHUTOFF:
        print("Thw domain is Off")
    elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
        print("Thw domain is Shut Down")
def ShufOFFtheVM(domainname):
    dom = conn.lookupByName(domainname)
    dom.destroy()
        