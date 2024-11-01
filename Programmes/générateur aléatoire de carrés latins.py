from random import *

def permutation(L,a,b): # fonction permettant de permuter le (a+1)ème et le (b+1)ème élément d'une liste L
    l=len(L)
    if (a in [i for i in range(l)]) and (b in [i for i in range(l)]):
        z = L[a]
        L[a] = L[b]
        L[b] = z
    else : print("Erreur")
    return L

def random2(l): # fonction générant deux entiers aléatoires entre 0 et l-1 inclus
    R=[]
    for i in range(2):
        R.append(randint(0,l-1))
    return R

def carre_latin_trivial(L): # fonction générant le carré latin trival de dimension n sous forme d'une liste de listes à partir de la liste de l paramètres L
    l=len(L)
    C=[]
    for n in range(l):
        C.append([L[(i+n)%l] for i in range(l)])
    return C

def cl_aleatoire(L): # fonction générant un carré latin aléatoire à partir de la liste de l paramètres L
    l=len(L)
    for j in range(l-1): # on effectue une permutation aléatoire de L sous la forme de l-1 transpositions (permutation des lignes)
        R=random2(l)
        L=permutation(L,R[0],R[1])
    c=carre_latin_trivial(L)
    for k in range(l-1): # on effectue une permutation aléatoire de c sous la forme de l-1 transpositions (permutation des colonnes)
        R=random2(l)
        c=permutation(c,R[0],R[1])
    return c

def latin_ou_non(C):
    n=len(C)
    for i in range(n):#parcours vertical
        acc=[]
        for j in range(n):
            if C[i][j] in acc:
                return False
            acc.append(C[i][j])
    for i in range(n): #parcours horizontal
        acc=[]
        for j in range(n):
            if C[j][i] in acc:
                return False
            acc.append(C[j][i])
    return True #complexité : 2*n^2

def greco_latin_ou_non(C,D):
    n=len(C)
    acc=[]#accumulateur des couples
    if not latin_ou_non(C):
        return False
    if not latin_ou_non(D):
        return False
    for i in range(n):
        for j in range(n):
            if [C[i][j],D[i][j]] in acc:
                return False
            acc.append([C[i][j],D[i][j]])
    return True

def proba(n):
    c=0
    for i in range(n):
        a=cl_aleatoire([0,1,2,3,4])
        if greco_latin_ou_non(a,carre_latin_trivial([0,1,2,3,4])) == True :
            c+=1
    return c