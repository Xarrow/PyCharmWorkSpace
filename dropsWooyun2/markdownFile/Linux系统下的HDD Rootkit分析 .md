# Linux系统下的HDD Rootkit分析

[ 腾讯电脑管家](/author/腾讯电脑管家) · 2015/10/22 11:12

# 0x01 概况

* * *

前段时间，卡巴斯基捕获到Winnti网络犯罪组织在Windows下进行APT攻击的通用工具——HDDRootkit。近期，腾讯反病毒实验室在Linux系统下也捕获到同类工具。Winnti组织利用HDDRootkit在Windows和Linux系统下进行持续而隐蔽的APT攻击。经分析发现，HDD Rootkit先是篡改系统的引导区，然后在进入Linux系统前利用自带的Ext文件系统解析模块，将隐藏在硬盘深处的后门文件解密出来后加入到开机启动脚本或系统服务里。目前受攻击的系统有Centos和Ubuntu。

![](http://static.wooyun.org//drops/20151020/2015102014030358723190.png)

(图1：HDD Rootkit在Linux下的攻击流程)

# 0x02 HDD Rootkit在 Linux下的详细分析

* * *

## 1、过程展示

分析HDD Rootkit：

![](http://static.wooyun.org//drops/20151020/2015102014033163916246.png)

（图2：分析HDD Rootkit得到的参数提示）

运行HDD Rootkit：

![](http://static.wooyun.org//drops/20151020/201510201403343634737.jpg)

(图3：运行HDD Rootkit工具)

通过图3，能看出HDD Rootkit平台已经把RKimage和Backdoor解密并写入扇区里面，而且计算了他们的Crc16值(这部分后面有更详细的分析）。接下来我们看看mbr的变化：一是第一扇区已经被改写(如图4)；二是开机瞬间显示出HDDRootkit的调试信息（如图5）。当系统中毒以后,第1扇区存放病毒的MBR，第25扇区存放BootCode，第26与第27扇区存放加密后的原始MBR。

![](http://static.wooyun.org//drops/20151020/2015102014033644646421.png)

（图4： 左边是被修改的mbr，右边是原始的mbr）

![](http://static.wooyun.org//drops/20151020/2015102014033894759517.png)

（图5：开机时RKimage的输出信息，注意：debug版本才有信息输出）

## 2、安装阶段详细分析

### (1) 运行安装方式与参数：

![](http://static.wooyun.org//drops/20151020/2015102014033943850615.png)

（图6：hdroot_32_bin安装方式）

在Linux下运行HDD Rootkit 如 `./root_32_bin inst ./createfile1`。其中第一个参数是安装类型，第二个参数是后门文件，第三个参数是启动类型(共三种开机启动方式)。

### (2) HDD Rootkit的文件存储和隐藏：

HDD Rootkit早期的版本是把MBR、BootCode、RKimage等放在程序资源里面，在Linux系统下则是把这些文件加密存储在安装器里面。以下分析HDDRootkit如何将加密好的MBR、Boot Code、RKimage解密出来，又重新加密写入到第一个扇区和空闲的扇区里面。

![](http://static.wooyun.org//drops/20151020/2015102014034150449717.png)

(图7：左边是加密的结构体，右边是解密过程)

HDD Rootkit将Rkimage 和Backdoor再次加密后写入扇区，将后门文件藏得更深。

![](http://static.wooyun.org//drops/20151020/2015102014034383963819.png)

(图8：将RKimage和Backdoor文件写入扇区)

获取引导盘，准备写入MBR和Bootcode，步骤如图9和图10所示。

![](http://static.wooyun.org//drops/20151020/2015102014035026976917.png)

(图9：步骤一)

![](http://static.wooyun.org//drops/20151020/20151020140351701011015.png)

(图10：步骤二)

### (3) RKimage 功能分析

RKimage是HDD Rootkit下释放的子工具。RKimage不依赖于操作系统，直接解析文件系统，能根据不同的安装情况，把后门加入开机启动。

RKimage模块：

  1. 由Bootcode拉起，将实模式切换到保护模式；
  2. 实现Ext文件系统解析与读写功能；
  3. 把隐藏在扇区的后门写成文件，根据不同的情况增加开机启动项。

![](http://static.wooyun.org//drops/20151020/20151020140353842361118.png)

(图11：RKimage的文件系统解析模块的字符串提示)

第一种开机启动方式：

![](http://static.wooyun.org//drops/20151020/20151020140355572181216.png)

(图12：`/etc/rc*.d/S7*cdiskmon` 类型)

第二种开机启动方式：

![](http://static.wooyun.org//drops/20151020/20151020140356886361313.png)

(图13：`/etc/rc.d/rc.local`类型)

第三种开机启动方式：

![](http://static.wooyun.org//drops/20151020/20151020140358219861413.png)

(图14：SYSTEMD类型)

### (4) 后门文件

由于获取的程序样本有限，在分析过程中并没有获取真正有效的Backdoor文件，所以整个攻击的完整流程和木马如何把信息向外通信并未分析到。因此，自主构造了一个写文件的可执行程序。

## 3、 调试 HDD Rootkit的MBR、Bootcode、RKImage关键节点

![](http://static.wooyun.org//drops/20151020/20151020140359470001513.png)

(图15：中毒后的第一扇区)

![](http://static.wooyun.org//drops/20151020/20151020140400947051612.png)

(图16：HDD加载Bootcode)

![](http://static.wooyun.org//drops/20151020/20151020140404834181711.png)

(图17：从Bootcode进入到RKimage模块)

![](http://static.wooyun.org//drops/20151020/20151020140408158391811.png)

(图18：RKimage模块加载GDTR)

![](http://static.wooyun.org//drops/20151020/2015102014041058454199.png)

(图19：RKimage模块里面准备切换到保护模式)

![](http://static.wooyun.org//drops/20151020/20151020140415804232010.png)

(图20：RKimage模块准备执行功能)

![](http://static.wooyun.org//drops/20151020/2015102014042243743211.jpg)

(图21：RKimage模块输出功能代码的调息信息)

