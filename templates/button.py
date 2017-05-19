"""
The MIT License (MIT)

Copyright (c) 2016 Swapnil Agarwal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from copy import deepcopy as copy

from text import TextTemplate
TextTemplate.get_text = lambda self: self.get_message()['text']

TEXT_CHARACTER_LIMIT = 320

template = {
    'template_type': 'button',
    'value': {
        'attachment': {
            'type': 'template',
            'payload': {
                'template_type': 'button',
                'text': '',
                'buttons': []
            }
        }
    }
}


class ButtonTemplate:
    def __init__(self, text=''):
        self.template = copy(template['value'])
        self.text = text

    def add_web_url(self, title='', url=''):
        web_url_button = dict()
        web_url_button['type'] = 'web_url'
        web_url_button['title'] = title
        web_url_button['url'] = url
        self.template['attachment']['payload']['buttons'].append(web_url_button)

    def add_postback(self, title='', payload=''):
        postback_button = dict()
        postback_button['type'] = 'postback'
        postback_button['title'] = title
        postback_button['payload'] = payload
        self.template['attachment']['payload']['buttons'].append(postback_button)

    def set_text(self, text=''):
        self.text = text

    def get_message(self):
        self.template['attachment']['payload']['text'] = self.text
        return self.template

    def get_buttons(self):
        return self.template['attachment']['payload']['buttons']
