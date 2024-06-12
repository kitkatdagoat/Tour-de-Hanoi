# from copy import copy
import pickle
import os
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import copy
import time
scores={}
statistics={}
nom_fichier_1='mon_fichier_gagne.pkl'
if os.path.exists(nom_fichier_1):
    if os.path.getsize(nom_fichier_1) > 0:
        with open('mon_fichier_gagne.pkl', 'rb') as fichier_1:
            statistics = pickle.load(fichier_1)
else :
    with open(nom_fichier_1, 'wb') as fichier_1:
        pickle.dump(statistics, fichier_1)
    with open(nom_fichier_1, 'rb') as fichier_1:
        statistics= pickle.load(fichier_1)
print(statistics)

nom_fichier='mon_fichier.pkl'
if os.path.exists(nom_fichier):
    if os.path.getsize(nom_fichier) > 0:
        with open('mon_fichier.pkl', 'rb') as fichier:
            scores = pickle.load(fichier)
else :
    with open(nom_fichier, 'wb') as fichier:
        pickle.dump(scores, fichier)
    with open(nom_fichier, 'rb') as fichier:
        scores= pickle.load(fichier)
print(scores)

##PARTIE A
def init(n):
    return [[a for a in range (n,0,-1)], [], []]
def nbDisques(plateau,numtour):
    return plateau[numtour]
def disqueSup(plateau,numtour):
    if numtour>len(plateau)-1 or plateau[numtour]==[]:
        return -1
    else:
        return plateau[numtour][-1]
def posDisque(plateau,numdisque):
    for i in range (len(plateau)):
        if numdisque in plateau[i]:
            return i
def verifDepl(plateau,nt1,nt2):
    if plateau[nt1]!=[]:
        if plateau[nt2]==[] or disqueSup(plateau,nt1)<disqueSup(plateau,nt2):
            return True
    return False
def verifVictoire(plateau,n):
    if (plateau[0]==[] and plateau[1]==[]):
        if len(plateau[2])==n:
            for i in range(n-1,0,-1):
                if plateau[2][i]<plateau[2][i-1]:
                    return True
    return False

#----------------------------------------------------------------------#

##PARTIE B
from turtle import *
colors=['red','orange','DarkGoldenrod1','DarkGreen','chartreuse','blue','green','cyan','CadetBlue1','DeepPink3','DeepPink','blue1','cyan','chocolate1','chocolate2','cornsilk','DarkOrchid','DeepPink']
texte=['Tour 1','Tour 2', 'Tour 3']
speed(0)
def rectangle(a,b,x,y):
    up()
    goto(a,b)
    down()
    goto(a,b+y)
    goto(a+x,b+y)
    goto(a+x,b)
    goto(a,b)

def dessinePlateau(n):
    longueur=40+(n-1)*30
    rectangle(-300,-200,80+longueur*3,20)
    for i in range(0,3):
        rectangle(-300-3+20+longueur/2+(20+longueur)*i,-180,6,(n+1)*20)
        up()
        goto(-300-3+20+longueur/2+(20+longueur)*i-10,-197.5)
        write(texte[i])
        down()
    
def dessineDisque(nd, plateau, n):
    longueur=40+(n-1)*30
    tour=posDisque(plateau,nd)
    coulor=colors[nd-1]
    fillcolor(coulor)
    begin_fill()
    for i in range(len(plateau[tour])):
        if plateau[tour][i]==nd:
            rectangle(-300+20+longueur/2+(20+longueur)*tour-(40+(nd-1)*30)/2,-180+20*i,40+(nd-1)*30,20)
    end_fill()

def effaceDisque(nd, plateau, n):
    longueur=40+(n-1)*30
    color('white')
    tour=posDisque(plateau,nd)
    fillcolor('white')
    begin_fill()
    for i in range(len(plateau[tour])):
        if plateau[tour][i]==nd:
            rectangle(-300+20+longueur/2+(20+longueur)*tour-(40+(nd-1)*30)/2,-180+20*i,40+(nd-1)*30,20)
    end_fill()
    color('black')
    for i in range(len(plateau[tour])):
        if plateau[tour][i]==nd:
            rectangle(-300+20+longueur/2+(20+longueur)*tour-(40+(nd-1)*30)/2,-180+20*(i),40+(nd-1)*30,0)
    for i in range(len(plateau[tour])):
        if plateau[tour][i]==nd:
            rectangle(-300-3+20+longueur/2+(20+longueur)*tour,-180+20*i,6,(n+1-i)*20)

