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

import re
######################################################
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


import datetime
######################################################
""" time format transform """
def timeorstr(timeorstr):
    if isinstance(timeorstr, datetime.datetime) and \
       hasattr(timeorstr, 'strftime'):
        return timeorstr.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(timeorstr, basestring):
        return datetime.datetime.strptime(timeorstr, "%Y-%m-%d %H:%M:%S")


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
