#-*- coding: utf8 -*-
__author__ = 'dasolma'
from parser import *


sentences = ["¿ Está la luz del dormitorio ?",
             "Enciende la luz de la cocina",
             "configura el aire acondicionado a 26 grados a las 6:25 pm hasta las 7:20 am",
             "Apaga el aire acondicionado",
             "Apaga el horno",
             "¿ Está la puerta de la cocina abierta ?",
             "por favor configura el aire acondicionado"]



for sent in sentences:

    for t in parse(sent):
        t.draw()

