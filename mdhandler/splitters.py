# coding: utf-8

"""
    author: lushijuan<243050994@qq.com>
    created_at: 2017-09-05
    updated_at: 2017-09-05
"""


class Splitter(object):
    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        return '<'+ self.tag + ' />'


class SplitLine(Splitter):
    def __init__(self):
        super(SplitLine).__init__(True)
        self.tag = 'hr'


class NextLine(Splitter):
    def __init__(self):
        super(NextLine).__init__(True)
        self.tag = 'br'
