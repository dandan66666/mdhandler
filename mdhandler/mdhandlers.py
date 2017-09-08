# coding: utf-8

"""
    author: lushijuan<243050994@qq.com>
    created_at: 2017-09-05
    updated_at: 2017-09-05
"""

from collections import deque
from array import array
from abc import ABCMeta
import re

from .tags import *
from .splitters import *
from .taginfo import TagInfo

class MdHandler(object):
    def __init__(self, fp, outname="main.html"):
        self.symbols = '\\`*_{}()[]#+-.!'
        self.flag = ''
        self.fp = fp
        self.line = None
        self.outname = outname
        self.block_end = False
        self.init_html()
        self.init_before_stack()

    def init_html(self):
        self.html = HTML()
        self.html.append(Head())
        self.body = Body()
        self.html.append(self.body)

    def init_before_stack(self):
        self.before = deque()
        self.before.append(self.html)
        self.before.append(self.body)

    def run(self):
        with open(self.fp, 'r') as fp:
            for line in fp:
                if line.strip() == '':
                    self.handle_block_end()
                    self.block_end = True
                else:
                    self.block_end = False
                    self.line = deque(line)
                    self.handle_line()

    def handle_title(self):
        num = 0
        while self.line[0] == '#':
            num += 1
            self.line.popleft()
        if self.line[0] == ' ':
            self.line.popleft()
        title = Title(num)
        self.before[-1].append(title)
        self.before.append(title)

    def get_list_flags(self):
        a = []
        u = self.is_unordered_list_flag()
        o = self.is_ordered_list_flag()
        while u or o:
            if u:
                a.append(False)
            if o:
                a.append(True)
            u = self.is_unordered_list_flag()
            o = self.is_ordered_list_flag()
        return a

    def find_same_start_str(self, a, b):
        len_ = min(len(a), len(b))
        for i in range(0, len_):
            if a[i] != b[i]:
                return a[:i]
        return a[:len_]

    def pop_before_listitem_with_list(self):
        '''
        For each listitem to be added, before stack last two item is 'List' and 'ListItem'
        In order to end this 'List' block, should pop 2 items
        :return:
        '''
        self.before.pop()
        self.before.pop()

    def push_before_listitem_with_list(self, parents, ordered=False):
        lt = OrderedList() if ordered else UnOrderedList()
        li = ListItem(lt, parents)
        self.before[-1].append(lt)
        self.before.append(lt)
        self.before.append(li)


    def handle_list(self):
        a = self.get_list_flags()
        if isinstance(self.before[-1], ListItem):
            bp = self.before[-1].parents
            if a == bp:
                li = ListItem(self.before[-1].parent, bp)
                del a
                self.before.pop()
                self.before.append(li)
            else:
                subs = self.find_same_start_str(a, bp)
                for i in range(0, len(bp)-len(subs)):
                    self.pop_before_listitem_with_list()
                for i in range(len(subs), len(a)):
                    p = getattr(self.before[-1], 'parents', [])
                    self.push_before_listitem_with_list(p+[a[i]], a[i])
        else:
            for index, item in enumerate(a):
                self.push_before_listitem_with_list(a[:index+1], item)

    def is_unordered_list_flag(self, pop=True):
        if len(self.line) < 2:
            return False
        if self.line[0] in ['*', '+', '-'] and self.line[1] == ' ':
            if pop:
                self.line.popleft()
                self.line.popleft()  # pop space
            return True
        return False

    def is_ordered_list_flag(self, pop=True):
        if re.search('^\d+\. ', ''.join(self.line)) is not None:
            if pop:
                temp = self.line.popleft()
                while temp != '.':
                    temp = self.line.popleft()
                self.line.popleft()  # pop space
            return True
        return False

    def handle_block_end(self):
        while isinstance(self.before[-1], List) or isinstance(self.before[-1], Code) or \
                isinstance(self.before[-1], Table):
            self.before.pop()

    def handle_code(self):
        if not isinstance(self.before[-1], Code):
            code = Code()
            code.append(''.join(self.line))
            self.before[-1].append(code)
            self.before.append(code)
        else:
            self.before[-1].append('\n'+''.join(self.line))

    def get_func(self, name):
        return getattr(self, 'handle_'+name, None)

    def get_match_flag(self):
        '''
        if len(match_flag) == 2, temp = match_flag[0]
        else temp = ''
        match_flag can be '[', '![', '](', ')', '*', '_', '**', '__', '`'
        if match nothing, return None
        :return:
        '''
        temp = ''
        if self.line[0] in TagInfo.ces_tags:
            if len(self.line) > 1 and self.line[1] == self.line[0]:
                temp = self.line.popleft()
        elif self.line[0] == '[' or self.line[0] == ')':
            pass
        elif len(self.line) > 1 and self.line[0] == '!' and self.line[1] == '[' or self.line[0] == ']' and self.line[1] == '(':
            temp = self.line.popleft()
        elif self.line[0] == '\\':   # handle escape meaningful flag
            self.line.popleft()
            return None
        else:
            return None
        return temp+self.line.popleft()

    def handle_inline(self):
        '''
        For now, '\n' is end of line
        em, strong, code, image, link does not work if change line
        :return:
        '''
        self.pop_left_space()
        if self.line[-1] == '\n':
            self.line.pop()  # pop '\n'
        if self.line[0] == '>':  # handle code block
            self.line.popleft()
            return self.handle_code()
        d = {}
        temp = deque()
        while self.line:
            match_flag = self.get_match_flag()
            if match_flag is None:  # handle other characher
                temp.append(self.line[0])
                self.line.popleft()
                continue

            if match_flag in TagInfo.ces_tags:  # handle em, strong and code flag
                if match_flag in d:  # right flag
                    l = d[match_flag]
                    last = self.get_items_from_deque_right(temp, l)
                    func = self.get_func(TagInfo.ces_tags[match_flag])
                    tag = func(last)
                    temp.append(tag)
                    del d[match_flag]
                else:   # left flag
                    d[match_flag] = len(temp)
                    temp.append(match_flag)

            elif match_flag == ')':  # handle end of link or image
                link_pos = d.get('[', -1)
                img_pos = d.get('![', -1)
                mid_pos = d.get('](', -1)
                # unless link_pos == img_pos == -1, link_pos is not equal to img_pos
                if mid_pos == -1 or link_pos == img_pos:
                    temp.append(')')
                    continue
                if img_pos > link_pos:
                    type, s = 'image', img_pos
                    del d['![']
                else:
                    type, s = 'link', link_pos
                    del d['[']
                del d['](']
                self.is_image_or_link(type, s, mid_pos, temp)
            elif match_flag == '](':  # handle middle of link or image
                if '[' in d or '![' in d:
                    d[match_flag] = len(temp)
                temp.append(match_flag)
            else:                    # handle begin of link or image
                d[match_flag] = len(temp)
                temp.append(match_flag)

        # push inline tags into parent tag
        if len(temp) == 1:
            self.before[-1].append(temp.popleft())
        else:
            lists = self.get_items_from_deque_right(temp, 0, True)
            self.before[-1].extend(lists)

    def get_items_from_deque_right(self, temp, pos, without_start_tag=False):
        pace = len(temp)-pos if without_start_tag else len(temp)-pos-1
        outs = deque()
        arr = array('c')
        while pace:
            s = temp.pop()
            if isinstance(s, str):
                arr.append(s)
            else:
                if arr:
                    arr.reverse()
                    outs.appendleft(''.join(arr))
                    arr = array('c')
                outs.appendleft(s)
            pace -= 1
        if arr:
            arr.reverse()
            outs.appendleft(''.join(arr))
        if without_start_tag is False:
            temp.pop()
        if len(outs) == 1:  # mean only have a string
            return outs[0]
        return outs

    def is_image_or_link(self, type, s, m, temp):
        url = self.get_items_from_deque_right(temp, m)
        text = self.get_items_from_deque_right(temp, s)
        func = self.get_func(type)
        tag = func(text, url)
        temp.append(tag)

    def handle_inline_tag(self, contents, cls):
        tag = cls()
        for content in contents:
            tag.append(content)
        return tag

    def handle_em(self, contents):
        return self.handle_inline_tag(contents, Em)

    def handle_strong(self, contents):
        return self.handle_inline_tag(contents, Strong)

    def handle_inline_code(self, contents):
        return self.handle_inline_tag(contents, Code)

    def handle_image(self, text, url):
        return Image(text, url)

    def handle_link(self, text, url):
        return Link(text, url)

    def handle_table(self):
        pass

    def handle_next_line(self):
        while isinstance(self.before[-1], ListItem):
            self.before.pop()

    def handle_hr(self):
        while not isinstance(self.before[-1], Body):
            self.before.pop()
        self.body.append(SplitLine())

    def pop_left_space(self):
        while self.line and self.line[0] in [' ', '\t']:
            self.line.popleft()

    def handle_line(self):
        # handle special condition -- Code
        if isinstance(self.before[-1], Code) and self.line[0] != '\n':
            self.before[-1].append(''.join(self.line))
            return

        self.pop_left_space()
        if self.line is None:
            return
        if self.line[0] == '#':
            self.handle_title()
        elif self.is_unordered_list_flag(False) or self.is_ordered_list_flag(False):
            self.handle_list()
        elif self.line in ['***', '___', '---']:
            self.handle_hr()
            return

        self.handle_inline()

    def save_to_html(self):
        with open(self.outname, 'w') as fp:
            fp.write(str(self.html))

