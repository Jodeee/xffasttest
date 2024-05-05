import os.path
import time
from xffasttest import driver, gvar

def setUpGlobal():
    print("setUpGlobal ----------")

def tearDownGlobal():
    print("tearDownGlobal")
    driver.stop()


def setUp(test):
    print(" --------- setUp", test._testMethodName)
    driver.init_window(gvar.config)

def tearDown(test):
    print(" --------- tearDown",test._testMethodName)
    try:
        screenshot_path = os.path.join(test.report_path, f'{time.time()}.png')
        driver.screenshot(path=screenshot_path)
        video_path = driver.video()
        print(video_path)

        test.screenshot_path = screenshot_path
        test.video_path = video_path
    except:
        pass
    driver.close()