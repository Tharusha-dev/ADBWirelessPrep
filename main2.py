from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.auth.keygen import keygen


# Load the public and private keys
adbkey = '/home/tharushajayasooriya/.android/adbkey'
keygen(adbkey)

with open(adbkey) as f:
    priv = f.read()
with open(adbkey + '.pub') as f:
     pub = f.read()
signer = PythonRSASigner(pub, priv)

# # Connect via USB (package must be installed via `pip install adb-shell[usb])`
device2 = AdbDeviceUsb()
device2.connect(rsa_keys=[signer], auth_timeout_s=0.1)

# Send a shell command

response2 = device2.shell('echo TEST2')
print(response2)