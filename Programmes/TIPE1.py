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
#complexité : 2*n^2

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



def generateur_tous_carres_ordre_six():
    T=[]#T contiendra toutes les carres latins possibles
    J=[[2],[2,3],[3],[2,4],[3,4],[4],[2,5],[3,5],[4,5],[5],[2,6],[3,6],[4,6],[5,6],[6],[2,3],[2,4],[3,4],[2,5],[3,5],[4,5],[2,6],[3,6],[4,6],[5,6]]#J stocke les les valeurs deja prises à l'indice i  et est indexé comme CONV
    PARCOURS=[0,1,15,3,2,16,6,4,17,18,10,7,5,19,21,11,8,20,22,12,9,23,13,24,14]
    CONV=[[],[0],[15],[0,1],[15,2],[16,17],[0,1,3],[15,2,4],[16,17,5],[18,19,20],[0,1,3,6],[15,2,4,7],[16,17,5,8],[18,19,20,9],[21,22,23,24],[0],[0,15],[1,2],[0,15,16],[1,2,17],[3,4,5],[0,15,16,18],[1,2,17,19],[3,4,5,20],[6,7,8,9]]
    PARCINV=[0,1,4,3,7,12,6,11,16,20,10,15,19,22,24,2,5,9,14,8,13,18,17,21,23]
    for i in range(1260):#Voir le schema du nombre maximum de possibiltés : 5*(4*3)*(3*7)=1260
        L=[]
        for j in PARCOURS:
            l=len(L)
            K=[]#K stocke les valeurs interdites
            for x in CONV[j]:
                if l>PARCINV[x]:
                    K.append(L[PARCINV[x]])
            for t in range(len(J[j])):
                K.append(J[j][t])
            for k in range(1,7):
                if k not in K:
                    L.append(k)
                    J[j].append(k)
                    break
        T.append(L)
    return T

        
    
    
                