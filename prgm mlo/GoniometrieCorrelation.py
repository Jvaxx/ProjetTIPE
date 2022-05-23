#executer en tant que script ( ctrl + shit + E sur pyzo)
import os
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
from math import *
import matplotlib.pyplot as plt
import Signaux
import KNNDelais
import AbaqueDelais

frequence = 300
K = 15 #a revoir
pas = 2#a revoir
EcartTypeBruit = 2
DureeSignal = 0.1
FrequenceEchantillonage = 20 * frequence

def convolution(Signal1: list, Signal2: list):
    print('a')
    M,N = len(Signal1), len(Signal2)
    Resultat = []
    
    for n in range(M+N-1):
        ValeurN =0
        for i in range(0,M):
            if (0 <= n-i < N):
                ValeurN += Signal1[i]*Signal2[n-i]
        Resultat.append(ValeurN)
    return Resultat

def IndexValeurMax(Liste:list):
    Max = max(Liste)
    indice = Liste.index(Max)
    return indice
    
    
def Delais(Signal1: list, Signal2: list, FrequenceEchantillonage:float):
    Liste1= Signal1[:]
    Liste2= Signal2[:]
    while len(Liste1) > len(Liste2):
        del Liste1[-1]
    while len(Liste2) > len(Liste1):
        del Liste2[-1]
    Liste2.reverse()
    ResultatCorrelationCroisee = convolution(Liste1, Liste2)
    IndiceMax = IndexValeurMax(ResultatCorrelationCroisee)
    Indice0 = len(ResultatCorrelationCroisee) // 2
    DiffTemps = abs(IndiceMax - Indice0)/FrequenceEchantillonage
    return DiffTemps
    
def CalculDirection(Abaque,Signaux,K,FrequenceEchantillonage):
    DiffTemps = []
    for i in range(1,6):
        DiffTemps.append(Delais(Signaux[0],Signaux[i],FrequenceEchantillonage))
    print(DiffTemps) #a supr
    direction = KNNDelais.KNN(Abaque,DiffTemps,K)
    return direction

AbaqueDelais.Abaque(pas,1000,frequence)
Abaque = KNNDelais.RecupereValeursFichier('AbaqueDelais.txt')
SignauxAntennes = Signaux.GenerateurSignaux(EcartTypeBruit, frequence, DureeSignal, FrequenceEchantillonage, (1000, 0, 0))
direction = CalculDirection(Abaque, SignauxAntennes, K, FrequenceEchantillonage)
print(direction)