def dessineConfig(plateau,n):
    for i in plateau:
        for nd in i:
            dessineDisque(nd, plateau,n)

def effaceTout(plateau,n):
    for x in range (1,n+1):
        effaceDisque(x,plateau,n)

##PARTIE C
##1
def lireCoords(plateau):
    q1=int(numinput("Déplacement","Choisir la tour de départ (Vous pouvez taper -1 pour undo): "))
    if q1==-1:
        return -1,0
    while disqueSup(plateau,q1)==-1 or (verifDepl(plateau,q1,0)==False and verifDepl(plateau,q1,1)==False and verifDepl(plateau,q1,2)==False):
        if disqueSup(plateau,q1)==-1: q1=int(numinput("Déplacement",f"Invalid, tour vide\nChoisir la tour de départ: "))
        elif (verifDepl(plateau,q1,0)==False and verifDepl(plateau,q1,1)==False and verifDepl(plateau,q1,2)==False): q1=int(numinput("Déplacement",f"Invalid, disque plus grande\nChoisir la tour de départ: "))
    q2=int(numinput("Déplacement","Choisir la tour d'arrivée: "))
    while (q2>2 or q2<0) or verifDepl(plateau,q1,q2)==False:
        q2=int(numinput(f"Déplacement","Invalid, disque plus petite\nChoisir la tour de d'arrivée: "))
    return q1, q2

##2
def jouerUnCoup(plateau,n):
    x,y=lireCoords(plateau)
    if x==-1:
        return -1
    effaceDisque(plateau[x][-1],plateau,n)
    plateau[y].append(plateau[x][-1])
    plateau[x].pop(-1)
    dessineDisque(plateau[y][-1],plateau,n)

#3
def boucleJeu(plateau,n):
    mincoup=(2**n)-1
    rep=0
    ##turns=0
    turn=int(numinput("Difficulté",f"Coups autorisés (minimum en {mincoup} en êtes-vous capable):"))
    while turn<mincoup:
        turn=int(numinput("Warning",f"Vous ne pouvez pas le resoudre en {turn} coups, reesayer, svp:"))
    time_debut=time.time()
    coups={0: copy.deepcopy(plateau)}
    while rep<turn and not(verifVictoire(plateau,n)):
        ##turns+=1
        print(f"Coup numéro {rep}")
        undo=jouerUnCoup(plateau,n)
        if undo==-1:
            rep-=1
            if rep<0:
                print (f'Vous ne pouvez plus annuler')
                #write(f"Vous ne pouvez plus annuler",font=("Arial",15,"bold"))
                undo=jouerUnCoup(plateau,n)
            else:
                annulerDernierCoup(coups)
                plateau=copy.deepcopy(coups[len(coups)-1])
        else:
            rep+=1
            coups[rep]=copy.deepcopy(plateau)
            plateau=copy.deepcopy(coups[rep])
    time_fin=time.time()
    return rep,verifVictoire(plateau,n),round(time_fin-time_debut,2)
##pour l'amelioration (partie C)
def on_click(x, y):
    print("Clicked at", x, y)

#PARTIE D
#1
def dernierCoup(coups):
    for i in range(3):
        if coups[len(coups)-2][i]!=coups[len(coups)-1][i]:
            for j in range(i+1,3):
                if coups[len(coups)-2][j]!=coups[len(coups)-1][j]:
                    return (i,j) if len(coups[len(coups)-2][j])<len(coups[len(coups)-1][j]) else (j,i)
#2
def annulerDernierCoup(coups):
    x,y=dernierCoup(coups)
    effaceDisque(coups[len(coups)-1][y][-1],coups[len(coups)-1],len(coups[0][0]))
    dessineDisque(coups[len(coups)-2][x][-1],coups[len(coups)-2],len(coups[0][0]))
    coups.pop(len(coups)-1)
#PARTIE E
#1
def sauvScore(scores,nombre,nom,disque,coups,temps):
    scores[nombre] = []
    scores[nombre]=[nom,disque,coups,temps]
    return scores
