# 东南大学健康打卡助手

这是一个健康申报自动化脚本，在正确配置之后，可以实现每日自动打卡，并通过邮件告知打卡结果。


## 前提

下面的操作都在 Windows 10 的机器上执行。相关依赖有：

- [Python 3.x](https://www.python.org/)
- Chrome 浏览器
- [ChromeDriver](https://sites.google.com/chromium.org/driver/)

脚本理论上跨平台，但暂无其他操作系统的配置演示。

## 快速上手

### 下载或 Clone 本仓库

```
git clone https://github.com/XAKK/SEU-health-reporting-helper.git
```

### 下载 ChromeDriver

下载与本机 Chome 浏览器版本相对应的 ChromeDriver，并移动至 SEU-health-reporting-helper 目录下。

### 新建配置文件

在 `SEU-health-reporting-helper` 目录下，新建一个名为 `personal_information.py` 的文件，并写入下面的内容：

```python
class Info:
    # 发送打卡状态的邮箱地址
    # 对于东南大学邮箱，为 "name@seu.edu.cn"（name一般为你的学号）
    from_addr = "name1@example.com"
    
    # 发送打卡状态的邮箱密码
    email_password = "******"

    # 发送打卡状态的邮箱的 smtp 服务器地址
    # 对于东南大学邮箱，为 "mail.seu.edu.cn"
    smtp_server = "mail.example.com"

    # 接收打卡状态的邮箱地址
    to_addr = "name2@example.com"

    # 学号
    user_id = "220xxxxxx"

    # 登录网上办事大厅的密码
    password = "******"
```

其中，根据自己实际，替换相关内容。各字段描述如下：

| 变量名           | 描述                                                         | 样例                  |
| ---------------- | ------------------------------------------------------------ | --------------------- |
| `from_addr`      | 发送打卡状态的邮箱地址，对于东南大学邮箱，一般为 "学号@seu.edu.cn" | `"name1@example.com"` |
| `email_password` | 发送打卡状态的邮箱密码                                       | `"******"`            |
| `smtp_server`    | 发送打卡状态的邮箱的 smtp 服务器地址，对于东南大学邮箱，为 "mail.seu.edu.cn" | `"mail.example.com"`  |
| `to_addr`        | 接收打卡状态的邮箱地址                                       | `"name2@example.com"` |
| `user_id`        | 学号                                                         | `"220xxxxxx"`         |
| `password`       | 登录网上办事大厅的密码                                       | `"******"`            |

上面信息将保存在本地，不会发送给第三方，但仍建议在可信的环境部署。

至此，`SEU-health-reporting-helper` 的目录中应至少包含下面的内容：

```
├───shrh-venv/
├───chromedriver.exe
├───main.py
├───personal_information.py
├───run.bat
├───readme.access/
└───readme.md
```

### 打卡

```powershell
run.bat
```

## 每日自动打卡相关配置（Windows）

借助一台在预定义打卡时间处于运行状态的 Windows 机器，以及 Windows 任务计划程序，可以无人干预的情况下每日自动打卡。

### 打开任务计划程序

按下 `Win` + `R` ，输入`taskschd.msc`

![image-20201225192823987](readme.assets/image-20201225192823987.png)

### 创建任务

右键【计划程序库】，再点击【创建任务】

![image-20201225201953696](readme.assets/image-20201225201953696.png)

### 常规

1. 输入名称
2. 将安全选项中的账户改为具有相关权限的账户
3. 选择【不管用户是否登录都要运行】
4. 勾选【使用最高权限运行】

![image-20201226100637805](readme.assets/image-20201226100637805.png)



### 触发器

新建触发器

![image-20201226100848430](readme.assets/image-20201226100848430.png)

1. 将任务设置为【每天】执行
2. 配置随机延迟时间（可选）

![image-20201226101131615](readme.assets/image-20201226101131615.png)

### 操作

1. 新建操作
2. 选择启动程序（项目目录下的 `run.bat` 脚本）

![image-20201226101320319](readme.assets/image-20201226101320319.png)

### 完成

完成上面配置后，便新建了一个计划任务。

### 测试

建议进行两个测试：

1. 右键任务，点击运行进行测试；
2. 设置一个近期的时间点，在未登录机器的情况下进行测试

正常情况下，该任务**不会弹出控制台**，**用户未登录也能下自动执行**，**能够将打卡结果通过邮件发送**。

## 其他

- 脚本理论上可跨平台运行，欢迎补充其他操作系统的配置方法。
- 默认上报体温为 36.5 ℃。