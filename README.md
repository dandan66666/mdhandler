# Mdhandler

### 语言

python

### 目录

* mdhandler
* * mdhandler
  * * \__init__.py
    * attrs.py                    — Tag标签的属性（继承dict）
    * splitters.py              — 如\<hr /> 和 \<br />这类简单的html 分隔符
    * taginfo.py                —  markdown标志与html Tag标签的对应关系
    * tags.py                     —   各类Tag标签
    * mdhandlers.py       —  把markdown语法按行转换，形成Tag语法树



### 实现

* 把markdown语法按行转换，形成一棵Tag语法树
* 把Tag语法树转换成html语法



### 扩展的方向

* 利用形成的语法树可以实现类似BeautifulSoup的功能
* 利用包输出对应的pdf文件
* 改成js语言，动态交互，实时查看输入对应的输出效果