####Pour creer un tableau de score et le style des mots
style=('Arial',10)
style_title=('Arial',10,'bold')
def tableScores(a,b,x,y):
    up()
    goto(a,b)
    down()
    goto(a+x,b+y)

#4
def afficheScores(scores):
    reset()
    speed(0)
    a=0
    tableScores(-250,220,550,0)
    up()
    color('blue')
    goto(-200,200)
    write('Classement',font=style_title)
    goto(-100,200)
    write('Nom', font=style_title)
    goto(0,200)
    write('Disque',font=style_title)
    goto(100,200)
    write('Coups', font=style_title)
    goto(200,200)
    write('Temps', font=style_title)
    color('black')
    sorted_items = sorted(scores.items(), key=lambda item: (item[1][1], -item[1][2]), reverse=True)
    sorted_dict = dict(sorted_items)
    for i in sorted_dict:
        tableScores(-250,195-25*a,550,0)
        up()
        goto(-200,175-25*a)
        write(a+1)
        goto(-100,175-25*a)
        write(scores[i][0],align='left')
        goto(20,175-25*a)
        write(scores[i][1])
        goto(120,175-25*a)
        write(scores[i][2],align='center')
        goto(220,175-25*a)
        write(scores[i][3],align='center')
        a+=1
    tableScores(-250,195-25*(a),550,0)
    up()
    goto(15,195-25*(a+1))
    color('chartreuse')
    write('Tapez "O" pour continuer', font=style_title,align='center')

#5
def afficheChronos(scores):
    reset()
    speed(0)
    a=0
    tableScores(-250,220,350,0)
    up()
    color('blue')
    goto(-200,200)
    write('Classement',font=style)
    goto(-100,200)
    write('Nom', font=style)
    goto(0,200)
    write('Temps', font=style)
    color('black')
    sorted_items = sorted(scores.items(), key=lambda item: (item[1][3]))
    for i in dict(sorted_items):
        tableScores(-250,195-25*i,350,0)
        up()
        goto(-200,175-25*a)
        write(a+1)
        goto(-100,175-25*a)
        write(scores[i][0],align='left')
        goto(40,175-25*a)
        write(scores[i][3],align="right")
        a+=1

def reflexion(scores,joueur): ##(pour reflexionMoy)
    temps=0
    coups=0
    for partie in scores.values():
        if partie[0]==joueur:
            temps+=partie[3]
            coups+=partie[2]
    return joueur,round(temps/coups,2)
#6
def reflexionMoy(scores):
    temps={}
    for i in range(len(scores)):
        x,y=reflexion(scores,scores[i][0])
        if x not in temps:
            temps[x]=[]
            temps[x]=[y]
    return temps

#7
def afficherTemps(scores):
    reset()
    speed(0)
    a=0
    tableScores(-250,220,350,0)
    up()
    color('blue')
    goto(-200,200)
    write('Classement',font=style_title)
    goto(-100,200)
    write('Nom', font=style_title)
    goto(0,200)
    write('Temps', font=style_title)
    color('black')
    sorted_items = sorted(reflexionMoy(scores).items(), key=lambda item: (item[1][0]))
    for i in dict(sorted_items):
        tableScores(-250,195-25*a,350,0)
        up()
        goto(-200,175-25*a+1)
        write(a+1)
        goto(-100,175-25*a+1)
        write(i,align='left')
        goto(40,175-25*a+1)
        write(sorted_items[a][1],align="right")
        a+=1
    tableScores(-250,195-25*(a),350,0)
    up()
    goto(-50,195-25*(a+1))
    color('chartreuse')
    write('Tapez "O" pour continuer', font=style_title,align='center')

#PARTIE F
#1
def solution(n, source, auxiliary, destination, liste): 
    if n == 1: 
        liste.append([source, destination])
    else:
        solution(n-1, source, destination, auxiliary,liste) 
        liste.append([source, destination])
        solution(n-1, auxiliary, source, destination,liste)
    return(liste)

#2
def auto(liste,plateau,n):
    for i in range(len(liste)):
        x,y=liste[i]
        effaceDisque(plateau[x][-1],plateau,n)
        plateau[y].append(plateau[x][-1])
        plateau[x].pop(-1)
        dessineDisque(plateau[y][-1],plateau,n)

