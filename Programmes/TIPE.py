from random import *
from matplotlib.pyplot import *
from numpy import *
from os import *

def fact_premiere(n):#Renvoie la liste des facteurs premiers de n pour n<200 avec leur multiplicité
    PRE=[2,3,5,7,9,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199]
    P=[]
    for i in PRE:
        while n%i==0:
            P.append(i)
            n=n//i
    m=len(P)
    L=[[P[0],1]]
    for j in range(1,m):
        if P[j]!=P[j-1]:
            L.append([P[j],0])
    c=0
    for k in range(1,m):
        if P[k]!=P[k-1]:
            c+=1
        L[c][1]+=1
    return L

def nb_carres_orth(n):# min(pi**ei - 1)
    P=fact_premiere(n)
    m=P[0][0]**P[0][1] - 1
    l=len(P)
    for i in range(l):
        if P[i][0]**P[i][1] - 1 < m:
            m=P[i][0]**P[i][1] - 1
    return m

def crea_tous_carres_orth(n):
    h=nb_carres_orth(n)
    LAT=[]
    for j in range(1,h+1):
        #Creation des h carres
        #Parcours vertical puis horizontal avec à chaque fois application des actions sur les lignes ou les colonnes
        L=[]
        for x in range(n):
            L.append([])
            for y in range(n):
                L[x].append((j*x)%n)
        for r in range(n):
            for s in range(n):
                L[s][r]=((L[s][r]+r)%n)
        LAT.append(L)
    return LAT

def matM1(m):#crée la matrice M1
    M=[]
    for i in range(m):
        M.append([])
        for j in range(m*m):
            if j>=m*i and j<m*(i+1):
                M[i].append(1)
            else:
                M[i].append(0)
    return M

def matM2(m):#crée la matrice M2
    M=[]
    for i in range(m):
        M.append([])
        for j in range(m*m):
            if j%m == i:
                M[i].append(1)
            else:
                M[i].append(0)
    return M


def vectVmu(mu,m,L):
    V=[]
    for j in range(m):
        for k in range(m):
            if L[j][k]==mu:
                V.append(1)
            else:
                V.append(0)
    return V


def matMi(i,m,LAT):
    L=LAT[i-3]
    Mi=[]
    for mu in range(m):
        Mi.append(vectVmu(mu,m,L))
    return Mi


def matH(m,t):#crée H
    H=[]#listes internes : lignes
    M1=matM1(m)
    M2=matM2(m)
    H=M1+M2
    LAT=crea_tous_carres_orth(m)
    for i in range(3,2*t+1):
        M=matMi(i,m,LAT)
        H=H+M
    for j in range(2*t*m):
        for k in range(2*t*m):
            if k==j:
                H[j].append(1)
            else:
                H[j].append(0)
    return H


def xor(L): #Fonction prenant en entrée une liste de bits, renvoyant le xor de la liste
    if len(L)<2:
        return "Liste trop petite"
    else:
        B=abs(L[0]-L[1])
        for i in range(2,len(L)):
            B=abs(B-L[i])
        return B

def bits_de_controle(d,m,t):
    if len(d)!=m**2:
        return "Mauvaise taille de liste"
    H=matH(m,t)
    for i in range(2*t*m):
        L=[]
        for j in range(m**2):
            if H[i][j]==1: L.append(d[j])
        d.append(xor(L))
    return d

def vote(L): #compte les suffrages d'une liste de bits
    a0=0
    a1=0
    for i in range(len(L)):
        if L[i]==0: a0+=1
        elif L[i]==1: a1+=1
        else: return ("Vote interdit",L[i])
    if a0>=a1: return 0
    else: return 1


def decode(d,m,t):
    L=[] #liste correspondant au code corrigé
    H=[d]+matH(m,t)
    for i in range(m**2):
        S=[d[i]] #liste des "suffrages"
        for j in range(1,2*m*t+1):
            X=[] #liste des éléments de la ligne
            if H[j][i]==1:
                for k in range(m**2+2*m*t):
                    if k!=i and H[j][k]==1:
                        X.append(d[k])
                S.append(xor(X))
        L.append(vote(S))
    return L

