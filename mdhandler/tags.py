# coding: utf-8

"""
    author: lushijuan<243050994@qq.com>
    created_at: 2017-09-05
    updated_at: 2017-09-05
"""

from array import array

from .attrs import Attrs, Style
from splitters import  Splitter

class Tag(object):
    def __init__(self, single=False):
        self.tree = []
        self.attrs = Attrs({'style': Style()})
        self._array = []
        self._str = None
        self.tag = None
        self.single = single

    # set attr
    def __setitem__(self, key, value):
        self.attrs[key] = value

    # get attr
    def __getitem__(self, key):
        return self.attrs.get(key, '')

    # delete attr
    def __delitem__(self, key):
        self.attrs.pop(key)

    def children(self, index):
        return self.tree[index]

    def _start_tag(self):
        if len(self.attrs) != 0:
            self._array.append('<'+self.tag+' '+str(self.attrs))
        else:
            self._array.append('<'+self.tag)
        if self.single:
            self._array.append(' />')
        else:
            self._array.append('>')

    def _end_tag(self):
        if self.single:
            return ''
        else:
            self._array.append('</'+self.tag+'>')

    def _handle_child_tag(self, tag):
        if isinstance(tag, Tag):
            self._array.append(str(tag))
        elif isinstance(tag, str):
            self._array.append(tag)
        else:
            raise ValueError('%s is kind of %s, not String or Tag.' % (tag, type(tag)))

    def __str__(self):
        '''
        String is immutable, in order to enhance performance,
        create a temp array, self._array.
        after finish, delete temp array.
        :return: string
        '''
        if self._str is not None:
            return self._str
        self._start_tag()
        for tag in self.tree:
            self._handle_child_tag(tag)
        self._end_tag()

        self._str = ''.join(self._array)
        del self._array
        return self._str

    def append(self, tag):
        if isinstance(tag, Tag) or isinstance(tag, Splitter) or isinstance(tag, str):
            self.tree.append(tag)
        else:
            raise ValueError('%s is kind of %s, not String or Tag.' % (tag, type(tag)))

    def extend(self, lists):
        self.tree.extend(lists)


class List(Tag):
    def __init__(self):
        super(List).__init__()
        self.depth = 1

    def _handle_child_tag(self, tag):
        if not isinstance(tag, ListItem):
            raise SyntaxError("Children of OrderedList must be ListItem.")
        self._array.append(str(tag))


class OrderedList(List):
    def __init__(self):
        super(OrderedList, self).__init__()
        self.tag = 'ol'


class UnOrderedList(List):
    def __init__(self):
        super(UnOrderedList, self).__init__()
        self.tag = 'ul'


class ListItem(Tag):
    def __init__(self, parent, parents):
        super(ListItem, self).__init__()
        self.tag = 'li'
        self.parent = parent
        self.parent.append(self)
        self.parents = parents


class Title(Tag):
    def __init__(self, flag):
        super(Title, self).__init__()
        self.tag = 'h'+str(flag)


class Table(Tag):
    def __init__(self):
        super(Table, self).__init__()
        self.tag = 'table'
        self.text_align = 'left'

    def set_alignment(self, s=':--:'):
        if s[1] == ':' and s[-1] == ':':
            self.text_align = 'center'
        elif s[-1] == ':':
            self.text_align = 'right'

    # def append(self, tr):
    #     tr['text-align'] = self.text_align
    #     super(Table).append(tr)


class TableRow(Tag):
    def __init__(self):
        super(TableRow, self).__init__()
        self.tag = 'tr'
        self.text_align = 'left'

    # def append(self, content):
    #     content['text-align'] = self.text_align


class TableHeader(Tag):
    def __init__(self, flag):
        super(TableHeader, self).__init__()
        self.tag = 'th'


class TableContent(Tag):
    def __init__(self):
        super(TableContent, self).__init__()
        self.tag = 'td'


class Image(Tag):
    def __init__(self, text, url):
        super(Image, self).__init__(True)
        self.tag = 'img'
        self['url'] = url
        self['alt'] = text


class Link(Tag):
    def __init__(self, text, url):
        super(Link, self).__init__()
        self.tag = 'a'
        self['href'] = url
        self.append(text)


class Em(Tag):
    def __init__(self):
        super(Em, self).__init__()
        self.tag = 'em'


class Strong(Tag):
    def __init__(self):
        super(Strong, self).__init__()
        self.tag = 'strong'


class Code(Tag):
    def __init__(self):
        super(Code, self).__init__()
        self.tag = 'code'


class BlockQuote(Tag):
    def __init__(self):
        super(BlockQuote, self).__init__()
        self.tag = 'blockquote'


class Delete(Tag):
    def __init__(self):
        super(Delete, self).__init__()
        self.tag = 'delete'


class HTML(Tag):
    def __init__(self):
        super(HTML, self).__init__()
        self.tag = 'html'

    def _start_tag(self):
        self._array.append('<!DOCTYPE html><html>')


class Head(Tag):
    def __init__(self):
        super(Head, self).__init__()
        self.tag = 'head'
        self.tree.append('<meta charset="utf-8">')


class Body(Tag):
    def __init__(self):
        super(Body, self).__init__()
        self.tag = 'body'

