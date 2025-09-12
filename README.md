# CXUtils

## 功能

- 支持所有签到类型——普通，定位，手势，签到码，二维码
- 可添加多个账户，支持多人同时签到
- 自动判断签到类型并解决验证码

## 使用

### 后端

**方法一：Docker**

```bash
docker pull kenxu2022/cxutils:latest
docker run -d -p 8000:8000 \
  --name cxutils \
  -e USERNAME=$USERNAME \
  -e PASSWORD=$PASSWORD \
  -e SECERT_KEY=$SECRET_KEY \
  kenxu2022/cxutils:latest
```
自行设置`USERNAME`，`PASSWORD`，`SECERT_KEY`变量

**方法二：手动运行**

```bash
git clone https://github.com/Kenxu2022/CXUtils.git
cd CXUtils/
pip install -r requirements.txt
python main.py
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