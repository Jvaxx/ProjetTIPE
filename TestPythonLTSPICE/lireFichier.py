from PyLTSpice.LTSpice_RawRead import LTSpiceRawRead
import numpy as np

def radToDeg(angle):
    if type(angle) == list:
        return list(map(lambda x: (x * 360) / (2*np.pi), angle))
    return (angle * 360) / (2*np.pi)

# Parametres generaux
celerite = 342
frequence = 300
longueurOnde = celerite/frequence
distanceEntreAntennes = longueurOnde/2


LTR = LTSpiceRawRead('heh.raw')


# Recuperation des listes de valeurs

amplitude1 = list(LTR.get_trace('V(sortiecrete1)'))[-1]
amplitude2 = list(LTR.get_trace('V(sortiecrete2)'))[-1]
amplitude3 = list(LTR.get_trace('V(sortiecrete3)'))[-1]
amplitudeFondamentalMult1 = list(LTR.get_trace('V(sortiepb1)'))[-1]
amplitudeFondamentalMult2 = list(LTR.get_trace('V(sortiepb2)'))[-1]

signal1 = np.array(list(LTR.get_trace('V(micro1)')))
signal2 = np.array(list(LTR.get_trace('V(micro2)')))
signal3 = np.array(list(LTR.get_trace('V(micro3)')))



correcteurMultiplieur = 1.13


# valeurs theoriques

mult1 = signal1 * signal2
mult2 = signal1 * signal3
fondamentalMult1 = (np.max(mult1[-len(mult1)//2:-1]) + np.min(mult1[-len(mult1)//2:-1])) / 2
fondamentalMult2 = (np.max(mult2[-len(mult2)//2:-1]) + np.min(mult2[-len(mult2)//2:-1])) / 2
amplitudeSignal1 = np.max(signal1[-len(signal1)//2:-1])
amplitudeSignal2 = np.max(signal2[-len(signal1)//2:-1])
amplitudeSignal3 = np.max(signal3[-len(signal1)//2:-1])
print(amplitudeSignal1, amplitudeSignal2, amplitudeSignal3)
print(fondamentalMult1, fondamentalMult2)

dephasagesTheo = [
    (np.arccos(2 * fondamentalMult1 /
        amplitudeSignal1*amplitudeSignal2)),
    (np.arccos(2 * fondamentalMult2 /
        amplitudeSignal1*amplitudeSignal3)),
]

directionsTheo = [
    (np.arcsin(-dephasagesTheo[0] * (longueurOnde / distanceEntreAntennes) /
        (2 * np.pi)) + np.pi/3),
    (-np.arcsin(-dephasagesTheo[0] * (longueurOnde / distanceEntreAntennes) /
        (2 * np.pi)) + np.pi/3),
    (np.arcsin(-dephasagesTheo[1] * (longueurOnde / distanceEntreAntennes) /
        (2 * np.pi)) - np.pi/3),
    (-np.arcsin(-dephasagesTheo[1] * (longueurOnde / distanceEntreAntennes) /
        (2 * np.pi)) - np.pi/3),
]




# en radians
dephasages = [
    (np.arccos(2 * amplitudeFondamentalMult1 * correcteurMultiplieur /
        (amplitude1*amplitude2))),
    (np.arccos(2 * amplitudeFondamentalMult2 * correcteurMultiplieur /
        (amplitude1*amplitude3))),
]



# en radians
directions = [
    (np.arcsin(-dephasages[0] * (longueurOnde / distanceEntreAntennes) /
        (2 * np.pi)) + np.pi/3),
    (-np.arcsin(-dephasages[0] * (longueurOnde / distanceEntreAntennes) /
        (2 * np.pi)) + np.pi/3),
    (np.arcsin(-dephasages[1] * (longueurOnde / distanceEntreAntennes) /
        (2 * np.pi)) - np.pi/3),
    (-np.arcsin(-dephasages[1] * (longueurOnde / distanceEntreAntennes) /
        (2 * np.pi)) - np.pi/3),
]


# for direc in directions:
#     print(radToDeg(direc))

# for deph in dephasages:
#     print(radToDeg(deph))

print('fondMult1Theo: ', fondamentalMult1)
print('fondMult2Theo: ', fondamentalMult2)
print('fondMult1Mes: ', amplitudeFondamentalMult1 * correcteurMultiplieur)
print('fondMult2Mes: ', amplitudeFondamentalMult2 * correcteurMultiplieur)

print('-----------------')

print('dephasagesTheo: ', radToDeg(dephasagesTheo[0]), radToDeg(dephasagesTheo[1]))
print('dephasagesMes', radToDeg(dephasages[0]), radToDeg(dephasages[1]))

print('-----------------')

print('DirectionsTheo :')
print(radToDeg(directionsTheo))
print('DirectionsMes: ')
print(radToDeg(directions))


print(radToDeg(np.arcsin(((-157.15*2*np.pi)/360) * (longueurOnde / distanceEntreAntennes) /
        (2 * np.pi)) + np.pi/3))

# 335.8454730127705 77.25686743221013 155.34436124761123

