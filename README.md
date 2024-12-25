# **宁夏理工新教务系统内网登录程序**
# **小易教务V3.1**
**作者：小易同学 邮箱：xytx954@126.com**

本程序来自电信学院，并不来自某些装逼狗。
本程序在2024.12.23与2024.12.25两次实际测试中完美帮助共计300名左右的同学抢到课。

## **简单说一下基本原理：**

登陆后抓取cookie然后用cookie登录内网教务。
就是这么简单，目前开源出来的这个版本能用但是拥有很多bug。
已经有做一个忽略时间随时随地都流畅的版本的思路了，但是学业繁忙，有思路但是没空做。
我就是干抢课这一行的，打算不干这一行了，于是开源自己的软件。
再说一遍，有bug，我知道，我懒得改了，这玩意儿和我的专业相关性不大。以后多半不会维护了。有相关大佬可以基于我的代码继续开发吧。

## **如何安装？**

在“EXE文件下载链接.txt”中有网盘下载链接。
下载你的电脑里浏览器所对应的版本。
若EDGE和CHROME两个版本都无法使用，你就下载集成浏览器版本。
若三个版本都无法使用。你就下载main.py文件自己用python运行吧！所需要哪些依赖？自己根据main.py文件的头部去逐个对比你是否安装那些依赖。

运行main.py很简单，先确保电脑已安装好chrome浏览器，然后在main.py所在文件目录的位置鼠标右键然后选择“在终端中打开”。
再输入：

```
python main.py
```

就OK了。再说一遍依赖自己研究有哪些，我还记得的就这个：

```
pip install psutil selenium
```

**小白用户直接点**https://www.alipan.com/s/7XFe4rkZ1uZ

## **如何使用？**

首先连接好校园网。尽量用联通校园网，测试的这两天移动校园网老是突然就使用不了内网了。
在抢课开始一个小时前运行main.py或者双击桌面图标。本软件支持多开，双击多少次桌面图标就开多少个浏览器实例。
我们有同学一台电脑开了50个浏览器，多开的上限取决于你的电脑CPU和内存。

然后等待到了统一门户登录界面后输入账号密码等待提示“你可以操作了，欢迎使用小易。。。”就OK了。然后你不要关闭这个浏览器和CMD窗口。每半个小时检查一次登录是否掉线，以及网址栏是否是10.100.100.141.
抢课开始后，就可以在内网教务流畅操作啦！

## **声明**

本软件仅支持提前登录到教务系统内网。不支持抢课开始后登录！！！

在这里提供给后继开发者一个抢课开始后继续登录内网的思路：

1. 从统一门户修改JS文件里的重定向规则，使其重定向到内网。
2. 直接在部署在教育网上的服务器抓取cookie,不从portal.nxist.com抓取cookie,从cas.nist.edu.cn或者myst.nist.edu.cn抓取。但是这个可不简单，你得精通WEB后端。
3. 一定要了解清楚10.100.100.141的每一个端口是干什么的以及10.100.100.141和portal.nxist.com关系。
4. 可登录内网的有效cookie的route值为：adef3cfba742b03d8aed0b1f92f60144。
5. 也就是，抢课开始后教育网和内网不卡，电信公网卡爆炸了，你能实现教育网登录到内网就行了。

**欢迎各位大佬基于我的思路二次开发！！！**