#TRACER LE GRAPHIQUE SUR LE PARTIE GAGNÉ (OPTIONS DE PARTIE E)
def creer_liste(scores,i):
    return [scores[a][i] for a in scores]

def graphique(scores):
    categories = creer_liste(scores,0) #scores
    values1 = creer_liste(scores,1)
    # values2 = creer_liste(scores,2)
    # values3 = creer_liste(scores,3)
    bar_width = 0.2
    index = np.arange(len(categories))
    plt.bar(index - 0* bar_width, values1, width=bar_width, label='Pourcentage de partie gagné')
    # plt.bar(index - 0.5 * bar_width, values2, width=bar_width, label="Pourcentage d'echec")
    # plt.bar(index + 0.5 * bar_width, values3, width=bar_width, label='Temps')
    plt.ylim(top=100)
    plt.xlabel('Noms')
    plt.ylabel('Pourcentage (%)')
    plt.title('Les Scores')
    plt.xticks(index, categories)
    plt.legend()
    plt.show()

#pour the le graphique de pourcentage
def liste_win(statistics,nom,y):
    if nom not in statistics:
        statistics[nom] = []
        statistics[nom]=[nom,0,0]
    if y==True:
        statistics[nom][1] += 1
    else:
        statistics[nom][2] += 1
    return statistics
def partie_win(statistics,nom): ##(pour reflexionMoy)
    win=0
    lose=0
    for partie in statistics.values():
        if partie[0]==nom:
            win+=partie[1]
            lose+=partie[2]
    return nom,round((win/(win+lose))*100,2)

def win(statistics):
    dicti={}
    for i in statistics:
        x,y=partie_win(statistics,statistics[i][0])
        if x not in dicti:
            dicti[x]=[]
            dicti[x]=[x,y]
    return dicti


def main(): ##FONCTION PRINCIPAL
    window=Screen()
    rep=0
    liste=[]
    i=len(scores)
    while rep!="N":
        reset()
        speed(0)
        n=int(numinput(f"Bienvenue dans les Tours de Hanoi","Combien de disques?"))
        dessinePlateau(n)
        plateau=init(n)
        dessineConfig(plateau,n)
        # bouton(n,liste,plateau)
        x,y,z=boucleJeu(plateau,n)
        if not(y): 
            nom=textinput("Nom",f'Defeat\nVotre nom? ')
            liste_win(statistics,nom,y)
            rep=textinput("Nouvelle partie",f"Defeat\nTapez 'o' pour voir les scores\nTapez 'p' pour voir le temps moyen\nTaper 's' pour la solution\nTaper 'O' ou 'N' pour rejouer ou quitter")
        else:
            nom=textinput("Nom",f'Victoire après {x} coups\nVotre nom? ')
            liste_win(statistics,nom,y)
            print(sauvScore(scores,i,nom,n,x,z))
            i+=1
            rep=textinput("Menu",f"Tapez 'o' pour voir les scores\nTapez 'p' pour voir le temps moyen\nTaper 'O' ou 'N' pour rejouer ou quitter ")
        while rep!="O" and rep!="N":
            if rep=="o":
                afficheScores(scores)
                rep=textinput("Menu",f"Tapez 'o' pour voir les scores\nTapez 'p' pour voir le temps moyen\nTaper 's' pour la solution\nTaper 'O' ou 'N' pour rejouer ou quitter")
            elif rep=="p":
                afficherTemps(scores)
                rep=textinput("Menu",f"Tapez 'o' pour voir les scores\nTapez 'p' pour voir le temps moyen\nTaper 's' pour la solution\nTaper 'O' ou 'N' pour rejouer ou quitter")
            elif rep=='s':
                reset()
                speed(0)
                plateau=init(n)
                dessinePlateau(n)
                dessineConfig(plateau,n)
                auto(solution(n,0,1,2,liste),plateau,n)
                rep=textinput("Menu",f"Tapez 'o' pour voir les scores\nTapez 'p' pour voir le temps moyen\nTaper 's' pour la solution\nTaper 'O' ou 'N' pour rejouer ou quitter")
    graphique(win(statistics))
    with open('mon_fichier.pkl', 'wb') as fichier:
        pickle.dump(scores, fichier)
    with open('mon_fichier_gagne.pkl', 'wb') as fichier_1:
        pickle.dump(statistics, fichier_1)
    window.exitonclick()
main()

    
    
        
    

    
