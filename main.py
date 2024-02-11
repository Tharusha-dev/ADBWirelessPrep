import subprocess
import re

#port to be used with tcpip
PORT = '5555'

COMMAND_GET_IP = ['adb', 'shell', 'ifconfig', 'wlan0', '|', 'grep', '"inet addr"']
COMMAND_SET_TCPIP_PORT = ['adb', 'tcpip', PORT]
COMMAND_CONNECT = ['adb','connect']
COMMAND_CONNECTED_DEVICES = ['adb','devices']


#extraxt ip address from the output of COMMAD_GET_IP
def extract_ipv4_1(string):
    pattern = r"inet addr:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"

    match = re.search(pattern, string)
    if match:
        return match.group(1)
    else:
        return None
    
#extraxt ip address from the output of COMMAND_CONNECTED_DEVICES
def extract_ipv4_2(string):
    pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"

    match = re.search(pattern, string.replace("\n",""))
    if match:
        return match.group(1)
    else:
        return None

#check whether the ip address is already connected
def is_already_connected(ip):

    proc = subprocess.Popen(COMMAND_CONNECTED_DEVICES, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    output = o.decode('utf-8').replace('\n','')
    ipaddr = extract_ipv4_2(output)

    return ipaddr != None and ip == ipaddr



def main():
    
    proc = subprocess.Popen(COMMAND_GET_IP, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    o, e = proc.communicate()
    output = o.decode('utf-8').replace('\n','')
    ipaddr = extract_ipv4_1(output)
    print(f"Android device IP address found => {ipaddr}")

    if is_already_connected(ip=ipaddr):
        print("Android device is already connected via wifi")
        # run_development_stuff(ip=ipaddr)
    
    else:

        proc = subprocess.Popen(COMMAND_SET_TCPIP_PORT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        o, e = proc.communicate()

        #Add adnroid devices ip address and predefined port to COMMAND_CONNECT
        COMMAND_CONNECT.append(f"{ipaddr}:{PORT}")

        proc = subprocess.Popen(COMMAND_CONNECT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        o, e = proc.communicate()

        print(o.decode("utf-8"))

        # run_development_stuff(ip=ipaddr)



main()

