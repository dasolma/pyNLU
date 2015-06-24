__author__ = 'dasolma'

objects_and_sites = """
O[deviceReference=horno, devicePlace=cocina] -> 'horno'
O[deviceReference=luz] -> 'luz'
O[deviceReference=puerta] -> 'puerta'
O[deviceReference=aireAcondicionado] -> 'aire' 'acondicionado'

L[devicePlace=cocina] -> 'cocina'
L[devicePlace=dormitorio] -> 'dormitorio'

U[deviceReference=horno] -> 'grados'
U[deviceReference=aireAcondicionado] -> 'grados'


"""

objects_and_sites += "\n"
for i in range(100):
    objects_and_sites += "NUM[num=%d] -> '%d'\n"%(i, i)


#hours
for i in range(12):
    objects_and_sites += "Hh[hour=%d] -> NUM[num=%d] 'pm'\n"%(i+12, i)

    objects_and_sites += "Hh[hour=%d] -> NUM[num=%d] 'p.m.'\n"%(i+12, i)

    objects_and_sites += "Hh[hour=%d] -> NUM[num=%d] 'am'\n"%(i, i)

    objects_and_sites += "Hh[hour=%d] -> NUM[num=%d] 'a.m.'\n"%(i, i)

    objects_and_sites += "Hm[hour=%d, minute=?m] -> NUM[num=%d] NUM[num=?m] 'pm'\n"%(i+12, i)

    objects_and_sites += "Hm[hour=%d, minute=?m] -> NUM[num=%d] NUM[num=?m] 'p.m.'\n"%(i+12, i)

    objects_and_sites += "Hm[hour=%d, minute=?m] -> NUM[num=%d] NUM[num=?m] 'am'\n"%(i, i)

    objects_and_sites += "Hm[hour=%d, minute=?m] -> NUM[num=%d] NUM[num=?m] 'a.m.'\n"%(i, i)


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

INT[] -> 'int'

""" + objects_and_sites

gs = u"""
% start SCHEDULE
SCHEDULE[ deviceOperation=setState, deviceReference=?a, devicePlace=?p, deviceProgram=?s] -> V DEVICE[deviceReference=?a, devicePlace=?p] PROGRAM[deviceProgram=?s, deviceReference=?a]

DEVICE[deviceReference=?a, devicePlace=?p] -> O[deviceReference=?a] L[devicePlace=?p]
DEVICE[deviceReference=?a, devicePlace=?p] -> O[deviceReference=?a, devicePlace=?p]

V -> 'configura' | 'programa' | 'prepara'


PROGRAM[deviceProgram=[targetState=?ts], deviceReference=aireAcondicionado] -> TS[targetState=?ts]
PROGRAM[deviceProgram=[startProgram=?sp, targetState=?ts], deviceReference=aireAcondicionado] -> TS[targetState=?ts] SP[startProgram=?sp]
PROGRAM[deviceProgram=[startProgram=?sp, endProgram=?ep, targetState=?ts], deviceReference=aireAcondicionado] -> TS[targetState=?ts] SP[startProgram=?sp] EP[endProgram=?ep]

TS[targetState=?ts] ->  NUM[num=?ts] U[deviceReference=aireAcondicionado]
TS[targetState=?ts] ->  NUM[num=?ts]

SP[startProgram=[hour=?h, minute=?m]] -> Hm[hour=?h, minute=?m]
SP[startProgram=[hour=?h]] -> Hh[hour=?h]
EP[endProgram=[hour=?h]] -> Hh[hour=?h]
EP[endProgram=[hour=?h, minute=?m]] -> Hm[hour=?h, minute=?m]


""" + objects_and_sites
