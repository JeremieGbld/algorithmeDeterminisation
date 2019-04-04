#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 11:14:11 2019

@author: Romain, Jérémie
"""

import pickle

#fonction qui permet de remplir une matrice de hauteur h et de largeur l contenant des listes vides
def initMatrice(l,h):
    res=[]
    for i in range(h):
        ligne=[]
        for j in range(l):
            ligne.append([])
        res.append(ligne)
    return res

class Automate:
    
    "automate de recherche contenant la matrice, état(s) de départ et état(s) d'arrivé"
    #attributs
    nom=""
    etat_depart=[]
    etat_arrive=[]
    matrice_transition=[]
    nombre_etat=0
    alphabet=[]

    #constructeur
    def __init__(self,nom,etat_dep,etat_ariv,matrice,nb_etat,alphabet):
        self.nom=nom
        self.etat_depart=etat_dep
        self.etat_arrive=etat_ariv
        self.matrice_transition=matrice
        self.nombre_etat=nb_etat
        self.alphabet=alphabet       
        
            
    def visu(self):
        for x in self.matrice_transition:
            print(x)
        print("ETAT(S) INITIAL(INITIAUX)")
        for i in self.etat_depart:
            print(i)
        print("ETAT(S) TERMINAL(TERMINAUX)")
        for i in self.etat_arrive:
            print(i)
            
    def deterministe(self):
        if len(self.etat_depart)!=1: #si il y a plusieurs etats initiaux l'automate n'est pas déterministe
            return False
        for j in self.matrice_transition[1:]: #parcours de la matrice
            for i in j[1:]:
                if len(i)>1: #s'il y a plus d'1 état d'arrive pour le meme etat de départ et la meme étiquette de transition, automate non deterministe
                    return False
        return True        #sinon l'automate est deterministe

    def algoDeter(self):
        
        m=initMatrice(len(self.alphabet)+1,2)
        AFD = Automate(self.nom+'_deter', [], self.etat_depart, m, 0, self.alphabet)
        
        i=0
        for j in range(len(AFD.matrice_transition[0])-1): #on remplit la première ligne avec l'alphabet
            AFD.matrice_transition[0][j+1]=AFD.alphabet[i]
            i+=1
            
        listDepart = []
        for i in self.etat_depart:
            listDepart.append(i)
        AFD.etat_depart.append(listDepart)
        
        if AFD.etat_depart != []: # s'il existe un ou plusieurs états de départ
            AFD.matrice_transition[1][0] = self.etat_depart # on définit l'état de départ comme la liste des états de départ de l'AFN
            AFD.nombre_etat +=1 # ajout d'un état dans l'attribut
        lig=1
        while AFD.matrice_transition[-1][1] == []:
            for i in range (1, len(AFD.alphabet)+1): # ième colonne
                AFD.matrice_transition[lig][i] = findListTrans(self.matrice_transition, AFD.matrice_transition[lig][0], i)
                trouve = False
                
                for j in AFD.matrice_transition[1:]:
                    if j[0] == AFD.matrice_transition[lig][i] or AFD.matrice_transition[lig][i] == []:
                        trouve=True
                if not trouve:
                    AFD.matrice_transition.append([])
                    AFD.matrice_transition[-1].append(AFD.matrice_transition[lig][i])
                    for k in range (1, len(AFD.alphabet)+1):
                        AFD.matrice_transition[-1].append([])
                    AFD.nombre_etat +=1
            lig+=1
        
        listArrive = []
        for j in AFD.matrice_transition:
            for i in self.etat_arrive:
                if i in j[0] and j[0] not in listArrive:
                    listArrive.append(j[0])
        AFD.etat_arrive = listArrive

        return AFD
    
    def reconnaissance(self,motif): #voir page 40 du cours
        def reconnu(self,motif,depuis):
            if motif=="":
                if depuis in self.etat_arrive:
                    return True
                else:
                    return False
            else:
                L=findListTrans(self.matrice_transition,depuis,self.matrice_transition[0].index(motif[0]))
                trouve=False
                while L!=[] and trouve==False:
                    vers=L[0]
                    L=L[1:]
                    if reconnu(self,motif[1:],vers):
                        trouve=True
                return trouve
            
        for depuis in self.etat_depart:
            if reconnu(self,motif,depuis):
                return True
            else:
                return False
            
    def reconnaissance_deter(self,motif): #voir page 43 du cours
        ok=True
        courant=self.etat_depart
        k=0
        if motif=="":
            return self.etat_depart in self.etat_arrive
        else:
            while k<=len(motif)-1 and ok:
                if findListTrans(self.matrice_transition,courant,self.matrice_transition[0].index(motif[k]))!=[]:
                    courant=findListTrans(self.matrice_transition,courant,self.matrice_transition[0].index(motif[k]))
                    k+=1
                else:
                    ok=False
            if ok:
                if courant in self.etat_arrive or courant==self.etat_arrive:
                    return True
                else:
                    return False
            else:
                return False
        
                
                    
        
    
def findListTrans(matriceAFN, ini, colonne):
    listeVal = []
    for i in matriceAFN[1:]:
        for j in range (1, len(i)):
            for k in ini:
                if int(k) in i[0] and colonne == j:
                    for l in i[j]:
                        if l not in listeVal:
                            listeVal.append(l)

    return sorted(listeVal)# classement des valeurs

def saisie_nb_etats():
    x=input("SAISIR LE NOMBRE D'ETAT(S) : ")
    while x.isdigit()==False: #si la valeur saisie n'est pas un entier
        print("MERCI DE SAISIR UN ENTIER") #on affiche un message
        x=input() #et on refait saisir la valeur
    return int(x)

def saisie_alphabet():
    x=input("SAISIR LE(S) CHARACTERE(S) DE L'ALPHABET (ENTREE POUR FINIR LA SAISIE)\n")
    alphabet=[]
    while x!="": #tant qu'on saisit un charactère
        if x in alphabet: #on verifie que le charactère n'a pas déja été saisie
            print("CE CHARACTERE EST DEJA PRESENT DANS L'ALPHABET !")
            x=input()
        elif len(x)!=1: #on vérifie qu'un seul charactère est saisie
            print("MERCI DE SAISIR UN SEUL CHARACTERE !")
            x=input()
        else: #si c'est bon
            alphabet.append(x) #on ajoute la valeur à l'alphabet
            x=input() #on passe à la valeur suivante 
    return alphabet

def saisie_matrice(alphabet, nombre_etat):
    matrice_transition=initMatrice(len(alphabet)+1,nombre_etat+1) #initialisation de la matrice
    r=0 #compteur
    for i in matrice_transition: #on remplit la première colonne avec le nombre d'états
        i[0].append(r)
        r+=1
    i=0 
    for j in range(len(matrice_transition[0])-1): #on remplit la première ligne avec l'alphabet
        matrice_transition[0][j+1]=alphabet[i]
        i+=1
    
    print("SAISIE DES ETATS DE TRANSITIONS")
    print("===============================")
    ini=input("ETAT DEPART (ENTREE POUR SORTIR) : ")
    while ini!="":
        while ini.isdigit()==False:
            print("MERCI DE SAISIR UN ENTIER")
            ini=input("ETAT DEPART : ")
        while int(ini) not in range(1,nombre_etat+1): #verification que l'etat saisie est un etat qui existe
            print("MERCI DE SAISIR UN ETAT QUI EXISTE !")
            ini=input("ETAT DEPART : ")              
        transi=input("ETIQUETTE DE TRANSITION : ")
        while transi not in alphabet:
            print("MERCI DE SAISIR UN CHARACTERE DE L'ALPHABET QUI EXISTE !") #verifie que l'etiquette de transition fait bien pati de l'alphabet
            transi=input("ETIQUETTE DE TRANSITION : ")
        arrive=input("ETAT ARRIVE : ")
        while arrive.isdigit()==False:
            print("MERCI DE SAISIR UN ENTIER")
            arrive=input("ETAT ARRIVE : ")
        while int(arrive) not in range(1,nombre_etat+1):
            print("MERCI DE SAISIR UN ETAT QUI EXISTE !")
            arrive=input("ETAT ARRIVE : ")
        j=matrice_transition[0].index(transi) #on récupère le numéro de la colonne
        for i in matrice_transition: #on cherche dans la matrice
            if int(ini) in i[0]: #quand on est sur la bonne ligne = bon état initial
                if arrive in i[j]:#on verifie que la fleche n'a pas déjà été saisie
                    print("CETTE TRANSITION DE L'AUTOMATE A DEJA ETE SAISIE !")
                else:#sinon
                    i[j].append(arrive) #ajoute l'etat d'arrive a la liste avec la bonne etiquette de transition (bonne colonne)
        ini=input("ETAT DEPART (ENTREE POUR SORTIR) : ")   #et on boucle pour toutes les flèches de l'automate  
    return matrice_transition

def saisie_etat_initial(nombre_etat):
    etat_depart=[]
    x=input("SAISIR LE(S) ETAT(S) INITIAL(INITIAUX) (ENTREE POUR FINIR LA SAISIE)\n")
    while x!="": 
        while x.isdigit()==False:
            print("MERCI DE SAISIR UN ENTIER")
            x=input()
        while int(x) not in range(1,nombre_etat+1):
            print("MERCI DE SAISIR UN ETAT QUI EXISTE !")
            x=input()
        etat_depart.append(x)
        x=input()
    return etat_depart

def saisie_etat_final(nombre_etat):
    etat_arrive=[]
    x=input("SAISIR LE(S) ETAT(S) TERMINAL(TERMINAUX) (ENTREE POUR FINIR LA SAISIE)\n")
    while x!="": 
        while x.isdigit()==False:
            print("MERCI DE SAISIR UN ENTIER")
            x=input()
        while int(x) not in range(1,nombre_etat+1):
            print("MERCI DE SAISIR UN ETAT QUI EXISTE !")
            x=input()
        etat_arrive.append(x)
        x=input()
    return etat_arrive



        
def menu():
        B = pickle.load(open('mypicklefile', 'rb'))
        liste_automate=B
        print("BIENVENUE DANS LE MENU DE DETERMINISATION D'AUTOMATE !")
        print("=====================================================")
        choix=" "
        while choix!="0":
            print("1 - SAISIE D'UN AUTOMATE")
            print("2 - VISUALISATION DE L'AUTOMATE")
            print("3 - DETERMINISATION DE L'AUTOMATE")
            print("4 - AUTOMATE DETERMINISTE ?")
            print("5 - RECONNAISSANCE DE MOTIF")
            print("6 - SUPPRIMER UN AUTOMATE DE LA LISTE")
            print("0 - QUITTER")
            choix=input("VOTRE CHOIX ? ")
            print("--------------------------------")
            if choix=="0":
                print("GOOD BYE !")
                pickle.dump(liste_automate, open('mypicklefile', 'wb'))
            elif choix=="1":
                print("SAISIE D'UN AUTOMATE")
                print("====================")
                nom=input("SAISIR LE NOM DE L'AUTOMATE : ")
                nb_etat=saisie_nb_etats()
                alphabet=saisie_alphabet()
                matrice=saisie_matrice(alphabet,nb_etat)
                etat_ini=saisie_etat_initial(nb_etat)
                etat_fin=saisie_etat_final(nb_etat)
                liste_automate.append(Automate(nom,etat_ini,etat_fin,matrice,nb_etat,alphabet))
                print("--------------------------------")
            elif choix=="2":
                print("LISTE DES AUTOMATES : ")
                for i in liste_automate:
                    print("-",i.nom)
                nom_auto=input("SAISIR LE NOM DE L'AUTOMATE : ")
                auto=""
                for i in liste_automate:
                    if i.nom==nom_auto:
                        auto=i
                if auto!="":
                    auto.visu()
                else:
                    print("CET AUTOMATE N'EXISTE PAS !")
                print("--------------------------------")
            elif choix=="3":
                print("LISTE DES AUTOMATES : ")
                for i in liste_automate:
                    print("-",i.nom)
                nom_auto=input("SAISIR LE NOM DE L'AUTOMATE : ")
                deter = False
                for j in liste_automate:
                    if j.nom==nom_auto:
                        newAuto=j.algoDeter()
                        liste_automate.append(newAuto)
                        deter = True
                if not deter:
                    print("CET AUTOMATE N'EXISTE PAS !")
                print("--------------------------------")
            elif choix=="4":
                print("LISTE DES AUTOMATES : ")
                for i in liste_automate:
                    print("- ",i.nom)
                nom_auto=input("SAISIR LE NOM DE L'AUTOMATE : ")
                auto=""
                for i in liste_automate:
                    if i.nom==nom_auto:
                        auto=i
                if auto!="":
                    if auto.deterministe():
                        print("CET AUTOMATE EST DETERMINISTE")
                        print("--------------------------------")
                    else:
                        print("CET AUTOMATE N'EST PAS DETERMINISTE")
                        print("--------------------------------")
                else:
                    print("CET AUTOMATE N'EXISTE PAS !")
                    print("--------------------------------")
            elif choix=="5":
                print("LISTE DES AUTOMATES : ")
                for i in liste_automate:
                    print("- ",i.nom)
                nom_auto=input("SAISIR LE NOM DE L'AUTOMATE : ")
                auto=""
                for i in liste_automate:
                    if i.nom==nom_auto:
                        auto=i
                if auto!="":
                    motif=input("SAISIR LE MOTIF A VERIFIER : ")
                    if auto.deterministe()==False:
                        if auto.reconnaissance(motif):
                            print("CE MOTIF EST RECONNU PAR L'AUTOMATE !")
                            print("--------------------------------")
                        else:
                            print("CE MOTIF N'EST PAS RECONNU PAR L'AUTOMATE !")
                            print("--------------------------------")
                    else:
                        if auto.reconnaissance_deter(motif):
                            print("CE MOTIF EST RECONNU PAR L'AUTOMATE !")
                            print("--------------------------------")
                        else:
                            print("CE MOTIF N'EST PAS RECONNU PAR L'AUTOMATE !")
                            print("--------------------------------")
                else:
                    print("CET AUTOMATE N'EXISTE PAS !")
                    print("--------------------------------")
            elif choix=="6":
                print("LISTE DES AUTOMATES : ")
                for i in liste_automate:
                    print("- ",i.nom)
                nom_auto=input("SAISIR LE NOM DE L'AUTOMATE : ")
                auto=""
                for i in liste_automate:
                    if i.nom==nom_auto:
                        auto=i
                if auto!="":
                    liste_automate.remove(auto)
                    print("AUTOMATE SUPPRIME !")
                else:
                    print("CET AUTOMATE N'EXISTE PAS !")
                    print("--------------------------------")
            else:
                print("CE CHOIX N'EST PAS VALIDE !")
                print("--------------------------------")
                    
#pickle.dump(Automate(), open('mypicklefile', 'wb'))         
                
menu()
