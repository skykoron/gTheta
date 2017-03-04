import paramiko

host = '192.168.100.130'
user = 'amigos'
password = 'NakaY0s1'
LOCAL_PATH = '/home/pi/hogehoge.JPG'
REMOTE_PATH = '/home/amigos/urushihara/sftphoge.JPG'

conn = paramiko.SSHClient()
conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
conn.connect(host, username=user, password=password)
sfconn = conn.open_sftp()

sfconn.put(LOCAL_PATH, REMOTE_PATH)

files = sfconn.listdir()
for f in files:
    print(f)

sfconn.close()
conn.close()

