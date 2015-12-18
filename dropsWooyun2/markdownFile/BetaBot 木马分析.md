# BetaBot 木马分析

[ 阿里云安全](/author/阿里云安全) · 2015/11/06 14:38

**作者:喔欧（阿里巴巴安全部安全威胁情报中心）**

# 0x00 背景介绍

* * *

在当下全球网络威胁活动中，国外攻击者主要使用Zeus、CryptoWall、Bedep、各类常见RAT工具等作为恶意负载，但在最近我们监控恶意威胁的过程中，发现个别高级样本攻击中使用了较为少见的BetaBot木马，关于此木马很少有相关的分析资料。在进一步了解、分析后发现，该木马还是具有很强的危害和对抗手段。为了方便监控BetaBot木马恶意攻击活动，所以记录相关分析结果，以供参考。

# 0x01 功能介绍

* * *

BetaBot，又被称为Neurevt，大概从2013年3月出现在地下市场被出售，售价大约在$120到$500。使用HTTP协议进行通信，使用RC4算法进行加密，代码使用C++语言编写，功能强大。据作者声称，该木马具备破坏杀软、自保护、BotKiller、Userkit(Ring3 Rootkit)、自定义注入技术、防其他木马感染、、DDoS、网络监视/阻塞、USB设备感染、SOCKS4代理、自校验保护、过UAC、反Sandbox等功能。

下图为示例的BetaBot服务端界面

