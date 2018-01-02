from time import sleep
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


ip = ['x.x.x.35','x.x.x.36']

def vmrun():
    while True:
        stdout, stderr = ssh.exec_command('/usr/bin/vmrun list')
        output = stdout.readlines()
        output = stderr.readlines()
        print ''.join(output)
        sleep(3)

def execmd_with_param(ip):
    print (ip)
    commands = [
                "mv /home/root/witopia/{}.conf /home/offshore/witopia/config.conf".format(ip)
                ]
    for cmd in commands:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = None
        if stdout:
            output = stdout.readlines()
        if stderr:
            output = stderr.readlines()
        print ''.join(output)
    ssh.close()

if __name__ == "__main__":
    for ips in ip:
        try:
            if "10.14.47.1" in ips:
                ssh.connect(ips,port=22,username='root',password='test',look_for_keys=False,timeout=11)
            else:
                ssh.connect(ips, port=22, username='root', password='test', look_for_keys=False, timeout=11)
            # execmd_with_param(ips)
            # vmrun()
        except Exception as e:
            print e
