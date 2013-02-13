#!/usr/bin/env python

import os
import sys

def add_python_site_packages_to_sys_path ():
    this_dir = os.path.dirname(__file__)
    packages_path = '.venv/lib/python2.7/site-packages'
    site_packages_dir = '{0}/{1}'.format(this_dir, packages_path) 
    sys.path.insert(0, this_dir)
    sys.path.insert(0, site_packages_dir)

add_python_site_packages_to_sys_path()

from flask import Flask, abort, request, redirect, url_for, render_template, g
from markdown import markdown
import codecs
app = Flask(__name__)

class MarkdownParser:
    
    def __init__(self, custom_options=None):
        self.options = self._get_default_options()
        if custom_options:
            self.options = self.options.update(custom_options)

    def _get_default_options(self):
        options = {
            "output_format": "html5",
            "safe_mode": "escape"
        }
        return options

    def parse(self, unicode_text):
        parsed_html = markdown(unicode_text, **self.options)
        return parsed_html

class FileReader:

    def read(self, file_path):
        input_file = codecs.open(file_path, mode="r", encoding="utf-8")
        unicode_text = input_file.read()
        return unicode_text

@app.route('/')
def hello_world():
    test_file_path = "readme.md"
    unicode_text = FileReader().read(test_file_path)
    markdown_parser = MarkdownParser()
    html_content = markdown_parser.parse(unicode_text)
    nav_items = ["one", "two", "three"]
    templatevars = {
        "content": html_content,
        "nav_items": nav_items
    }
    return render_template('page.html', **templatevars)

if __name__ == '__main__':
    app.jinja_env.line_statement_prefix = '%'
    # app.debug = True
    app.run()
