# HBUT-Srun-Login

## 简述 - Description

湖工校园网认证。
不包括任何非法破解网络内容。脚本仅为学习分享，不承担任何使用责任。

因为学校在冬季执行晚熄灯，每天路由器断电重启后都需重复web认证，故写了这个脚本开机执行。
借鉴了前人的代码，使用 `requests` 模拟了登录的 HTTP 过程。

## 用法 - Usage

下载这个项目，其中需要login.py 、config.json 、encryption/
将这个文件夹放入你想要的目录，设置开机执行即可

```plaintext
作者本机信息 - Host Info
OS: Arch Linux on Windows 10 x86_64 
Kernel: 5.15.90.1-microsoft-standard-WSL2 
Python 3.11.5
```

首先，需要确认所依赖的包是否安装：

```plaintext
pip3 install -r requirement.txt
```

安装好依赖项，查看配置文件 `config.json`：

```json
{
    "userInfo": {
        "username": "",
        "password": "",
        "domain": ""
    },
    "platformInfo": {
        "loginURL" : "http://202.114.177.246",
        "device" : "Windows NT",
        "os": "Windows"
    }
}
```

按照表格中的进行填入：

| 字段名   | 字段类型 | 应填内容                                      |
| -------- | -------- | --------------------------------------------- |
| username | string   | 登录校园网的用户名                            |
| password | string   | 登录校园网的密码                              |
| domain   | string   | 校园网类型                                    |
| device   | string   | 设备类型（可填：`Machintosh`, `Windows`,`PowerPC`） |
| os       | string   | 设备系统（可填：`Mac OS`, `Windows`, `Linux`）      |

校园网类型：

| 校园网类型 | 应填内容 |
| ---------- | -------- |
| 中国移动   | cmcc     |
| 中国电信   | ctcc     |
| 中国联通   | cucc     |
| 校园网     |          |

配置好信息之后保存至 `config.json`。

输入：

```plaintext
python3 login.py
```

如果输出：

```
jQuery112405169380394746533_1650453290998({"ServerFlag":0,"ServicesIntfServerIP":"202.114.177.246","ServicesIntfServerPort":"8001","access_token":"09e427ee4c0d9fe79c9af670140e3f00128c9ac7f3fb1dbf33ae3233db2d3192","checkout_date":0,"client_ip":"10.102.195.165","ecode":0,"error":"ok","error_msg":"","online_ip":"10.102.195.165","ploy_msg":"E0000: Login is successful.","real_name":"","remain_flux":0,"remain_times":0,"res":"ok","srun_ver":"SRunCGIAuthIntfSvr V1.18 B20210305","suc_msg":"login_ok","sysver":"1.01.20210305","username":"**********@*","wallet_balance":0})
```

其中：

```
"error":"ok"
```

代表登录成功。

## reboot to start

在OpenWRT系统中，要确保在系统完全启动后自动执行脚本，你可以使用以下方法：

使用`/etc/rc.local`文件：
   - 编辑`/etc/rc.local`文件，可以使用`vi`或其他文本编辑器打开它：`vi /etc/rc.local`
   - 在文件中添加`/bin/sh /root/HBUT-Srun-Login/autoLogin.sh`，确保在文件的`exit 0`行之前。
   - 保存并退出文件。
   - 授予`/etc/rc.local`执行权限：`chmod +x /etc/rc.local`

   这个文件会在系统启动的最后阶段执行，通常在其他服务和网络接口都已准备就绪后。

## License

本项目按照 [GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt) 进行开源。

## Credit

[coffeehat/BIT-srun-login-script](https://github.com/coffeehat/BIT-srun-login-script)

[iskoldt-X/SRUN-authenticator](https://github.com/iskoldt-X/SRUN-authenticator)
