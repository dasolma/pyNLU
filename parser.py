#-*- coding: utf8 -*-
__author__ = 'dasolma'

from tagger import *
from nltk.tree import Tree
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
from translater import *
from nltk import grammar, parse
import nltk

objects_and_sites = """
O[deviceReference=horno, devicePlace=cocina] -> 'horno'
O[deviceReference=luz] -> 'luz'
O[deviceReference=puerta] -> 'puerta'
O[deviceReference=aireAcondicionado] -> 'aire' 'acondicionado'

L[devicePlace=cocina] -> 'cocina'
L[devicePlace=dormitorio] -> 'dormitorio'
"""

go = """
% start ORDEN
ORDEN[ deviceOperation=setState, deviceReference=?a, deviceState=?s, devicePlace=?p] -> V[deviceState=?s, deviceReference=?a] DEVICE[deviceReference=?a, devicePlace=?p]
ORDEN[ deviceOperation=setState, deviceReference=?a, deviceState=?s, devicePlace=?p] -> V[deviceState=?s, deviceReference=?a] DEVICE[deviceReference=?a, devicePlace=?p]

DEVICE[deviceReference=?a, devicePlace=?p] -> O[deviceReference=?a] L[devicePlace=?p]
DEVICE[deviceReference=?a, devicePlace=?p] -> O[deviceReference=?a, devicePlace=?p]


V[deviceReference=?a,deviceState=0] -> 'apaga'
V[deviceReference=?a, deviceState=100] -> 'enciende'
V[deviceReference=persiana,deviceState=0] -> 'sube'
V[deviceReference=persiana, deviceState=100] -> 'baja'
""" + objects_and_sites

gq = u"""
% start QUESTION
QUESTION[ deviceOperation=getState, deviceReference=?a, devicePlace=?p] -> INT[] DEVICE[deviceReference=?a, devicePlace=?p]

DEVICE[deviceReference=?a, devicePlace=?p] -> O[deviceReference=?a] L[devicePlace=?p]
DEVICE[deviceReference=?a, devicePlace=?p] -> O[deviceReference=?a, devicePlace=?p]

INT[] -> 'INT'

""" + objects_and_sites

gs = u"""
% start SCHEDULE
SCHEDULE[ deviceOperation=setState, deviceReference=?a, devicePlace=?p, deviceProgram=?s] -> V[] DEVICE[deviceReference=?a, devicePlace=?p] PROGRAM[deviceProgram=?s, deviceReference=?a]

DEVICE[deviceReference=?a, devicePlace=?p] -> O[deviceReference=?a] L[devicePlace=?p]
DEVICE[deviceReference=?a, devicePlace=?p] -> O[deviceReference=?a, devicePlace=?p]


PROGRAM[deviceProgram=?s, deviceReference=?a] -> T[deviceProgram=?s, deviceReference=?a]

V[] -> 'configura' | 'programa' | 'prepara'

T[deviceProgram=?s, deviceReference=horno] -> 'nose'

""" + objects_and_sites



parser_orden = parse.FeatureEarleyChartParser(grammar.FeatureGrammar.fromstring(go))
parser_question = parse.FeatureEarleyChartParser(grammar.FeatureGrammar.fromstring(gq))
parser_schedule =  parse.FeatureEarleyChartParser(grammar.FeatureGrammar.fromstring(gs))

sites = ["cocina", "comedor", "salón", "salón comedor", "dormitorio" ]
devices = ["light", "blind", "door", "owen"]
actions_en = ["turn on", "turn of", "raise", "lower", "open", "close", "configure", "ask"]

words = ["turn_on", "turn_off", "raise", "lower", "open", "close", "configure", "ask", "state", "light", "blind", "door", "owen"]

#grammar = "COMO: {Como}"

mappings = { "acondicionado": "ams",
            }

type_mapping = {"n": ["n"],
                "v": ["vtr", "vi"],
                "a": ["adj"],
                "p": ["prep"],
                "i": ["pron"],
                "e": ["pron"],
                "d": ["def art"],
                "s": ["prep"]
                }

def parse(text):

    sentences = sent_tokenize(text)

    trees = []
    for s in sentences:

        s = word_tokenize(s)
        #NPChunker.parse( pos_tag(test_sent) ).draw()
        tags =  pos_tag(s)
        tags = [ (w, t) if not w in mappings else (w, mappings[w]) for w,t in tags ]
        relevant_words = [ w.lower().strip() for w, t in tags if t[0] in "inavZ"]

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

        relevant_words = [ w.lower().strip() for w, t in tags if t[0] in "inaZ"]
        relevant_words = [ w if w != '¿' else 'INT' for w in relevant_words]

        print relevant_words

        try:
            for t in  parser_question.parse(relevant_words):
                print t
        except:
            pass


        #print relevant_words


    return trees

sentences = ["Por favor configura el aire acondicionado a 26 grados a las  6pm",
             "Apaga el aire acondicionado",
             "Apaga el horno",
             "Enciende la luz de la cocina",
             "¿ Está la luz del dormitorio ?",
             "¿ Está la puerta de la cocina abierta ?",
             "por favor configura el aire acondicionado"]

sentences_otras = ["¿ Está la puerta de la cocina abierta ?",
             "¿ Está la luz del dormitorio encendida ?",
             "Por favor configura el aire acondicionado a 26 grados a las  6pm",
             "Programa el video para grabar a las 12:30",
             "Configura el video para grabar a las 12:30",
             "Prepara el video para grabar a las 12:30",
             "Enciende el horno",
             "Apaga la luz",
             "Apaga la luz de la cocina",
             "Él lo sabía",
            ]

for sent in sentences:
    for t in parse(sent):
        t.draw()

