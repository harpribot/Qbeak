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

TEXT_CHARACTER_LIMIT = 640

template = {
    'template_type': 'text',
    'value': {
        'text': ''
    }
}


class TextTemplate:
    def __init__(self, text='', post_text='', limit=TEXT_CHARACTER_LIMIT):
        self.template = template['value']
        self.text = text
        self.post_text = post_text
        self.limit = limit

    def set_text(self, text=''):
        self.text = text

    def set_post_text(self, post_text=''):
        self.post_text = post_text

    def set_limit(self, limit=TEXT_CHARACTER_LIMIT):
        self.limit = limit

    def get_message(self):
        n = self.limit - len(self.post_text)
        if n > len(self.text):
            self.template['text'] = self.text + self.post_text
        else:
            # append ellipsis (length = 3)
            self.template['text'] = self.text[:n-3].rsplit(' ', 1)[0] + '...' + self.post_text
        return self.template
