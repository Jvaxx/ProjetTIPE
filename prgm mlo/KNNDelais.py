#executer en tant que script ( ctrl + shit + E sur pyzo)
import os
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
import math
import AbaqueDelais

frequence = 300 

def tri_fusion_index0(Liste: list):
    if  len(Liste) <= 1: 
        return Liste
    pivot = len(Liste)//2
    ListeGauche = Liste[:pivot]
    ListeDroite = Liste[pivot:]
    GaucheTrie = tri_fusion_index0(ListeGauche)
    DroiteTrie = tri_fusion_index0(ListeDroite)
    Listefusionne = fusion_index0(GaucheTrie,DroiteTrie)
    return Listefusionne

def fusion_index0(Liste1: list,Liste2: list):
    indice_Liste1 = 0
    indice_Liste2 = 0    
    taille_Liste1 = len(Liste1)
    taille_Liste2 = len(Liste2)
    Liste_fusionne = []
    while indice_Liste1<taille_Liste1 and indice_Liste2<taille_Liste2:
        if Liste1[indice_Liste1][0] < Liste2[indice_Liste2][0]:
            Liste_fusionne.append(Liste1[indice_Liste1])
            indice_Liste1 += 1
        else:
            Liste_fusionne.append(Liste2[indice_Liste2])
            indice_Liste2 += 1
    while indice_Liste1<taille_Liste1:
        Liste_fusionne.append(Liste1[indice_Liste1])
        indice_Liste1+=1
    while indice_Liste2<taille_Liste2:
        Liste_fusionne.append(Liste2[indice_Liste2])
        indice_Liste2+=1
    return Liste_fusionne
    
def distance(vecteur1, vecteur2):
    d = 0
    for i in range(len(vecteur1)):
        d += (vecteur1[i]-vecteur2[i])**2
    d = math.sqrt(d)
    return d
    
def ChoixKforKNN(ListRef: list, ListTest: list):
    a=0
    e = 0
    Erreurs=[]
    for Test in ListTest:
        a=a+1
        if e != int((a/len(ListTest))*100):
            e = int((a/len(ListTest))*100)
            print(str(e) + "%")
        
        DistancesValeurs = []
        for Ref in ListRef:
            dist = distance(Ref[0],Test[0])
            DistancesValeurs.append((dist,Ref[1]))
        DistancesValeursTriees = tri_fusion_index0(DistancesValeurs)
        ErreursPourTest = []
        for k in range(1,len(ListRef)):
            estimevaleur1=0
            estimevaleur2=0
            for i in range(0,k):
                estimevaleur1+=DistancesValeursTriees[i][1][0]
                estimevaleur2+=DistancesValeursTriees[i][1][1]
            estimevaleur1 = estimevaleur1/k
            estimevaleur2 = estimevaleur2/k
            erreur1 = abs(estimevaleur1 - Test[1][0])
            erreur2 = abs(estimevaleur2 - Test[1][1])
            ErreursPourTest.append((erreur1,erreur2))
        Erreurs.append(ErreursPourTest)
    ErreursMoyennes = []    
    for k in range(1,len(ListRef)):
        s1 = 0
        s2 = 0
        for i in range(len(Erreurs)):
            s1 += Erreurs[i][k-1][0]
            s2 += Erreurs[i][k-1][1]
        s1 = s1 / len(Erreurs)
        s2 = s2 / len(Erreurs)
        
        ErreursMoyennes.append((s1+s2)/2)
    K = ErreursMoyennes.index(min(ErreursMoyennes)) + 1
    return K, ErreursMoyennes[K-1]   
    
def KNN(ListRef: list, Inconnu: list, k: int): #inconnu: liste sous la forme dephasage1, dephasage2, dephasage3, dephasage4, dephasage5
    DistancesValeurs = []
    for Ref in ListRef:
        dist = distance(Ref[0],Inconnu)
        DistancesValeurs.append((dist,Ref[1]))
    DistancesValeursTriees = tri_fusion_index0(DistancesValeurs)
    estimevaleur1=0
    estimevaleur2=0
    for i in range(0,k):
        estimevaleur1 += DistancesValeursTriees[i][1][0]
        estimevaleur2+=DistancesValeursTriees[i][1][1]
    estimevaleur1 = estimevaleur1/k
    estimevaleur2 = estimevaleur2/k
    return((estimevaleur1,estimevaleur2))
    

def RecupereValeursFichier(Nom: str):
    ValeursFichier = [] #liste de liste sous la forme dephasage1, dephasage2, dephasage3, dephasage4, dephasage5,angle1,angle2
    fichier = open(Nom, 'r')
    for ligne in fichier:
        ValeursLigne = tuple(map(float, ligne.split(',')))
        L= [(ValeursLigne[0],ValeursLigne[1],ValeursLigne[2],ValeursLigne[3],ValeursLigne[4]),(ValeursLigne[5],ValeursLigne[6])]
        ValeursFichier.append(L)
    fichier.close()
    
    return ValeursFichier
    
    

def ChoixAbaqueEtKpourKKN():
    ResulatChoixK = []
    for i in range(20,1,-1):
        
        AbaqueDelais.DelaisAleatoire(100,10000,frequence)
        AbaqueDelais.Abaque(i,1000,frequence)
        
        Abaque,ValeursTest = RecupereValeursFichier('AbaqueDelais.txt') ,RecupereValeursFichier('ValeursTestDelais.txt')
        
        K,ErreursMoyenneK = ChoixKforKNN(Abaque,ValeursTest)
        
        ResulatChoixK.append((i,K,ErreursMoyenneK))
        
        print(ResulatChoixK)
    return ResulatChoixK

print(ChoixAbaqueEtKpourKKN())
