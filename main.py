import smtplib, time
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
from random import random
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from personal_information import Info

class ReportingHelper:
    def __init__(self):
        self.cfg = Info

    def _random_temp(self) -> float:
        """Generate random normal body temperature. [36.2, 36.7]

        Returns:
            float, normal body temperature
        """
        lb = 36.2
        x = random(round(random() / 2, 1))  # [0, 0.5]
        return lb + x

    def run(self):
        options = Options()
        options.add_argument("--headless") # headless browser
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")


        driver = Chrome(
            service = Service(self.cfg.chrome_driver_path),
            options = options
        )

        driver.get('https://newids.seu.edu.cn/authserver/login?service=http%3A%2F%2Fehall.seu.edu.cn%2Fqljfwapp2%2Fsys%2FlwReportEpidemicSeu%2Findex.do%3Ft_s%3D1594447890898%26amp_sec_version_%3D1%26gid_%3DSTZiVXZjRnhVSS9VNERWaFNNT1hXb2VNY3FHTHFVVHMwRC9jdTdhUlllcXVkZDNrKzNEV1ZxeHVwSEloRVQ4NHZFVzRDdHRTVlZ1dEIvczVvdzVpVGc9PQ%26EMAP_LANG%3Dzh%26THEME%3Dindigo%23%2FdailyReport')
        driver.find_element(By.ID, 'username').send_keys(self.cfg.user_id)  # student ID
        driver.find_element(By.ID, 'password').send_keys(self.cfg.password)  # password
        driver.find_element(By.XPATH, '//*[@class="auth_login_btn primary full_width"]').click()

        status = ""
        try:
            WebDriverWait(driver, 15, 0.2).until(lambda x:x.find_element(By.XPATH, '//*[@class="bh-btn bh-btn-primary"]'))
            driver.find_element(By.XPATH, '//*[@class="bh-btn bh-btn-primary"]').click()
            WebDriverWait(driver, 15, 0.2).until(lambda x:x.find_element(By.NAME, 'DZ_JSDTCJTW'))
            driver.find_element(By.NAME, 'DZ_JSDTCJTW').send_keys(str(self._random_temp()))
            driver.find_element(By.ID, 'save').click()

            WebDriverWait(driver, 15, 0.2).until(lambda x:x.find_element(By.XPATH, '//*[@class="bh-dialog-btn bh-bg-primary bh-color-primary-5"]'))
            driver.find_element(By.XPATH, '//*[@class="bh-dialog-btn bh-bg-primary bh-color-primary-5"]').click()
            status = "successful"
        except Exception as e:
            status = "failed"
            print(str(e))
        
        if self.cfg.notification == "yes":
            if self.cfg.notify_failure_only == "no":
                self.send_email(status)
            elif status == "failed":
                self.send_email(status)

        driver.close()
        print(time.strftime("%Y-%m-%d %H:%M:%S -", time.localtime()), status)

    def send_email(self, message):
        """Sand email to predefined mailbox.

        Args:
            msg: str.
        """
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['From'] = self._format_addr("Physical condition reporter {}".format(self.cfg.from_addr))
        msg['To'] =self. _format_addr("Admin {}".format(self.cfg.to_addr))
        msg['Subject'] = Header("SEU daily report", "utf-8").encode()

        server = smtplib.SMTP(self.cfg.smtp_server, 25) # SMTP port: 25
        server.login(self.cfg.from_addr, self.cfg.email_password)
        server.sendmail(self.cfg.from_addr, [self.cfg.to_addr], msg.as_string())
        server.quit()

    def _format_addr(self, s):
        """Formatting address.

        Args:
            s: str, like "Physical condition reporter <xxx@seu.edu.cn>"

        Returns:
            str, like "'=?utf-8?q?Physical condition reporter?= <xxx@seu.edu.cn>'"
        """
        name, addr = parseaddr(s)

        return formataddr((Header(name, 'utf-8').encode(), addr))


if __name__ == '__main__':
    print(time.strftime("%Y-%m-%d %H:%M:%S -", time.localtime()), "start")
    rh = ReportingHelper()
    rh.run()