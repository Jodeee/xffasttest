#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
from xffasttest.common import Dict, DictEncoder
from jinja2 import Environment, FileSystemLoader

RANGES_COLOR = [
    (0, 60, 'color-errors'),
    (61, 80, 'color-failures'),
    (81, 100, 'color-success')
]
class TestReports(object):

    def __init__(self, testresult = None) -> None:

        self.total = len(testresult.result)
        self.errors = len(testresult.errors)
        self.failures = len(testresult.failures)
        self.skipped = len(testresult.skipped)
        self.success = self.total - self.errors - self.failures - self.skipped
        self.duration = testresult.duration
        self.passrate = (self.success / self.total) * 100
        self.reports = testresult.reports
        self.passrate_color = 'color_default'
        for low, high, color in RANGES_COLOR:
            if low <= self.passrate <= high:
                self.passrate_color = color

        self.summary = {
            'total': self.total,
            'errors': self.errors,
            'failures': self.failures,
            'skipped': self.skipped,
            'success': self.success,
            'duration': self.duration,
            'passrate': self.passrate,
            'reports': self.reports,
            'passrate_color': self.passrate_color
        }
        self.report_data = Dict({
            'summary': self.summary,
            'tests': self._parse_report_(testresult.result)
        })
        
    def _parse_report_(self, results: list) -> Dict:
        
        data = {}
        for result in results:
            file_name = result.file_name.strip('.py')
            key = f'{result.case_module}/{file_name}'
            if key not in data:
                data[key] = Dict({
                    'path': key,
                    'cases': [],
                    'total': 0,
                    'success': 0,
                    'errors': 0,
                    'failures': 0,
                    'skipped': 0,
                    'duration': 0.0,
                })
            
            data[key].cases.append(result.__dict__)
            data[key]['total'] += 1
            data[key]['duration'] += round(result.duration, 2)
            
            if result.status == 0: data[key]['success'] += 1
            if result.status == 1: data[key]['failures'] += 1
            if result.status == 2: data[key]['errors'] += 1
            if result.status == 3: data[key]['skipped'] += 1
            data[key]['passrate'] = (data[key].success / data[key].total) * 100

        return list(data.values())
    
        
    def generate_reports(self) -> None:
        
        json_data = json.dumps(self.report_data, cls=DictEncoder, indent=4)
        with open(os.path.join(self.reports, 'reports.json'), 'w', encoding='utf-8') as json_file:
            json_file.write(json_data)
        

        resource = os.path.join(os.path.split(os.path.abspath(__file__))[0], "resource")
        env = Environment(loader=FileSystemLoader(resource))

        template = env.get_template('reporter.html')

        rendered_html = template.render(json.loads(json_data))

        with open(os.path.join(self.reports, 'reports.html'), 'w', encoding='utf-8') as html_file:
            html_file.write(rendered_html)