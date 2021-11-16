import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

from personal_information import Info

class ReportingHelper:
    def __init__(self):
        self.cfg = Info

    def run(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless') # 使用无头浏览器，不跳出窗口
        driver = Chrome(chrome_options=chrome_options)

        driver.get('https://newids.seu.edu.cn/authserver/login?service=http%3A%2F%2Fehall.seu.edu.cn%2Fqljfwapp2%2Fsys%2FlwReportEpidemicSeu%2Findex.do%3Ft_s%3D1594447890898%26amp_sec_version_%3D1%26gid_%3DSTZiVXZjRnhVSS9VNERWaFNNT1hXb2VNY3FHTHFVVHMwRC9jdTdhUlllcXVkZDNrKzNEV1ZxeHVwSEloRVQ4NHZFVzRDdHRTVlZ1dEIvczVvdzVpVGc9PQ%26EMAP_LANG%3Dzh%26THEME%3Dindigo%23%2FdailyReport')
        driver.maximize_window()
        driver.find_element_by_id('username').send_keys(self.cfg.user_id)  # 一卡通号
        driver.find_element_by_id('password').send_keys(self.cfg.password)  # 密码
        driver.find_element_by_xpath('//*[@class="auth_login_btn primary full_width"]').click()        

        status = "failed"
        try:
            WebDriverWait(driver, 30, 0.2).until(lambda x:x.find_element_by_xpath('//*[@class="bh-btn bh-btn-primary"]'))
            driver.find_element_by_xpath('//*[@class="bh-btn bh-btn-primary"]').click()

            WebDriverWait(driver, 30, 0.2).until(lambda x:x.find_element_by_name('DZ_JSDTCJTW'))
            driver.find_element_by_name('DZ_JSDTCJTW').send_keys('36.5')
            driver.find_element_by_id('save').click()

            WebDriverWait(driver, 30, 0.2).until(lambda x:x.find_element_by_xpath('//*[@class="bh-dialog-btn bh-bg-primary bh-color-primary-5"]'))
            driver.find_element_by_xpath('//*[@class="bh-dialog-btn bh-bg-primary bh-color-primary-5"]').click()
            status = "successful"
        except: 
            pass
        
        if self.cfg.notification == "yes":
            if self.cfg.notify_failure_only == "no":
                self.send_email(status)
            elif status == "failed":
                self.send_email(status)

        driver.close()

    def send_email(self, message):
        """发送打卡状态至预定义的邮箱.

        Args:
            msg: str.
        """
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['From'] = self._format_addr("Physical condition reporter {}".format(self.cfg.from_addr))
        msg['To'] =self. _format_addr("Admin {}".format(self.cfg.to_addr))
        msg['Subject'] = Header("SEU daily report", "utf-8").encode()

        server = smtplib.SMTP(self.cfg.smtp_server, 25) # SMTP协议默认端口是25
        server.login(self.cfg.from_addr, self.cfg.email_password)
        server.sendmail(self.cfg.from_addr, [self.cfg.to_addr], msg.as_string())
        server.quit()

    def _format_addr(self, s):
        """格式化地址.

        Args:
            s: str, 类似"Physical condition reporter <xxx@seu.edu.cn>"

        Returns:
            str, 类似"'=?utf-8?q?Physical condition reporter?= <xxx@seu.edu.cn>'"
        """
        name, addr = parseaddr(s)

        return formataddr((Header(name, 'utf-8').encode(), addr))


if __name__ == '__main__':
    rh = ReportingHelper()
    rh.run()