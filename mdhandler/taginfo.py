# coding: utf-8

"""
    author: lushijuan<243050994@qq.com>
    created_at: 2017-09-05
    updated_at: 2017-09-05
"""


class TagInfo(object):
    tags = {}
    ces_tags = {'*': 'em', '_': 'em',
                   '**': 'strong', '__': 'strong', '`': 'inline_code'}
    al_tags = {'[': 'link', '![': 'image'}

    @classmethod
    def __set__(cls, tag, tagcls):
        TagInfo.tags[tag] =tagcls

    @classmethod
    def __get__(cls, tag):
        if tag in TagInfo.tags:
            return TagInfo.tags[tag]()
        return NotImplementedError('%s is not implemented.'%tag)
