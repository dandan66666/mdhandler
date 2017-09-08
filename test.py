# coding: utf-8

"""
    author: lushijuan<243050994@qq.com>
    created_at: 2017-09-07
    updated_at: 2017-09-07
"""

from collections import deque
from array import array

from mdhandler.mdhandlers import MdHandler

from unittest import TestCase
import unittest

class MdHandlerTest(TestCase):
    def setUp(self):
        self.handler = MdHandler(None)

    def tearDown(self):
        print str(self.handler.html)
        del self.handler

    def test_inline_with_str(self):
        self.handler.line = deque('\*slfkjd\_\n')
        self.handler.handle_inline()
        self.assertIn('*slfkjd_', str(self.handler.html))

    def test_inline_with_tags(self):
        self.handler.line = deque("*skd`dsfs`![dsf](d)fs)__dfdsf__jfld*\n")
        self.handler.handle_inline()
        self.assertIn('<em>skd<code>dsfs</code><img url="d" alt="dsf"  />fs)<strong>dfdsf</strong>jfld</em>',\
                      str(self.handler.html))

    def test_title_with_tags(self):
        self.handler.line = deque('##12*abc*\n')
        self.handler.handle_line()
        self.assertIn('<h2>12<em>abc</em></h2>', str(self.handler.html))


    # def test_get_list_flags(self):
    #     self.handler.line = deque('* 1. 1. + - ablkjsldfsd\n')
    #     arr = self.handler.get_list_flags()
    #     out = [False, True, True, False, False]
    #     self.assertListEqual(arr, out, '')

    def test_lists_with_tags(self):
        l = ["* lskdjfhhd\n", "* 1. fsdjflsda\n", "* 2. jklsdfhhsd", "* + sdlkhfh\n", "3. * + 1. fdjslkf"]
        for item in l:
            self.handler.line = deque(item)
            self.handler.handle_line()
        self.handler.save_to_html()





if __name__ == '__main__':
    unittest.main()
