import paramiko

# Create SSH client
client = paramiko.SSHClient()

# Automatically add unfamiliar host keys
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the server
client.connect(
    hostname="192.168.68.80",
    username="kentv",
    password="Veekeong_90",
)

# stdin, stdout, stderr = client.exec_command("cd 'C:\Users\kentv\Desktop\testing' && echo 1234 > testt.txt")
stdin, stdout, stderr = client.exec_command("dir 'C:\\Users\\kentv\\Desktop\\testing'")
output = stdout.read().decode()
print(output)
client.close()