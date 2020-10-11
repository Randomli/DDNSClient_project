#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Henry  17607168727@163.com

import requests
from new_logger import logger, error_logger
from manage_config import get_config, set_config
import time


class SendWenXinMessage(object):
    """
    调动企业微信接口发送ddns自定义应用消息
    """
    def __init__(self):
        self.qy_weixin_id = get_config('message', 'qy_weixin_id')
        self.agent_id = get_config('message', 'agent_id')
        self.app_secret = get_config('message', 'app_secret')
        self.to_tag = get_config('message', 'to_tag')
        self.message_body = {
          "totag": self.to_tag,
          "msgtype": "text",
          "agentid": self.agent_id,
          "text": {"content": ""},
          "safe": 0,
          "enable_id_trans": 0,
          "enable_duplicate_check": 0
        }
        self.get_token_url = get_config('message', 'get_token_url')
        self.send_message_url = get_config('message', 'send_message_url')
        try:
            # 从配置中获取access_token
            self.access_token = get_config('message', 'access_token')
            self.token_ttl = get_config('message', 'token_ttl')
            # 判断超时时间
            if str(time.time()) > self.token_ttl:
                self.get_access_token()
        except Exception as error:
            error_logger.error("%s" % error)
            error_logger.error("从配置文件读取access_token失败,将重新获取")
            self.get_access_token()

    def get_access_token(self):
        """
        调用企业微信接口获取access_token
        """
        response = requests.get(url=self.get_token_url, params={"corpid": self.qy_weixin_id, "corpsecret": self.app_secret})
        r = response.json()
        if r["errcode"] == 0:
            self.access_token = r["access_token"]
            self.token_ttl = str(time.time()+r["expires_in"])
            set_config('message', 'access_token', self.access_token)
            set_config('message', 'token_ttl', self.token_ttl)
        else:
            error_logger.error("获取企业微信access_token失败")

    def send(self, message):
        """
        调用企业微信接口发送消息
        """
        self.message_body["text"]["content"] = message
        response = requests.post(url=self.send_message_url, params={"access_token": self.access_token}, json=self.message_body)
        r = response.json()
        if r["errcode"] == 0:
            error_logger.info("企业微信消息发送成功")
        else:
            error_logger.error("企业微信消息发送失败")