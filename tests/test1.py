import os.path
import unittest

from xffasttest import TestCase, driver, gvar
import  re
import asyncio
import  time
from playwright.sync_api import Page, expect
from playwright.sync_api import sync_playwright

class MyTestCase1(TestCase):

    def test_zget_started_link(self):
        print('---------')

    def test_get_started_link(self):
        '''
        sdf sdfasf s
        :return:
        '''

        driver.goto('https://www.baidu.com')

        driver.new_page('https://www.yuque.com')

        config = {
            'context': {
                'viewport': {"width": 1920, "height": 1080}
            }

        }
        driver.new_window('NEW_WINDOW1', config)
        driver.new_page('https://www.alipay.com')
        time.sleep(2)