![](http://static.wooyun.org//drops/20151106/201511060621355003714.png)

# 0x02 木马功能

* * *

## 系统驻留

添加注册表自启动

![](http://static.wooyun.org//drops/20151106/201511060621369362824.png)

添加Windows Tasks

![](http://static.wooyun.org//drops/20151106/201511060621388307234.png)

## 收集信息

运行环境、系统信息、硬件信息、软件信息等

例如软件信息搜集

![](http://static.wooyun.org//drops/20151106/201511060621409043044.png)

## 启动参数

部分命令以程序启动参数传入解析并执行

![](http://static.wooyun.org//drops/20151106/201511060621426632654.png)

## DDoS

支持4种类型的DDoS攻击方式

![](http://static.wooyun.org//drops/20151106/201511060621437634562.png)

## System Wide Userkit(Ring3 Rootkit)

功能名称引用作者描述，用于隐藏保护木马。

HOOK API列表

![](http://static.wooyun.org//drops/20151106/201511060621458433272.png)

![](http://static.wooyun.org//drops/20151106/201511060621462530781.png)

## UAC欺骗绕过

根据用户语言习惯构造错误信息，欺骗用户

![](http://static.wooyun.org//drops/20151106/201511060621472307091.png)

调用cmd.exe或者rundll32.exe触发UAC，实际调用木马自身

![](http://static.wooyun.org//drops/20151106/2015110606214943990101.png)

根据用户语言习惯构造错误信息

![](http://static.wooyun.org//drops/20151106/2015110606215069895112.png)

在BetaBot木马对抗杀软介绍时作者也提到了使用”社会工程学”的手段

![](http://static.wooyun.org//drops/20151106/2015110606215246030122.png)

## 配置解密

* * *

BetaBot的配置数据包含运行时所需要的释放目录位置、C&C、通信密钥等重要信息，并加密存放在木马文件内。

配置数据解密流程可以分为:

  1. 解密整体Config
  2. 依次解密C&C Entry

配置文件结构大小是0x0D56字节(随木马版本更新)，下图为解密整体config初始化代码，构造参数，动态解密执行代码，替换启动线程。

![](http://static.wooyun.org//drops/20151106/2015110606215358770131.png)

解密线程从imagebase搜索加密config特征，通过RC4和4字节异或进行解密，RC4解密key在自身代码中保存，解析出所需数据后，使用自更新的加密key重新加密。

![](http://static.wooyun.org//drops/20151106/2015110606215540039141.png)

![](http://static.wooyun.org//drops/20151106/201511060621574017515.png)

解密结果如下

![](http://static.wooyun.org//drops/20151106/201511060621591870916.png)

上图中前半部分已经解密，偏移0x156起始的C&C Entry还需要使用图中偏移0x6选中内容作为key解密，解密流程见下图

![](http://static.wooyun.org//drops/20151106/201511060622004054017.png)

可以看出该木马最多可以支持16个C&C配置。

例如解密出的一条C&C配置，其中包含了域名(偏移0x26)、端口(偏移0x14)、path(偏移0x66)、C&C通信key1(偏移0xAA)、key2(偏移0XB7)。

![](http://static.wooyun.org//drops/20151106/201511060622024064318.png)

## C&C通信解密

* * *

### 请求过程

![](http://static.wooyun.org//drops/20151106/201511060622033736919.png)

构造请求数据

![](http://static.wooyun.org//drops/20151106/201511060622058406120.png)

RC4加密请求数据并进行bin2hex转换，加密key是由C&C Entry配置的key1和随机字节序列拼接处理得到。

![](http://static.wooyun.org//drops/20151106/2015110606220617615211.png)

第一次请求会附上额外信息。

![](http://static.wooyun.org//drops/20151106/2015110606220887763221.png)

额外信息异或特定值并进行bin2hex转换。

![](http://static.wooyun.org//drops/20151106/2015110606220920000231.png)

最后将参与加密请求数据的随机字节序列进行bin2hex转换和上述bin2hex转换信息一起发送到服务端。

![](http://static.wooyun.org//drops/20151106/2015110606221066878241.png)

发送数据如下

![](http://static.wooyun.org//drops/20151106/201511060622121297025.png)

### 响应过程

![](http://static.wooyun.org//drops/20151106/201511060622138843526.png)

服务器响应包含两部分，header和body。

![](http://static.wooyun.org//drops/20151106/201511060622147812127.png)

首先需要解密header，其中最重要的是8个DWORD组成的数组streams_array，位于偏移0x3C，表示body各个结构的长度。

解密过程如下，RC4加密key是由C&C Entry的key1和response数据的前四个字节组合异或得到。

![](http://static.wooyun.org//drops/20151106/201511060622165540128.png)

最后根据streams_array计算body长度然后解密。

![](http://static.wooyun.org//drops/20151106/201511060622175285429.png)

加密的body位于偏移0x5C，解密过程如下，RC4加密key是由C&C Entry的key2和response数据偏移0x4四个字节组合异或得到。

![](http://static.wooyun.org//drops/20151106/201511060622206757530.png)

最终解密结果如下图，此图所示是服务端下发的监视域名列表配置。

![](http://static.wooyun.org//drops/20151106/2015110606222316723311.png)

## 其他

DNS阻断、表格抓取等功能可见参考链接。

# 0x03 对抗手法

* * *

## 反调试

**1.ZwQueryInformationProcess检测DebugPort**

![](http://static.wooyun.org//drops/20151106/2015110606222520033321.png)

**2.DbgBreakPoint对抗**

![](http://static.wooyun.org//drops/20151106/2015110606222671473331.png)

**3.ZwSetInformationThread**

![](http://static.wooyun.org//drops/20151106/2015110606222750126341.png)

**4.多处代码执行过程反调试对抗**

例如解密config代码中

![](http://static.wooyun.org//drops/20151106/201511060622296674935.png)

## 反虚拟机

![](http://static.wooyun.org//drops/20151106/201511060622309395736.png)

## 反JoeBox,GFI,Kasperksy,CWSandbox,Anubis等沙箱

![](http://static.wooyun.org//drops/20151106/201511060622324398837.png)

## 反Sandboxie沙箱

![](http://static.wooyun.org//drops/20151106/201511060622339326838.png)

## 反wine

![](http://static.wooyun.org//drops/20151106/201511060622355648539.png)

## 导入API加密

通过遍历系统dll导出表，拼接成moduleName+’.’+APIName计算hash进行搜索

Hash计算方式

![](http://static.wooyun.org//drops/20151106/201511060622368735240.png)

## 对抗杀软

检测杀软类型

![](http://static.wooyun.org//drops/20151106/2015110606223887346411.png)

![](http://static.wooyun.org//drops/20151106/2015110606223915085421.png)

![](http://static.wooyun.org//drops/20151106/2015110606224116772431.png)

禁用杀软

![](http://static.wooyun.org//drops/20151106/2015110606224256775441.png)

![](http://static.wooyun.org//drops/20151106/201511060622449527245.png)

![](http://static.wooyun.org//drops/20151106/201511060622454437346.png)

## 代码加密、动态替换

解密执行代码过程，例如解密Config线程函数体内容

![](http://static.wooyun.org//drops/20151106/201511060622475166447.png)

在一些函数调用时通过替换stub参数实现。例如stub原始代码

![](http://static.wooyun.org//drops/20151106/201511060622497138148.png)

替换参数

![](http://static.wooyun.org//drops/20151106/201511060622507127249.png)

## Snort检测规则

    
    
    alert http any any -> any any (msg: "Betabot Windows RAT Trojan Online Request"; flow: established, to_server; content: "POST"; http_method; content:"="; http_client_body; pcre: "/=\d{8}&/P"; content: "1="; distance:1; http_client_body; content: "2="; distance:1; content: "3="; distance:1; content: "4="; distance:1; content: "5="; distance:1; flowbits: set, betabot_online; classtype: trojan-detect; sid:010200291; rev:1; )
    

# 0x04 参考链接

* * *

  * <https://securityintelligence.com/beta-bot-phish/>
  * <http://www.slideshare.net/securityxploded/dissecting-betabot>

