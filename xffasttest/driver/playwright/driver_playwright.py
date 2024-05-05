
from xffasttest.common import Dict
from playwright.sync_api import sync_playwright

DEFAULT_CONTEXT = 'DEFAULT_CONTEXT'
NEW_CONTEXT = 'NEW_CONTEXT'

class PlaywrightDriver(object):

    def __init__(self) -> None:
        playwright = sync_playwright().start()
        self.driver: object = None
        self.playwright: object = playwright
        self.browser: object = None
        self.browser_context: object = None
        self.browser_page: object = None
        self.browser_contexts: dict = {}
        self.config: dict = {}
    
    def _create_browser(self, config: dict) -> object:
        browser_name = config.browser_name or 'chromium'
        headless = config.headless
        slow_mo = config.slow_mo
        downloads_path = config.downloads_path
        browser = self.playwright[browser_name].launch(headless = headless, # type: ignore
                                                       downloads_path = downloads_path,
                                                       slow_mo = slow_mo)
        return browser
        
    def _create_context(self, config: dict) -> object:
        ignore_https_errors = config.ignore_https_errors
        java_script_enabled = config.java_script_enabled
        bypass_csp = config.bypass_csp
        viewport = config.viewport
        locale = config.locale or 'zh-CN'
        extra_http_headers = config.extra_http_headers
        record_video_dir = config.record_video_dir
        context = self.browser.new_context(ignore_https_errors = ignore_https_errors,
                                           java_script_enabled = java_script_enabled,
                                           bypass_csp = bypass_csp,
                                           viewport = dict(viewport) if viewport else None,
                                           locale = locale,
                                           extra_http_headers = extra_http_headers,
                                           record_video_dir = record_video_dir)
        return context

    def init_window(self, config: dict) -> None:
        browser_config: dict = config.browser
        context_config: dict = config.context
        
        self.config = config
        self.browser = self._create_browser(browser_config)
        self.browser_context = self._create_context(context_config)

        page = self.browser_context.new_page()
        self.browser_page = page
        self.browser_contexts.update({DEFAULT_CONTEXT: self.browser_context})
    
    def goto(self, url: str) -> None:
        self.browser_page.goto(url)
        self.browser_page.wait_for_load_state()

    def new_page(self, url: str) -> None:
        page = self.browser_context.new_page()
        self.browser_page = page
        self.goto(url)
    
    def new_window(self, context_key: str = NEW_CONTEXT, config: dict = {}) -> None:
        new_config = Dict({**self.config.context, **config.get('context')})
        context = self._create_context(new_config)
        self.browser_context = context
        self.browser_contexts.update({context_key: context})

    def video(self) -> str:
        return self.browser_page.video.path()

    def close(self) -> str:
        self.browser_page.close()
        self.browser_context.close()
        self.browser.close()

    def stop(self) -> None:
        self.playwright.stop()

    def screenshot(self, path: str, full_page: bool = True) -> None:
        self.browser_page.screenshot(path = path, full_page = full_page)

playwright = PlaywrightDriver()