def transmission(d,m,t,p): #p est le nombre d'erreurs
    d=bits_de_controle(d,m,t)
    P=[]
    while len(P)<p:
        r=randint(0,m**2+2*m*t-1)
        if r not in P: P.append(r)
    for j in P:
        if d[j]==0:
            d[j]=1
        else:
            d[j]=0
    return d

def listes_egales(u,v): #retourne si deux listes sont égales
    if len(u)!=len(v): return False
    else :
        for i in range(len(u)):
            if u[i]!=v[i] : return False
    return True

def liste_aleatoire(m): #crée une liste de bits aléatoire de longueur m
    L=[]
    for i in range(m):
        L.append(randint(0,1))
    return L

def test(m,t,p,n): #fais n essais à p erreurs
    a=0 #compteur
    for i in range(n):
        L=liste_aleatoire(m**2)
        Lc=L[:]
        T=transmission(L,m,t,p)
        D=decode(T,m,t)
        if listes_egales(Lc,D):
            a+=1
    return a

def graphe_test(m,n,e): #calcule la précision pour tous les t possibles jusqu'à e erreurs
    X=[i for i in range(1,e+1)]
    Y=[]
    for t in range(1,proportion(m)[0]+1):
        Z=[]
        for i in range(1,e+1):
            a=test(m,t,i,n)
            Z.append(a)
            print(i,a)
        Y.append(Z)
    figure()
    for k in range(proportion(m)[0]):
        plot(X,Y[k])
    show()

def proportion(m): #nombre d'erreurs maximal par liste de données
    t=int(nb_carres_orth(m)/2)+1
    c=m**2+2*m*t
    return(t,c)

def graphe_proportion(m):
    X=[i for i in range(2,m+1)]
    Y=[]
    for i in range(2,m+1):
        Y.append(proportion(i)[0]/proportion(i)[1])
    figure()
    plot(X,Y)
    show()

def graphe_proportion_stockage(m):
    X=[i for i in range(2,m+1)]
    Y=[]
    for i in range(2,m+1):
        Y.append(proportion(i)[1]/i**2)
    figure()
    plot(X,Y)
    show()

def conv_binaire(n):#Convertit un entier naturel de [0,255] en binaire avec la division euclidienne
    B=[]
    N=n
    for i in range(8):
        r = N%2
        N = N//2
        B.append(r)
    list.reverse(B)
    return(B)

def convertisseur_jpeg_vers_binaire(L): #Convertit des listes d'images en format jpeg en liste de listes binaires (un binaire entre 0 et 255 est codé par une liste de 0 et de 1 de longueur 8)
    hau=len(L)
    lar=len(L[0])
    M=[]
    for i in range(hau):
        M.append([])
        for j in range(lar):
            M[i].append([0,0,0])
            for k in range(3):
                M[i][j][k]=conv_binaire(L[i][j][k])
    return(M)

def convertisseur_png_vers_binaire(L): #Convertit des listes d'images en format jpeg en liste de listes binaires (un binaire entre 0 et 255 est codé par une liste de 0 et de 1 de longueur 8)
    hau=len(L)
    lar=len(L[0])
    M=[]
    for i in range(hau):
        M.append([])
        for j in range(lar):
            M[i].append([0,0,0])
            for k in range(3):
                M[i][j][k]=conv_binaire(int(L[i][j][k]*255))
    return(M)

def liste4_a_1(L):
    N=[]
    for i in range(len(L)):
        for j in range(len(L[i])):
            for k in range(len(L[i][j])):
                for l in range(len(L[i][j][k])):
                    N.append(L[i][j][k][l])
    return N

def png_entier(L):
    N=[]
    for i in range(len(L)):
        N.append(int(L[i]*255))
    return N

def conv_base_10(N):#convertit un binaire sous forme de liste en base 10 si il est inférieur à 255, len(N)=8
    l=0
    for i in range(8):
        l= 2*l + N[i]
    return(l)

