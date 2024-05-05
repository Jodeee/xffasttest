import os
import sys
import shutil
import unittest
from xffasttest.utils import Utils
from xffasttest.common import gvar, logger, Dict
from xffasttest.runner import TestCase, TestRunner, TestLoader

DIRS = ['reports', 'common', 'resource', 'tests']

class FastTest:

    def __init__(self) -> None:
        self._load_config()
        self.hook_func = self._load_hook(self.hook_path)
        self.tests_suite = self._load_tests(self.hook_func)
        self.reports = ''

    def __setitem__(self, key, value) -> None:
        object.__setattr__(self, key, value)

    def __getitem__(self, name: str) -> object:
        try:
            value = self.__getattribute__(name)
            return value
        except:
            return None

    def _load_config(self) -> None:
        self.root = os.getcwd()
        sys.path.append(self.root)

        for _dir in DIRS:
            _path = os.path.join(self.root, _dir)
            self[_dir] = _path
            gvar[_dir] = _path
            sys.path.append(_path)

        # load config
        config_path = os.path.join(self.root, 'config.yaml')
        if not os.path.isfile(config_path):
            raise Exception(f'The file {config_path} does not exist.') 
        config = Utils.load_yaml(config_path)
        hook_path = config.hook
        self.hook_path = os.path.join(self.root, hook_path)
        gvar.config = config

        # laod reports
        logger.reports = self.reports
        if os.path.exists(self.reports):
            shutil.rmtree(self.reports)
        os.makedirs(self.reports)

    def _import_module(self, file: str) -> tuple:
        file_name: str = os.path.basename(file)
        file_path: str = os.path.dirname(file)
        sys.path.append(file_path)
        module = __import__(file_name[:-3])
        return (file_name, file_path, module)
        
    def _load_hook(self, hook_path) -> dict:
        if not os.path.isfile(hook_path): return 
        _, _, module = self._import_module(hook_path)
        set_up = module.setUp if 'setUp' in dir(module) else None
        tear_down = module.tearDown if 'tearDown' in dir(module) else None
        set_up_global = module.setUpGlobal if 'setUpGlobal' in dir(module) else None
        tear_down_global = module.tearDownGlobal if 'tearDownGlobal' in dir(module) else None
        return Dict({
            'set_up': set_up,
            'tear_down': tear_down,
            'set_up_global': set_up_global,
            'tear_down_global': tear_down_global
        })
        
    def _load_tests(self, hook_func: dict) -> list:
        tests_suite: list = []
        test_files: list[str] = Utils().traverse_dir(self.tests)

        for test_file in test_files:
            file_name, file_path, module = self._import_module(test_file)
            case_module = file_path.replace(f'{self.root}/', '')
            report_path = os.path.join(self.reports, case_module)
            if not os.path.exists(report_path):
                os.makedirs(report_path)

            for name in dir(module):
                test_case_ojb: type = getattr(module, name)
                if not isinstance(test_case_ojb, type): continue
                if not issubclass(test_case_ojb, TestCase): continue
                # load test cases
                test_case_ojb.case_info = Dict({
                    'file_name': file_name,
                    'case_module': case_module,
                    'report_path': report_path,
                    'reports': self.reports,
                    'set_up': hook_func.set_up,
                    'tear_down': hook_func.tear_down
                })
                test_case: unittest.suite.TestSuite = TestLoader().loadTestsFromTestCase(test_case_ojb)
                if test_case._tests: tests_suite.append(test_case)         
        return tests_suite

    def start(self) -> None:
        suite = unittest.TestSuite(tuple(self.tests_suite))
        runner = TestRunner(hook = self.hook_func)
        runner.run(suite)