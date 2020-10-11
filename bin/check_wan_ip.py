# -*- coding: utf-8 -*-
# Auther: Henry
# Email: 17607168727@163.com

import requests
from lxml import etree
from new_logger import logger, error_logger
from manage_config import get_config
from send_wexin_message import SendWenXinMessage


class UpdateDynamicIP:
    def __init__(self):
        self.check_url = get_config('main', 'check_url')
        self.log_data = get_config("log", "log_data")
        self.domain = get_config("main", "domain")
        self.passwd = get_config("main", "password")
        self.update_url = get_config("main", "update_url")
        self.wan_ip = ""
        self.sen_to_wx = SendWenXinMessage()
        self.get_wan_ip()

    def get_wan_ip(self):
        """
        获取wan ip
        :return:
        """
        try:
            response = requests.get(url=self.check_url)
            html = etree.HTML(response.text)
            text = html.xpath("/html/body/text()")[0]
            self.wan_ip = text.split(":")[1].strip()
            self.check_old_ip()
        except Exception as error:
            error_logger.error("%s" % (error))
            error_logger.error("获取wan IP失败")
            exit()

    def check_old_ip(self):
        """
        比对日志中的ip
        如果相同打印日志
        如果不同调用update()
        :return:
        """
        try:
            with open(self.log_data, 'r', encoding='utf-8') as f:
                last_line = f.readlines()[-1:]
                if last_line:
                    line_str = last_line[0]
                    # 判断self.get_wan_ip函数执行是否成功
                    if '->' in line_str:
                        ip = line_str.split("->")[1].strip()
                        if ip != self.wan_ip:
                            self.update()
        except Exception as error:
            message = "比对上一次检查时获取到的IP失败, %s" % (error)
            error_logger.error(message)
            self.sen_to_wx.send(message)
            exit()
        finally:
            self.save_ip()

    def save_ip(self):
        """
        记录每次获取到的wan ip和时间
        :return:
        """
        message = "获取到的wan IP -> %s" % (self.wan_ip)
        logger.info(message)

    def update(self):
        """
        更新A记录
        :return:
        """
        try:
            update_url = "http://%s:%s@%s" % (self.domain, self.passwd, self.update_url.split("//")[1])
            params_dic = {
                "hostname": self.domain,
            }
            response = requests.get(url=update_url, params=params_dic)
            error_logger.info(response.request.url)
            error_logger.info(response.text)
            msg = response.text.split(" ")[0]
            if msg not in ["nochg", "good"]:
                message = "修改解析记录失败, wan IP ->%s" % (self.wan_ip)
                error_logger.error(message)
                self.sen_to_wx.send(message)
                exit()
            else:
                message = "修改解析记录成功, wan IP ->%s" % (self.wan_ip)
                self.sen_to_wx.send(message)

        except Exception as error:
            error_logger.error("%s" % error)
            exit()


if __name__ == '__main__':
    UpdateDynamicIP()
