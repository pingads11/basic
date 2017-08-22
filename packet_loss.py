import smtplib
import subprocess
import socket
import fcntl
import struct
import datetime
import os

fileName = os.popen("date +%y_%m_%d_%H_%M_%S").read()

def ping():
    host1 = "google.com"
    ping1 = subprocess.Popen(
            ["ping", "-c", "5", "-W", "1", host1],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
    )

    host2 = "208.43.102.250"
    ping2 = subprocess.Popen(
            ["ping", "-c", "5", "-W", "1", host2],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
    )

    out, error = ping1.communicate()
    lines = out.splitlines()
    packet_lineg = ''
    for each_line in lines:
        print each_line
        if 'packet loss' in each_line:
            packet_lineg = each_line
            break

    out, error = ping2.communicate()
    lines = out.splitlines()
    packet_lines = ''
    for each_line in lines:
        print each_line
        if 'packet loss' in each_line:
            packet_lines = each_line
            break

    percentageg = int(packet_lineg.split('packet loss')[0].split(',')[-1].replace('%', '').strip())
    percentages = int(packet_lines.split('packet loss')[0].split(',')[-1].replace('%', '').strip())

    if percentageg > 2 or percentages > 2:
        return True,packet_lines,packet_lineg
    else:
        return False,None,None
    
def sendmail(ip,packet_lines,packet_lineg):
    sender = 'pingads11@gmail.com'
    receivers = ['pingads11@gmail.com','pingads11@live.com']
    message = """Subject: Packet loss on """ + ip + """\n\n Ping statistics for Google.com""" """\n""" + packet_lineg + """\n\n Ping statistics for Softlayer""" """\n""" + packet_lines + """\n\n""" + """filename is """ + fileName
    cur_time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    os.system('echo "' + cur_time + ', ' + packet_lines + '" >> p1.txt')
    os.system('echo "' + cur_time + ', ' + packet_lineg + '" >> p2.txt')
    username = 'ads@gmail.com'
    password = 'ads123'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(sender, receivers, message)
    server.quit()


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
    )[20:24])

def dump():
    print "dump",fileName
    os.system(
        "screen -dmS tcp tcpdump -i eth0 -w test.pcap host 208.43.102.250 -G 60 -W 1 -w /home/ads/packetloss-ads/packet_" + fileName + ".pcap")

def wget():
    os.system("wget -t 2 -T 11 -O /dev/null http://208.43.102.250/downloads/test10.zip")

def trace():
    os.system("tracepath 208.43.102.250 > /home/ads/packetloss-ads/trace" + fileName + "2>&1")

def telnet():
    os.system('{ echo ""; echo "test"; sleep 1; echo "bye\n"; } | telnet 208.43.102.250 80')

if __name__ == '__main__':
    wget()
    telnet()
    flag,packet_lines,packet_lineg= ping()
    if flag:
        ip = get_ip_address('eth0')
        sendmail(ip,packet_lines,packet_lineg)
        trace()
    else:
        os.system("rm -rf /home/ads/packetloss-ads/packet_" + fileName + ".pcap")
