__author__ = 'dasolma'
import dryscrape
import urllib
from lxml import html
import os.path
import pickle

translates = {}

if os.path.isfile("translates.pk"):
    translates = pickle.load(open("translates.pk"))

def translate(word, types=["vtr", "vi"]):
    w = word.lower()
    key = "_".join([w]+types)
    if key in translates:
        return translates[key].strip()

    url = "http://www.wordreference.com/es/en/translation.asp?spen=" + w
    session = dryscrape.Session()
    session.visit(url)
    response = session.body()
    tree = html.fromstring(response)

    for e in tree.xpath("//td[@class='ToWrd']".decode('latin1')):
        if is_type(e, types):
            translates[key] = e.text.strip()
            pickle.dump(translates, open("translates.pk", "wb"))
            return e.text.strip()

def is_type(e, types):
    for se in e.getchildren():
        if se.text in types: return True

    return False