#-*- coding: utf8 -*-
__author__ = 'dasolma'
from parser import *
from nltk import Tree
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget

sentences = ["¿ Como está la luz del dormitorio ?",
             "Enciende la luz de la cocina",
             "configura el aire acondicionado a 26 grados a las 6 pm hasta las 7:20 am",
             "Apaga el aire acondicionado",
             "Apaga el horno",
             "¿ Como está la puerta de la cocina ?",
             "Enciende el aire acondicionado"]


count = 1
for sent in sentences:
    print sent
    trees = parse(sent)
    if len(trees) == 0: print "No parser"
    else:
        for t in trees:
            cf = CanvasFrame()
            tc = TreeWidget(cf.canvas(),t)
            cf.add_widget(tc,10,10) # (10,10) offsets
            cf.print_to_file('tree%d.ps'%count)
            cf.destroy()
            count +=1

