# CXUtils

## 功能

- 支持所有签到类型——普通，定位，手势，签到码，二维码
- 支持要求定位验证的二维码签到
- 自动判断签到类型并解决验证码
- 支持随堂练习答题
- 支持课堂讨论回复并支持查看他人答案（无视教师端设置）
- 支持查看抢答情况（状态，已抢人数和列表）并一键抢答
- 可添加多个账户，支持多人同时进行同一项活动
- 支持多端同步已添加的账户
- 可生成配置二维码，便捷导入新设备使用

## 使用

### 后端

**方法一：Docker**

```bash
docker pull kenxu2022/cxutils:latest
docker run -d -p 8000:8000 \
  --name cxutils \
  -v cxutils_db:/cxutils/db \
  -e USERNAME=$USERNAME \
  -e PASSWORD=$PASSWORD \
  -e SECERT_KEY=$SECRET_KEY \
  kenxu2022/cxutils:latest
```
**环境变量优先级高于配置文件**，可供设置的变量列表：
|项目|说明|
|:---|:---|
|`USERNAME`|后端用户名|
|`PASSWORD`|后端密码|
|`SECERT_KEY`|用于生成访问令牌的密钥，若发生变化，则需重启前端应用，默认随机生成|
|`ALLOW_USER_SYNC`|是否开启用户列表同步功能，默认为否|

**方法二：手动运行**

```bash
git clone https://github.com/Kenxu2022/CXUtils.git
cd CXUtils/
pip install -r requirements.txt
python main.py
```

之后需要配置反向代理，以下提供 Nginx 配置参考：  
```conf
server {
    listen 80;
    listen [::]:80;
    server_name $SERVER_NAME;
    return 301 https://$host$request_uri;
}
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name $SERVER_NAME;
    ssl_certificate $PATH_TO_CERTIFICATE;
    ssl_certificate_key $PATH_TO_KEY;
    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Host $http_host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
    }
}
```

### 前端

**Android**

前往[前端仓库](https://github.com/Kenxu2022/CXUtils_APP)，下载并安装.apk结尾的安装包。

**iOS**

由于平台限制无法提供iOS平台安装包，暂时需要使用网页端，详见[前端仓库](https://github.com/Kenxu2022/CXUtils_APP)。

## 注意

- 对于手势或签到码签到，依然需要知道签到码（手势顺序即为签到码）
- 对于二维码签到，依然需要扫描教师发布的二维码

## 许可

GNU GPLv3