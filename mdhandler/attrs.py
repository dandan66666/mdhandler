# coding: utf-8

"""
    author: lushijuan<243050994@qq.com>
    created_at: 2017-09-05
    updated_at: 2017-09-05
"""

from array import array

class Style(dict):
    def __str__(self):
        '''
        return style string -- style="color:red; float:left; "
        :return: string
        '''
        if len(self) == 0:
            return ''
        temp = []
        temp.append('style=\"')
        for key, value in self.items():
            temp.append(key + ':' + value + '; ')
        temp.append('\"')
        return ''.join(temp)

class Attrs(dict):
    def __str__(self):
        temp = []
        for key, value in self.items():
            if key != 'style':
                temp.append(key+'=\"'+value+'\" ')
            else:
                temp.append(str(value))
        return ''.join(temp)

