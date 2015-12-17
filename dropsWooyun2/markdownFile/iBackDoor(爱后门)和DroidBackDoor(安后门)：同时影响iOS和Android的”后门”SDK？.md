# iBackDoor(爱后门)和DroidBackDoor(安后门)：同时影响iOS和Android的”后门”SDK？

[ 蒸米](/author/蒸米) · 2015/11/05 10:11

**作者：蒸米@阿里移动安全，楚安@阿里威胁感知，迅迪@阿里移动安全**

# 0x00 FireEye报告

* * *

iOS被XcodeGhost血洗一把之后，Android又被WormHole暴揍一顿。正当大家打算歇一歇的时候，FireEye的Zhaofeng等人又发表了一篇报告叫《iBackDoor: High-Risk Code Hits iOSApps》。报告中指出FireEye的研究员发现了疑似”后门”行为的广告库mobiSage在上千个app中，并且这些app都是在苹果官方AppStore上架的应用。通过服务端的控制，这些广告库可以做到：

  1. 录音和截屏
  2. 上传GPS信息
  3. 增删改查app数据
  4. 读写app的钥匙链
  5. 发送数据到服务器
  6. 利用URL schemes打开其他app或者网页
  7. 安装企业应用

FireEye的研究员一共在App Store上发现了2,846个app包含具有“后门”特征的mobiSage广告库。并且这些广告库会不断的向服务器端发送请求，并获取执行指令的JavaScript脚本。FireEye的研究员还发现mobiSage广告库一共有17不同的版本从5.3.3到6.4.4。然而在最新的mobiSage SDK 7.0.5版本中已经将这些”后门”特征删掉了。

# 0x01 iOS样本 - iBackDoor分析

* * *

看到FireEye的报告后，我们第一时间拿到了iOS上的app样本进行分析（注：在我们分析时，该样本还没有下架）。在广告库的类MSageCoreUIManagerPlugin中，我们的确发现了报告中所提到的各种控制功能。其中包括非常高危的获取录音、截屏功能以及读取修改字符串的函数。

![enter image descriptionhere](http://static.wooyun.org//drops/20151104/2015110418454315024.png)

根据反编译的代码可以看到，iBackDoor在获取到服务器命令后会启动录音功能并将录音保存为audio_[编号].wav，并且可以通过sendHttpUpload函数将文件发送到服务器上。

![enter image descriptionhere](http://static.wooyun.org//drops/20151104/2015110418454343300.png)

![enter image descriptionhere](http://static.wooyun.org//drops/20151104/2015110418454390909.png)

iBackDoor还可以截取当前屏幕的内容，反编译代码如下：

![enter image descriptionhere](http://static.wooyun.org//drops/20151104/2015110418454392363.png)

iBackDoor还可以读取keychain的数据，也就是iOS上的app用来保存密码信息的容器：

![enter image descriptionhere](http://static.wooyun.org//drops/20151104/2015110418454490700.png)

一个广告sdk，为什么需要录音，截屏和读取密码等功能呢？的确非常可疑。

![enter image descriptionhere](http://static.wooyun.org//drops/20151104/2015110418454417599.png)

除此之外，iBackDoor还可以根据服务器的指令调用任意的URLSchemes，也就是说XcodeGhost可以干的事情（打开钓鱼网页，安装企业应用等）iBackDoor也都可以干。比如如下是安装企业应用的反编译代码：

![enter image descriptionhere](http://static.wooyun.org//drops/20151104/2015110418454434031.png)

# 0x02 数据流量分析

* * *

通过分析反汇编代码我们发现中了iBackDoor的app会根据本地的msageJS脚本执行相应的指令。除此之外，iBackDoor还会发送post请求到entry.adsage.com去检查更新，如果有新的JS命令脚本就会到mws.adsage.com下载。

于是我们分析了一下entry.adsage.com和mws.adsage.com的DNS解析和流量数据：

![enter image descriptionhere](http://static.wooyun.org//drops/20151104/2015110418454479569.png)

根据DNS解析趋势，可以看到每天请求的数据并没有太大的浮动。但有意思的是，在对流量的分析中，除了adv-ios-*-min.zip外我们还发现了很多机器对adv-android-*-min.zip的下载请求。难道除了iOS的app，android上的app也难逃魔爪？

![enter image descriptionhere](http://static.wooyun.org//drops/20151104/2015110418454417680.png)

并且这个请求的数量还不小，在我们有限的监测流量中，光九月份就有4亿多次对adsage.com的数据发送。并且，最近半年内至少有超过50000次对更新脚本adv-ios-*-min.zip或adv-android-*-min.zip的下载请求。

# 0x03 Android样本 - DroidBackDoor分析

* * *

上文讲到了我们除了iOS的payload还发现了Android的payload，我们把这个payload下载下来一看，发现原来就是个动态加载的dex文件。这个dex文件包含了非常多的高危代码，我们把它称为DroidBackDoor。DroidBackDoor除了广告sdk都会做的获取手机各种信息，下载和安装任意apk外，还可以获取用户的坐标、打开任意网页、打电话、发短信等。

收集用户的imei，root信息，地理位置，wifi信息等几十种信息：

![in1](http://static.wooyun.org//drops/20151105/2015110505592495575in1.png)

![in2](http://static.wooyun.org//drops/20151105/2015110505592641395in2.png)

![in3](http://static.wooyun.org//drops/20151105/2015110505592771888in3.png)

![in4](http://static.wooyun.org//drops/20151105/2015110505592978865in4.png)

![in5](http://static.wooyun.org//drops/20151105/2015110505593410887in5.png)

![in6](http://static.wooyun.org//drops/20151105/2015110505593942083in6.png)

![in7](http://static.wooyun.org//drops/20151105/2015110505594039419in7.png)

获取用户坐标的反汇编代码：

![enter image descriptionhere](http://static.wooyun.org//drops/20151104/2015110418454531487.png)

打开任意网页的反汇编代码：

![enter image descriptionhere](http://static.wooyun.org//drops/20151104/2015110418454536774.png)

打电话的反汇编代码：

![enter image descriptionhere](http://static.wooyun.org//drops/20151104/2015110418454565079.png)

发短信的反汇编代码：

![enter image descriptionhere](http://static.wooyun.org//drops/20151104/2015110418454560975.png)

我们将提取的mobisage的特征去后台数据库查询，发现Android上也有超过2000款的app使用了mobisage的sdk。

# 0x04 网站分析

* * *

通过相关域名网站(http://www.adsage.cn/index.html)，可以知道这家公司的名字叫艾德思奇，并且有很多知名的合作伙伴和案列。我们建议所有使用了这个SDK的厂商应立刻检查自己产品中是否被插入了高危风险的代码，以免被苹果下架。

# 0x05 总结

* * *

虽然这次”后门”SDK同时影响了iOS和Android，但根据我们的数据分析结果发现影响力是远远不及XcodeGhost和WormHole的。所以用户不用太过担心，在受影响的app下架之前尽量不要安装不知名应用，并记得及时更新自己的app。

# 0x06 参考资料

* * *

  1. https://www.fireeye.com/blog/threat-research/2015/11/ibackdoor_high-risk.html

