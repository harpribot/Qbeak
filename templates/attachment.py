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

template = {
    'template_type': 'attachment',
    'value': {
        'attachment': {
            'type': 'file',
            'payload': {
                'url': ''
            }
        }
    }
}


class AttachmentTemplate:
    def __init__(self, url='', type='file'):
        self.template = template['value']
        self.url = url
        self.type = type

    def set_url(self, url=''):
        self.url = url

    def set_type(self, type=''):
        # image / audio / video / file
        self.type = type

    def get_message(self):
        self.template['attachment']['payload']['url'] = self.url
        self.template['attachment']['type'] = self.type
        return self.template
