# coding: utf-8

"""
    author: lushijuan<243050994@qq.com>
    created_at: 2017-09-07
    updated_at: 2017-09-07
"""

from collections import deque

from mdhandler.mdhandlers import MdHandler

def test_inline():
    handler = MdHandler(None)
    handler.line = deque("*skd`dsfs`![dsf](d)fs)__dfdsf__jfld*")
    handler.handle_inline()
    handler.save_to_html()

if __name__ == '__main__':
    test_inline()
