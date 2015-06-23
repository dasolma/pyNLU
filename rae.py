#-*- coding: utf8 -*-
__author__ = 'dasolma'

import dryscrape
import urllib
from lxml import html
from collections import defaultdict

BASE_URL = 'http://lema.rae.es/drae/srv/'
SEARCH_URL = 'http://lema.rae.es/drae/srv/search?val='

def parse_types(tree, tags):
    conj_url = tree.xpath("//span[@class='g']/span".decode('latin1'))
    for e in conj_url:
        if 'title' in e.attrib.keys():
            tags[e.attrib['title']] += 1

    conj_url = tree.xpath("//p[@class='q']/span".decode('latin1'))
    for e in conj_url:
        if 'title' in e.attrib.keys():
            tags[e.attrib['title']] += 1

    return tags

def get_def(session, word):
    word = word.decode('utf-8').lower()
    word = word.encode('latin1')
    w = urllib.quote(word)
    session.visit(SEARCH_URL + w)
    response = session.body()
    tree = html.fromstring(response)
    return tree


def rae_tag(word, session=None):
    if session is None:
        session = dryscrape.Session()


    try:
        tree = get_def(session, word)
        #take the button link

        conj_url = tree.xpath("//a/span[@class='f']/b".decode('latin1'))

        tags = defaultdict(int)
        if len(conj_url) > 0:
            for e in conj_url:
                tree = get_def(session, e.text.encode('utf-8'))
                parse_types(tree, tags)
        else:
            parse_types(tree, tags)

        return get_tag(max(tags, key=tags.get))

    except Exception as ex:
        print ex
        pass



    return ""

def get_tag(str):

    mappings = {'verbo transitivo': "v",
                u'locuci\xc3\xb3n verbal': 'v',
           "nombre femenino": "ncf",
           "nombre masculino": "ncm",
           "pronombre personal": "e"}

    if str in mappings.keys():
        return mappings[str]


    return str