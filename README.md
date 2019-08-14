# Y-WebFind  

传入域名或者ip 进行相关信息探测  

需要安装 sudo apt-get install libpq-dev  nmap masscan   

web信息获取 请求头 使用的语言 服务器 简单的web框架指纹识别  

端口扫描  使用 masscan和 nmap结合  

弱口令扫描 支持 mysql redis ftp mongodb ssh postgresql  

## 使用:

[![asciicast](https://asciinema.org/a/MB4jdhHLe9lwkKu8WRTH9WhKg.png)](https://asciinema.org/a/MB4jdhHLe9lwkKu8WRTH9WhKg)


## **web信息获取**
`--web` 进行web信息获取 默认有这个参数  

## **端口扫描**: 
`--port` 则是使用nmap扫描默认的1000个常见端口  
`--netc` 进行c段扫描  
`--ap` 进行全端口扫描  


端口扫描后也会对识别的http https进行web信息获取  

## **弱口令**:
端口扫描后才能使用weak  
默认会去加载script目录下的弱口令脚本  
这里暂时把支持的写死到了类中  

## **DEBUG**
`--debug` 可以输出debug信息  



