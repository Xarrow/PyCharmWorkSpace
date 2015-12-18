# Redis漏洞攻击植入木马逆向分析

[ 阿里云安全](/author/阿里云安全) · 2015/11/17 14:24

作者：梦特（阿里云云盾安全攻防对抗团队）

# 0x00 背景

* * *

2015年11月10日，阿里云安全团队捕获到黑客大规模利用Redis漏洞的行为，获取机器root权限，并植入木马进行控制，异地登录来自IP：104.219.xxx.xxx（异地登录会有报警）。由于该漏洞危害严重，因此阿里云安全团队在2015年11月11日，短信电话联系用户修复Redis高危漏洞，2015年11月14日，云盾系统检测到部分受该漏洞影响沦为肉鸡的机器进行DDOS攻击，发现后云盾系统已自动通知用户。

# 0x01 木马控制协议逆向分析

* * *

分析发现木马作者，有2个控制协议未完成。

  * Connect协议有处理函数，但没有功能，函数地址为0x8048545。

![](http://static.wooyun.org//drops/20151117/2015111705143193322127.png)

  * sniffsniff协议没有对应的处理函数，作者未实现该功能。

完全逆向分析后得到控制协议如下表：

协议

协议格式

分析描述

kill

kill

结束自身进程

dlexec

dlexec IP filepath port

在指定IP下载文件并执行

qweebotkiller

qweebotkiller

遍历进程PID为0到65535，查找对应文件，若匹配特征EXPORT %s:%s:%s，则删除文件

system

system cmdline

调用系统的/bin/sh执行shell脚本

connect

connect ips arg2 arg3 arg4

有处理函数，但作者把connect的功能给阉割了，并没有去实现connect协议的功能，因此我们只分析出协议1个参数的意议，另外3个参数不知道意义。

icmp

icmp IPs attacktime PacketLen

发动icmp协议攻击

tcp

tcp ips port attacktime flags packetlen

发动TCP的(fin,syn,rst,psh,ack,urg)DDOS攻击，攻击时间为秒。

udp

udp ips port attacktime packetlen

发动UDP攻击。

sniffsniff

sniffsniff

这个协议木马并没有实现功能。

  * 协议完成逆向后，我们用Python写了一个控制端，并实现全部协议控制木马，如下图：

![](http://static.wooyun.org//drops/20151117/2015111705143496654223.png)

# 0x02 木马概述

* * *

从逆向得到的协议分析可以发现，该木马的功能主要包括：

  * 发动DDoS攻击（ICMP、UDP、TCP）
  * 远程执行命令
  * 远程下载文件执行
  * 清除其他后门文件

文件MD5：9101E2250ACFA8A53066C5FCB06F9848

## 进程操作

  * 木马启动，木马接受1个参数，参数为要kill的进程PID。函数地址为0x8049C77.

![](http://static.wooyun.org//drops/20151117/2015111705143547127319.png)

  * 木马会启动一个孙子进程执行木马功能，然后当前进程退出。

## 文件操作

  * 暴力关闭文件，关闭0到0xFFFF的文件，调用系统调用sys_close()，函数地址为0x8049C77。

![](http://static.wooyun.org//drops/20151117/2015111705143724045418.png)

  * 自我删除，调用系统调用`sys_readlink()`读取`/proc/self/exe`获取文件路径，`sys_unlink()`进行删除，处理函数地址为0x80494F3。

![](http://static.wooyun.org//drops/20151117/2015111705143994497512.png)

## 网络操作

  * 连接8.8.8.8的53端口，探测网络是否连接到Internet，处理函数地址为0x8049B90。

![](http://static.wooyun.org//drops/20151117/201511170514414532769.png)

  * 连接木马控制端37.xxx.xxx.x的53端口，处理函数地址为0x8049C77。

![](http://static.wooyun.org//drops/20151117/201511170514438152078.png)

