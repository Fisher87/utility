#!/usr/bin/env python
# coding=utf-8

"""
funtions.
---------------------------------------
common using or utility functions set.

"""

"""
luandun.brief_scripts
--------------------------------------
   all brief utility functions set.
--------------------------------------
"""

######################################################
import re
""" delete html tags """
re_h      = re.compile('</?\w+[^>]*>', re.I)
re_blank  = re.compile(ur'\s+')
re_comment= re.compile('<!--[^>]*-->')
re_script =  re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I|re.S)

def delete_html_tags(html_body):
    body = re_script.sub('', html_body)
    body = re_comment.sub('', body)
    body = re_h.sub('', body)
    body = re_blank.sub('', body)
    return body

######################################################


######################################################
import datetime
""" time format transform """
def timeorstr(timeorstr):
    if isinstance(timeorstr, datetime.datetime) and \
       hasattr(timeorstr, 'strftime'):
        return timeorstr.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(timeorstr, basestring):
        return datetime.datetime.strptime(timeorstr, "%Y-%m-%d %H:%M:%S")
#######################################################


#######################################################
def quto_string(string, split_flag=None):
    """
    change str format:
        >>> string = 'title, topics, category, content'
        >>> qutostring = quto_string(string, split_flag=', ')
        >>> print '%r' %qutostring
        >>> "'title', 'topics', 'category', 'content'"
    """
    str_list = string.strip().split(split_flag) if split_flag else \
               string.strip().split()
    return "'" +  "', '".join(str_list) + "'"
#######################################################


#######################################################

def scatter(inputs, target_gpus, dim=0):
    r""" Duplicates references to objects.
    NOTE: 每个元素都拷贝复制
    refer: https://github.com/pytorch/pytorch/blob/4bd54cebe0b736acbcb8f040df897d17956bb71b/torch/nn/parallel/scatter_gather.py#L42
    """
    def scatter_map(obj):
        if isinstance(obj, tuple) and len(obj) > 0:
            return list(zip(*map(scatter_map, obj)))
        if isinstance(obj, list) and len(obj) > 0:
            return [list(i) for i in zip(*map(scatter_map, obj))]
        if isinstance(obj, dict) and len(obj) > 0:
            return [type(obj)(i) for i in zip(*map(scatter_map, obj.items()))]
        return [obj for targets in target_gpus]

    # After scatter_map is called, a scatter_map cell will exist. This cell
    # has a reference to the actual function scatter_map, which has references
    # to a closure that has a reference to the scatter_map cell (because the
    # fn is recursive). To avoid this reference cycle, we set the function to
    # None, clearing the cell
    try:
        res = scatter_map(inputs)
    finally:
        scatter_map = None
    return res

inputs = [[1, 2, 3], [4, 5, 6],[7,8,9], [0,0,0]]
target_gpus = [1,2]

l = scatter(inputs, target_gpus)
print(l)
print(id(l[0]))
print(id(l[1]))

m = [inputs] * len(target_gpus)
print(m)
print(id(m[0]))
print(id(m[1]))
m[0][0] = [-1, -1, -1]
print(m)
print(id(m[0]))
print(id(m[1]))
#######################################################