def convertisseur_binaire_vers_jpeg(L):
    hau = len(L)
    lar = len(L[0])
    M=[]
    for i in range(hau):
        M.append([])
        for j in range(lar):
            M[i].append([0,0,0])
            for k in range(3):
                M[i][j][k] = conv_base_10(L[i][j][k])
    return(M)

def partition(L,dis):#partitionne une liste en bouts de longueur m^2. Si il y a des éléments en en trop, on rajoute des 0
    n=len(L)
    c=0
    k=0
    M=[[]]
    for i in range(n):
        c+=1
        M[k].append(L[i])
        if c==dis:
            M.append([])
            k+=1
            c=0
    r=n%dis
    for i in range(dis-r):
        M[k].append(0)
    return(M)

def liste1_a_4(L,n,m):
    N1=[]
    c=0
    for i in range(n):
        if i%10==0 : print('liste1_a_4',100*i/n)
        N2=[]
        for j in range(m):
            N3=[]
            for k in range(3):
                N4=[]
                for l in range(8):
                    N4.append(L[c])
                    c+=1
                N3.append(N4)
            N2.append(N3)
        N1.append(N2)
    return N1

def liste256_a_binaire(L):
    N1=[]
    for i in range(len(L)):
        N1.append(conv_binaire(L[i]))
    N2=[]
    for i in range(len(N1)):
        N2=N2+N1[i]
    return N2

