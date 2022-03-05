# 东南大学健康打卡助手

这是一个健康申报自动化脚本，在正确配置之后，可以实现每日自动打卡，并通过邮件告知打卡结果。

请平日自觉打卡，建议将自动打卡脚本作为兜底。**出现发烧等异常状况时，请务必在打卡脚本运行前手动申报健康状况**，以免造成信息错报。祝各位用户身体健康。

默认上报体温为 36.2 ℃ 至 36.7 ℃。

## 更新日志

**2022.03.05:**

1. 正常体温数据随机化，取值范围为 [36.2, 36.7]；
2. 配置文件格式切换至 yaml，老式配置文件（personal_information.py）支持暂时保留;
3. 增加对 Docker 的支持。

**2022.03.04:**

1. 增加对 Linux 的支持。

**2021.11.16：**

1. 增加配置选项：是否需要通过邮件发送打卡结果;
2. 增加配置选项：是否只有在打卡失败时进行通知。

## 快速上手（Windows）

### 下载或 Clone 本仓库

```
git clone https://github.com/XAKK/SEU-health-reporting-helper.git
```

### 下载 ChromeDriver

下载与本机 Chome 浏览器版本相对应的 ChromeDriver，并移动至 SEU-health-reporting-helper 目录下。

### 新建配置文件

`config_demo.yml` 是演示配置文件，可以在此基础上修改。在 `SEU-health-reporting-helper` 目录下，新建一个名为 `config.yml` 的文件，并写入下面的内容，并根据实际情况，替换属性值字段。

```yaml
#################### 必填 ####################
# 学号（将 220000000 替换为您的一卡通号）
user_id: "220000000"

# 登录网上办事大厅的密码（将 ****** 替换为登录信息门户的密码）
password: "******"

# chromedriver 可执行文件路径
chrome_driver_path: "/usr/bin/chromedriver"

#################### 可选 ####################
# 是否需要发送邮件通知打卡结果（yes/no）
notification: "no"

# 只有尝试打卡失败后，才发送邮件（yes/no）
notify_failure_only: "no"

# 发送打卡状态的邮箱地址。对于东南大学邮箱，为 "USER_NAME@seu.edu.cn"（将 USER_NAME 替换为您的域名）
from_addr: "USER_NAME@seu.edu.cn"

# 发送打卡状态的邮箱密码（将 ****** 替换为您邮箱的密码）
email_password: "******"

# 发送打卡状态的邮箱的 smtp 服务器地址。对于东南大学邮箱，为 "smtp.seu.edu.cn"
smtp_server: "smtp.seu.edu.cn"

# 接收打卡状态的邮箱地址
to_addr: "name@example.com"


```

### 新建虚拟环境与安装依赖

```
python3 -m venv shrh-venv
.\shrh-venv\Scripts\activate
pip install -r requirements.txt
```

### 打卡

```powershell
run.bat
```

### 配置每日自动打卡

借助一台在预定义打卡时间处于运行状态的 Windows 机器，以及 Windows 任务计划程序，可以无人干预的情况下每日自动打卡。

**打开任务计划程序**。按下 `Win` + `R` ，输入 `taskschd.msc`

![image-20201225192823987](readme.assets/image-20201225192823987.png)

**创建任务**。右键【计划程序库】，再点击【创建任务】

![image-20201225201953696](readme.assets/image-20201225201953696.png)

**常规**。

1. 输入名称
2. 将安全选项中的账户改为具有相关权限的账户
3. 选择【不管用户是否登录都要运行】
4. 勾选【使用最高权限运行】

![image-20201226100637805](readme.assets/image-20201226100637805.png)

**触发器**

新建触发器

![image-20201226100848430](readme.assets/image-20201226100848430.png)

1. 将任务设置为【每天】执行
2. 配置随机延迟时间（可选）

![image-20201226101131615](readme.assets/image-20201226101131615.png)

**操作**

1. 新建操作
2. 选择启动程序（项目目录下的 `run.bat` 脚本）

![image-20201226101320319](readme.assets/image-20201226101320319.png)

完成上面配置后，便新建了一个计划任务。

**测试**

建议进行两个测试：

1. 右键任务，点击运行进行测试；
2. 设置一个近期的时间点，在未登录机器的情况下进行测试

正常情况下，该任务**不会弹出控制台**，**用户未登录也能下自动执行**，**能够将打卡结果通过邮件发送**。

## 快速上手（Docker）

### 下载或 Clone 本仓库

```
git clone https://github.com/XAKK/SEU-health-reporting-helper.git
```

### 新建配置文件

参考前文，略。

### 新建镜像

```
cd SEU-health-reporting-helper
docker build -t shrh:0.1 .
```

### 打卡

```
chmod +x run_docker.sh
./run_docker.sh
```

### 配置每日自动打卡

新建定时任务

```
crontab -e
```

新增下面的内容，将每天早上 8 点打卡（注意将 `/path/to/SEU-health-reporting-helper` 路径替换为实际项目路径）

```
* 8 * * * /path/to/SEU-health-reporting-helper/run_docker.sh
```

## 快速上手（Linux）

### 下载或 Clone 本仓库

```
git clone https://github.com/XAKK/SEU-health-reporting-helper.git
```

### 下载 ChromeDriver

自动根据 Chrome 版本，安装对应的 ChromeDriver 至 `/usr/bin`

```
./install_chromedriver.sh
```

### 新建配置文件

参考前文，略。

### 新建虚拟环境与安装依赖

```
python3 -m venv shrh-venv
source shrh-venv/bin/activate
pip install -r requirements.txt
```

### 打卡

```
chmod +x run.sh
./run.sh
```

### 配置每日自动打卡

借助 crontab，可实现自动打卡功能。

新建定时任务

```
crontab -e
```

新增下面的内容，将每天早上 8 点打卡（注意将两个 `/path/to/SEU-health-reporting-helper` 路径替换为实际项目路径）

```
SHELL=/bin/bash
PATH=/usr/local/bin/:/usr/bin:/usr/sbin
* 8 * * * DISPLAY=:1 /path/to/SEU-health-reporting-helper/run.sh >> /path/to/SEU-health-reporting-helper/dailyReport.log 2>&1
```
