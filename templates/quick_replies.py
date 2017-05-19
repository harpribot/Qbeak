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

QUICK_REPLIES_LIMIT = 11
TITLE_CHARACTER_LIMIT = 20
PAYLOAD_CHARACTER_LIMIT = 1000


def add_quick_reply(message, title='', payload=''):
    message_with_quick_reply = copy(message)
    if 'quick_replies' not in message_with_quick_reply:
        message_with_quick_reply['quick_replies'] = []
    if len(message_with_quick_reply['quick_replies']) < QUICK_REPLIES_LIMIT:
        quick_reply = dict()
        # TODO: location + image_url
        quick_reply['content_type'] = 'text'
        quick_reply['title'] = title[:TITLE_CHARACTER_LIMIT]
        quick_reply['payload'] = payload[:PAYLOAD_CHARACTER_LIMIT]
        message_with_quick_reply['quick_replies'].append(quick_reply)
    return message_with_quick_reply