def ajout_bits_de_controle(L,m,t): #Prend une liste de bits et y ajoute les bits de contrôle
    P=partition(L,m**2)
    N=[]
    p=len(P)
    print(p)
    for i in range(p):
        if 10000//m**2==0 : print('ajout_bits_de_controle',100*i/p)
        elif i%(10000//m**2)==0: print('ajout_bits_de_controle',100*i/p)
        B=bits_de_controle(P[i],m,t)
        for j in range(len(B)):
            N.append(B[j])
    return N

def ajout_bits_de_controle2(L,m,t): #Prend une liste de bits et y ajoute les bits de contrôle
    P=partition(L,m**2)
    N=[]
    longueur=len(P)
    for i in range(longueur):
        B=bits_de_controle(P[i],m,t)
        for j in range(len(B)):
            N.append(B[j])
    return N

def transmi_proba(L,p): #pour chaque bit d'une liste de bits L, il y a une probabilité p qu'il y ait une erreur de transmission
    for j in range(len(L)):
        if random.random()<p:
            if L[j]==0:
                L[j]=1
            else:
                L[j]=0
    return L

def recombinateur(L,m,t):#L est la liste après transmission_image , la fonction renvoie une liste décodée de binaires
    P=partition(L,m**2+2*m*t)
    p=len(P)
    CORRI=[]
    for i in range(p):
        if 10000//m**2==0 : print('recombinaison',100*i/p)
        elif i%(10000//m**2)==0: print('recombinaison',100*i/p)
        CORRI.append(decode(list(P[i]),m,t))
    CORR=[]
    for j in range(len(CORRI)):
        for k in range(len(CORRI[0])):
            CORR.append(CORRI[j][k])
    for l in range(L[1]*L[2]%(m**2)):
        a=CORR.pop()
    return CORR

def recombinateur2(L,m,t):#L est la liste après transmission_image , la fonction renvoie une liste décodée de binaires
    P=partition(L,m**2+2*m*t)
    p=len(P)
    CORRI=[]
    for i in range(p):
        CORRI.append(decode(list(P[i]),m,t))
    CORR=[]
    for j in range(len(CORRI)):
        for k in range(len(CORRI[0])):
            CORR.append(CORRI[j][k])
    for l in range(L[1]*L[2]%(m**2)):
        a=CORR.pop()
    return CORR


def transmission_image_png(T,m,t,p): #T contient le tableau numpy d'une image, m et t sont les paramètres du code correcteur. La fonction renvoit la liste de bite transmise avec une probabilité d'erreurs p
    L1=convertisseur_png_vers_binaire(T)
    L2=liste4_a_1(L1)
    L3=ajout_bits_de_controle(L2,m,t)
    L4=transmi_proba(L3,p)
    return L4,len(T),len(T[0])

def transmission_image_jpeg(T,m,t,p): #T contient le tableau numpy d'une image, m et t sont les paramètres du code correcteur. La fonction renvoit la liste de bite transmise avec une probabilité d'erreurs p
    print('Conversion jpeg vers binaire')
    L1=convertisseur_jpeg_vers_binaire(T)
    print('Conversion vers une liste simple')
    L2=liste4_a_1(L1)
    print('Ajout des bits de contrôle')
    L3=ajout_bits_de_controle(L2,m,t)
    print('Transmission')
    L4=transmi_proba(L3,p)
    print('Recombinaison')
    C=recombinateur(L4,m,t)
    print('Conversion binaire vers jpeg')
    D=convertisseur_binaire_vers_jpeg(liste1_a_4(C,len(T),len(T[0])))
    return D

def transmission_image_sans_controle_png(T,p): #Renvoie une image après une transmission sans contrôle de probabilité d'erreur p
    L1=convertisseur_png_vers_binaire(T)
    L2=liste4_a_1(L1)
    L3=transmi_proba(L2,p)
    L4=liste1_a_4(L2,len(T),len(T[0]))
    L5=convertisseur_binaire_vers_jpeg(L4)
    return L5

def transmission_image_sans_controle_jpeg(T,p): #Renvoie une image après une transmission sans contrôle de probabilité d'erreur p
    print('Conversion jpeg vers binaire')
    L1=convertisseur_jpeg_vers_binaire(T)
    print('Conversion vers une liste simple')
    L2=liste4_a_1(L1)
    print('Transmission')
    L3=transmi_proba(L2,p)
    print('Conversion vers une 4 listes imbriquées')
    L4=liste1_a_4(L2,len(T),len(T[0]))
    print('Conversion binaire vers jpeg')
    L5=convertisseur_binaire_vers_jpeg(L4)
    return L5

chdir('D:\\Aubin\\École\\MP★\\TIPE')
im = imread('bois3.jpg')
L1=list(im)
L2=convertisseur_png_vers_binaire(L1)
L3=liste4_a_1(L2)
L4=liste1_a_4(L3,18,28)
L5=convertisseur_binaire_vers_jpeg(L4)

M=list(imread("maxresdefault.jpg"))
M2=list(imread('Nuit Étoilée.jpg'))
M3=list(imread('Nuit Étoilée zoom.jpg'))
M4=list(imread('La Joconde zoom.jpg'))
M5=list(imread('fond blanc.jpg'))
M6=list(imread('fond blanc petit.jpg'))
M7=list(imread('Maison-Carrée-Nîmes.jpg'))

def statist_max(T,m,p):#Renvoie un graphe avec les proportions d'image non corigées au minimum avec les valeurs de partition entre 2 et m. Note : ce qui est long ce sont les nombres premiers et les carrés
    L=[]
    M=transmission_image_sans_controle_jpeg(T,p)
    q=proportions(T,M)
    for i in range(2,m+1):
        t=int((nb_carres_orth(i)+1)/2)
        N=transmission_image_jpeg(T,i,t,p)
        print(i)
        L.append(proportions(T,N)/q)
    figure()
    title("proportion d'erreurs non corrigées au minimum selon m")
    plot(list(range(2,m+1)),L,)
    show()

def trois_transmissions(L,p):
    M1=L[:]
    M2=L[:]
    M3=L[:]
    M1=transmi_proba(M1,p)
    M2=transmi_proba(M2,p)
    M3=transmi_proba(M3,p)
    S=[]
    for i in range(len(L)):
        v=vote([M1[i],M2[i],M3[i]])
        S.append(v)
    return S

def quatre_transmissions(L,p):
    L1=copy(L)
    L2=copy(L)
    L3=copy(L)
    T=[transmi_proba(L,p),transmi_proba(L1,p),transmi_proba(L2,p),transmi_proba(L3,p)]
    S=[]
    for i in range(len(L)):
        B=vote([T[0][i],T[1][i],T[2][i],T[3][i]])
        S.append(B)
    return S

def transmission_image_trois_transmission(T,p):
    print('Conversion jpeg vers binaire')
    L1=convertisseur_jpeg_vers_binaire(T)
    print('Conversion vers une liste simple')
    L2=liste4_a_1(L1)
    print('Transmission')
    L3=trois_transmissions(L2,p)
    print('Conversion vers une 4 listes imbriquées')
    L4=liste1_a_4(L3,len(T),len(T[0]))
    print('Conversion binaire vers jpeg')
    L5=convertisseur_binaire_vers_jpeg(L4)
    return imshow(L5)

def transmission_image_quatre_transmission(T,p):
    print('Conversion jpeg vers binaire')
    L1=convertisseur_jpeg_vers_binaire(T)
    print('Conversion vers une liste simple')
    L2=liste4_a_1(L1)
    print('Transmission')
    L3=quatre_transmissions(L2,p)
    print('Conversion vers une 4 listes imbriquées')
    L4=liste1_a_4(L2,len(T),len(T[0]))
    print('Conversion binaire vers jpeg')
    L5=convertisseur_binaire_vers_jpeg(L4)
    return imshow(L5)

def erreurs(A,B): #renvoie le nombre d'erreurs entre les deux codes A et B ainsi que la longueur de la liste analysée
    if len(A)!=len(B): print("Les listes n'ont pas la même longueur")
    c=0
    for i in range(len(A)):
        if A[i]!=B[i]:
            c+=1
    return c,len(A)

def erreurs_transmission_sans_controle(l,p): #calcule le nombre d'erreurs d'une liste de longueur l après une transmission sans contrôle de probabilité p
    L=[0]*l
    L1=transmi_proba(copy(L),p)
    return erreurs(L,L1)

def erreurs_transmission_avec_controle(l,m,t,p):
    L=[0]*l
    L1=ajout_bits_de_controle(L,m,t)
    L2=transmi_proba(L1,p)
    L3=recombinateur(L2,m,t)
    print(L3)
    return erreurs(L,L3)

def erreurs_transmission_trois_transmissions(l,p):
    L=[0]*l
    L1=trois_transmissions(L,p)
    return erreurs(L,L1)

def latin_ou_non_tous(n):
    LAT=crea_tous_carres_orth(n)
    for i in LAT:
            print(latin_ou_non(i))

def latin_ou_non(C):
    n=len(C)
    for i in range(n):#parcours vertical
        acc=[]
        for j in range(n):
            if C[i][j] in acc:
                return False
            acc.append(C[i][j])
    for i in range(n):#parcours horizontal
        acc=[]
        for j in range(n):
            if C[j][i] in acc:
                return False
            acc.append(C[j][i])
    return True

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

def greco_latin_ou_non_tous(n):
    LAT=crea_tous_carres_orth(n)
    for i in range(len(LAT)):
        for j in range(i):
            print(greco_latin_ou_non(LAT[i],LAT[j]))

def image_erreurs(I,T): #I est l'image originale, T est l'image transmise
    hau=len(I)
    lar=len(I[0])
    H=[]
    for i in range(hau):
        L=[]
        for j in range(lar):
            if listes_egales(I[i][j],T[i][j]):
                L.append([255,255,255])
            else:
                L.append([0,0,0])
        H.append(L)
    return H

def statistiques(m,t,p,n):
    E=0 #Nombre total d'erreurs
    for i in range(n):
        L=liste_aleatoire(m**2)
        M=L[:]
        L=ajout_bits_de_controle2(L,m,t)
        L=transmi_proba(L,p)
        L=decode(L,m,t)
        for j in range(m**2):
            if M[j]!=L[j]: E+=1
    return E/(n*m**2)

def liste(p_min, p_max, pas):
    p_min_1 = int(p_min * 10**10)
    p_max_1 = int(p_max * 10**10)
    pas_1 = int(pas*10**10)
    X=[i/(10**10) for i in range(p_min_1,p_max_1+pas_1,pas_1)]
    return X

def graphe_statistiques_p(m,t,p_min,p_max,pas,n):
    X=liste(p_min,p_max,pas)
    Y=[]
    for p in X:
        print(p)
        Y.append(statistiques(m,t,p,n))
    figure()
    plot(X,X)
    plot(X,Y)
    show()

def liste2(n,m):
    if n>1:
        A=liste2(n-1,m)
        l=len(A)
        B=[]
        for i in range(m):
           for j in range(l):
               C=A[j]
               B.append([i]+C)
        return B
    if n==1:
        return [[i] for i in range(m)]

def graphe_statistiques_m(m_min,m_max,p,n):
    X = list(range(m_min,m_max+1))
    Y=[]
    for m in X:
        A=liste_aleatoire(n)
        B=A[:]
        t=nb_carres_orth(m)//2+1
        print(m,t)
        A=ajout_bits_de_controle2(A,m,t)
        A=transmi_proba(A,p)
        A=recombinateur(A,m,t)
        E=0
        for i in range(n):
            if B[i]!=A[i]:
                E+=1
        Y.append(E/n)
    figure()
    plot(X,Y)
    show()

def prime(n):
    a=True
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            a=False
            break
    return a

def liste_premiers(a,b): #renvoie la liste des nombres premiers entre a et b inclus
    A=[]
    for i in range(a,b+1):
        if prime(i): A.append(i)
    return A

def graphe_statistiques_m_premier(m_min,m_max,p,n):
    X = liste_premiers(m_min, m_max)
    Y=[]
    for m in X:
        print(m)
        A=liste_aleatoire(n)
        B=A[:]
        t=nb_carres_orth(m)//2+1
        A=ajout_bits_de_controle2(A,m,t)
        A=transmi_proba(A,p)
        A=recombinateur(A,m,t)
        E=0
        for i in range(n):
            if B[i]!=A[i]:
                E+=1
        Y.append(E/n)
    figure()
    plot(X,Y)
    show()

def transmi_rafale(L,d_min,d_max,n):
    for j in range(n):
        if d_min==d_max: d=d_min
        else: d=random.randint(d_min,d_max)
        R=random.randint(0,len(L)//8-1-24*d)
        for i in range(24*R,24*R+24*d):
            L[i]=1
    return L

def transmission_erreur_de_rafale_nb(L,m,t,d_min,d_max,n):
    #L est l'image, m et t les paramètres du code correcteur, n le nombre de rafales, d_min et d_max les extrémités de taille des rafales (choisies uniformément dans cet intervalle)
    print('Conversion jpeg vers binaire')
    L1=convertisseur_jpeg_vers_binaire_nb(L)
    print('Conversion vers une liste simple')
    L2=liste3_a_1(L1)
    print('Ajout des bits de contrôle')
    L3=ajout_bits_de_controle(L2,m,t)
    L4=transmi_rafale_8bit(L3,d_min,d_max,n)
    print('Recombinaison')
    C=recombinateur(L4,m,t)
    print('Conversion binaire vers jpeg')
    D=convertisseur_binaire_vers_jpeg(liste1_a_4_nb(C,len(L),len(L[0])))
    return D

def transmission_erreur_de_rafale_sans_controle_nb(L,d_min,d_max,n):
    print('Conversion jpeg vers binaire')
    L1=convertisseur_jpeg_vers_binaire_nb(L)
    print('Conversion vers une liste simple')
    L3=liste3_a_1(L1)
    L4=transmi_rafale_8bit(L3,d_min,d_max,n)
    print('Conversion binaire vers jpeg')
    D=convertisseur_binaire_vers_jpeg(liste1_a_4_nb(L4,len(L),len(L[0])))
    return D

def graphe_statistiques_trois_transmissions(p_min,p_max,pas):
    X=liste(p_min,p_max,pas)
    Y=[]
    for p in X:
        print(p)
        Y.append(3*p**2*(1-p)+p**3)
    figure()
    plot(X,X)
    plot(X,Y)
    show()

def graphe_statistiques_trois_transmissions_2(m,t,p_min,p_max,pas,n):
    X=liste(p_min,p_max,pas)
    Y=[]
    Z=[]
    for p in X:
        print(p)
        Z.append(statistiques(m,t,p,n))
        Y.append(3*p**2*(1-p)+p**3)
    figure()
    plot(X,X)
    plot(X,Z)
    plot(X,Y)
    show()

def graphe_statistiques_p_plusieurs_m(L,p_min,p_max,pas,n):
    X=liste(p_min,p_max,pas)
    figure()
    plot(X,X)
    for (m,t) in L:
        Y=[]
        for p in X:
            print(m,t,p)
            Y.append(statistiques(m,t,p,int(n/m)))
        plot(X,Y)
    show()

def compte_erreurs(I,T): #I est l'image originale, T est l'image transmise
    hau=len(I)
    lar=len(I[0])
    C=0
    for i in range(hau):
        for j in range(lar):
            if not listes_egales(I[i][j],T[i][j]):
                C+=1
    return C

def compte_erreurs_bits(I,T): #I est l'image originale, T est l'image transmise
    C=0
    I=liste4_a_1(convertisseur_jpeg_vers_binaire(I))
    T=liste4_a_1(convertisseur_jpeg_vers_binaire(T))
    for i in range(len(I)):
        if I[i]!=T[i]: C+=1
    return C

def transmi_rafale_8bit(L,d_min,d_max,n):
    for j in range(n):
        if d_min==d_max: d=d_min
        else: d=random.randint(d_min,d_max)
        R=random.randint(0,len(L)//8-1-8*d)
        for i in range(8*R,8*R+8*d):
            L[i]=1
    return L

def liste3_a_1(L):
    N=[]
    for i in range(len(L)):
        for j in range(len(L[i])):
            for k in range(len(L[i][j])):
                N.append(L[i][j][k])
    return N

def liste1_a_4_nb(L,n,m):
    N1=[]
    c=0
    for i in range(n):
        if i%10==0 : print('liste1_a_4',100*i/n)
        N2=[]
        for j in range(m):
            N3=[[],[],[]]
            for l in range(8):
                N3[0].append(L[c])
                N3[1].append(L[c])
                N3[2].append(L[c])
                c+=1
            N2.append(N3)
        N1.append(N2)
    return N1

def convertisseur_jpeg_vers_binaire_nb(L): #Convertit des listes d'images en format jpeg en liste de listes binaires (un binaire entre 0 et 255 est codé par une liste de 0 et de 1 de longueur 8)
    hau=len(L)
    lar=len(L[0])
    M=[]
    for i in range(hau):
        M.append([])
        for j in range(lar):
            M[i].append([])
            A0=int(L[i][j][0])
            A1=int(L[i][j][1])
            A2=int(L[i][j][2])
            k=(A0+A1+A2)//3
            M[i][j]=conv_binaire(k)
    return(M)

def image_erreurs(I,T): #I est l'image originale, T est l'image transmise
    hau=len(I)
    lar=len(I[0])
    H=[]
    for i in range(hau):
        L=[]
        for j in range(lar):
            A=abs(I[i][j][0]-T[i][j][1])
            L.append([255-A,255-A,255-A])
        H.append(L)
    return H

def produit_matriciel(A,B):
    if len(A[0])!=len(B):
        return "Mauvaise taille"
    C=[]
    for i in range(len(A)):
        C.append([])
        for j in range(len(B[0])):
            S=0
            for k in range(len(B)):
                S+=A[i][k]*B[k][j]
            C[i].append(S)
    return C

def produit_matriciel_vect_binaire(A,B):
    if len(A[0])!=len(B):
        return "Mauvaise taille"
    C=[]
    for i in range(len(A)):
        S=0
        for k in range(len(B)):
            S+=A[i][k]*B[k]
        C.append(S%2)
    return C

def matH2(m,t):
    M=matH(m,t)
    for i in range(len(M)):
        M[i]=M[i][:m**2]
    return M