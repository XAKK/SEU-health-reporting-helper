class Info:
    # 是否需要发送邮件通知打卡结果（yes/no）
    notification = "no"

    # 只有尝试打卡失败后，才发送邮件（yes/no）
    notify_failure_only = "no"

    # 发送打卡状态的邮箱地址。对于东南大学邮箱，为 "USER_NAME@seu.edu.cn"（将 USER_NAME 替换为您的域名）
    from_addr = "USER_NAME@seu.edu.cn"
    
    # 发送打卡状态的邮箱密码（将 ****** 替换为您邮箱的密码）
    email_password = "******"

    # 发送打卡状态的邮箱的 smtp 服务器地址。对于东南大学邮箱，为 "mail.seu.edu.cn"
    smtp_server = "mail.seu.edu.cn"

    # 接收打卡状态的邮箱地址
    to_addr = "name2@example.com"

    # 学号（将 220000000 替换为您的一卡通号）
    user_id = "220000000"

    # 登录网上办事大厅的密码（将 ****** 替换为登录信息门户的密码）
    password = "******"