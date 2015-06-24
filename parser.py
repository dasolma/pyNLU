#-*- coding: utf8 -*-
__author__ = 'dasolma'

from tagger import *
from nltk.tree import Tree
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
from translater import *
from nltk import grammar, parse
import nltk
from grammar import *

parser_orden = parse.FeatureEarleyChartParser(grammar.FeatureGrammar.fromstring(go))
parser_question = parse.FeatureEarleyChartParser(grammar.FeatureGrammar.fromstring(gq))
parser_schedule =  parse.FeatureEarleyChartParser(grammar.FeatureGrammar.fromstring(gs))


def parse(text):

    sentences = sent_tokenize(text)

    trees = []
    for s in sentences:
        s = s.replace(":", " : ").replace("¿", "INT")
        s = word_tokenize(s)
        #NPChunker.parse( pos_tag(test_sent) ).draw()
        tags =  pos_tag(s)

        print tags
        relevant_words = [ w.lower().strip() for w, t in tags if t[0] in "inavZh"]

        print relevant_words
        try:
            for t in  parser_orden.parse(relevant_words):
                print t
        except:
            pass

        try:
            for t in  parser_schedule.parse(relevant_words):
                print t
        except:
            pass

        relevant_words = [ w.lower().strip() for w, t in tags if t[0] in "IinaZ"]

        print relevant_words

        try:
            for t in  parser_question.parse(relevant_words):
                print t
        except:
            pass


        #print relevant_words


    return trees


