# 敏感信息探测设计  

# git svn 等  

对于git 我们请求 .git 返回200 或者返回403 
对于 .gitignore 同样  
.svn/wc.db  

开发工具的    
./vscode  
.idea/  
.gitlab-ci.yml  
.DS_Store  

参考 https://xz.aliyun.com/t/3677  

下面这几个工具看一下  
Dirb Dirbuster wfuzz  
我们后面用这个页面进行测试 http://testphp.vulnweb.com/  

Python3中通过fake_useragent生成随机UserAgent    
我们这个web find 完全就是 他Vxscan的功能啊 对一个网站web的所有find 对把  
最后一个json报告
这个是第一步的信息探测  

下一步就是主动爬虫了  
获取url进行操作 当然可以主动和被动的形式  
功能一步一步做  
我们先搞 目录扫描 后面的再说  
如果这样做就不只是目录扫描了  
先把目录扫描做出来再说  
随机ua 那ip肯定也得随机啊  
先有个目录扫描的功能 然后后面再做其他的  
几个类之间进行结合操作  

对于页面相似度的计算  
#判断相似度的方法，用到了difflib库
def get_equal_rate_1(str1, str2):
   return difflib.SequenceMatcher(None, str1, str2).quick_ratio() 

先判断请求头那里的没有再算这个啊  


Content-Type  

如果是单页面开发那就没有对应的那些文件了  
我们得判断下是否是单页面开发  

如果是单页面开发又是怎么设置 
各种nginx 前后端分离就解决了这个问题其实 那我们这款主要是扫描信息泄露的  

我明白了 对于很多网站还是weblogic啊什么的这种开发的 会遗留很多敏感的目录  
当然这是比较基本的扫描  
后面我们对于单页面应用等就不是这样了 这种更多的是从流量接口下手  
我们先实现基本的探测 然后后面再针对单页面实现主动爬虫扫描和被动流量扫描  

各种模块结合  


### 获取服务端信息 
server 直接请求从响应的头中 `Server: BWS/1.1`  这个字段获取  
端口扫描 从 ip + 端口进行探测  可以选择 简单扫描还是全量扫描  使用nmap进行扫描  
获取网站什么语言的可以从这个 字段获取  `X-Powered-By`  很可能没有  

可以针对域名来生成对应的备份文件 域名+ `.rar  .zip` 等  

字典太大尽量少量的扫描 还会被封ip  
所以我们动态代理和 优化字典的是很重要的  
我们要尽可能减少请求次数 同时更精确的测试url  

他这里对域名各种变化来生成对应的字典  


输出的话 [时间] [状态码] -> /config/config/ 

就是这样的  
一个是字典的形式  
基于字典 但是应该尽量减少 跑的总量  
针对去跑 对字典进行分类-> 命中 这样再去跑  
我看有一些目录在这些目录的情况下再去跑  
不是特定的目录吗  


UA 使用特定的 要指定sec scan这样  

args 传入一个域名  是否指定ip 没有就要直接自己解析 
1.扫描端口是否全端口扫描  
识别是否cdn cdn的话就没必要端口扫描这些了  

一个域名 -> ip->判断是否cdn 
                        ->不是cdn -> 端口扫描 web请求获取网站标题 服务器类型 语言类型 cms waf识别 
                                 -> 获取c段  
                                 -> 是否进行敏感信息探测 (git svn js 目录等)
                                     敏感信息探测-> 基于语言类型或者传入的参数指定基于字典进行扫描  (基于爬虫动态生成字典?)
                                                -> 对js敏感信息的一些获取


支持代理和延迟功能  


这个要增加颜色输出  
应该多线程去处理相当于一个任务队列多节点 伪分布式非阻塞实现  


流程:  
判断是ip还是域名  
域名转成ip 判断是否存活  
这个得增加log输出的 并且增加颜色输出  

py3的日志操作 
重新写个最好写个三方库作为安全开发的log第三方库  
