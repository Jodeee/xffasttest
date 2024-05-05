
import os
import sys
from xffasttest.common import action, gvar
from xffasttest.driver.playwright.driver_playwright import playwright

class Driver(object):

    def __init__(self) -> None:
        pass
    
    @staticmethod
    @action
    def init_window(config: dict = {}) -> None:
        playwright.init_window(config)

    @staticmethod
    @action
    def new_window(context_key: str = '', config: dict = {}) -> None:
        playwright.new_window(context_key = context_key, 
                              config = config)

    @staticmethod
    @action
    def new_page(url: str) -> None:
        playwright.new_page(url = url)

    @staticmethod
    @action
    def goto(url: str) -> None:
        playwright.goto(url = url)

    @staticmethod
    def close() -> None:
        playwright.close()

    @staticmethod
    @action
    def screenshot(path: str, full_page: bool = True) -> None:
        playwright.screenshot(path = path, full_page = full_page)
    
    @staticmethod
    def video() -> str:
        return playwright.video()
    
    @staticmethod
    def stop() -> None:
        playwright.stop()