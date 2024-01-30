# Gevraise Mathéo, Benoit Jagueneau, tibo Opet
# Fourmi de Langton
from colorama import init, Fore, Back, Style


# fonction qui permet de se mettre à un caractère précis avec colorama
def posXY(abscisse, ordonnee):
    print("\x1b[" + str(ordonnee) + ";" + str(abscisse) + "H", end="")


# fonction qui efface ce qui est afficher
def effacerEcran():
    print("\x1b[2J", end="")


# permet de récupérer la couleur d'une case
def recup_couleur(case, Y, X):
    return case[Y][X]


# permet de récupérer les informations de la fourmie
def recup_info_fourmis(fourmis):
    return fourmis["posY"], fourmis["posX"], fourmis["direction"]


# permet de crer une matrice qui sert de map au jeu
def creeMap(colone, ligne):
    map = [[0 for i in range(colone)] for j in range(ligne)]
    return map


# permet de crer les fourmie
def creerFourmis(nombre):
    fourmis = [{"posY": 0, "posX": 0, "direction": 0} for i in range(nombre)]
    return fourmis


# permet de choisir les règles du jeu comme par exemple le nombre de couleur en plus de blanc et noir
def regles():
    reglesTemp = []
    rotation = {"D": 0, "G": 1, "U": 2, "I": 3}
    rules = [0, 1]
    regle = input(
        "Entrez les regles de la fourmi : 'G' pour gauche, 'D' pour droite, 'U' pour demi-tour, 'I' pour tous drois... "
        "une action par couleur, cela définiras le nombre de couleur et de fourmis à créer 6 max (les deux première "
        "couleur noir et blanc obligatoire sont déga définis avec droite et gauche: ")
    reglesTemp = list(regle)
    nombre = len(reglesTemp)
    if nombre == 0:
        nombre = 2
    else:
        for i in range(nombre):
            if reglesTemp[i] == "G":
                rules.append(rotation["G"])
            elif reglesTemp[i] == "D":
                rules.append(rotation["D"])
            elif reglesTemp[i] == "U":
                rules.append(rotation["U"])
            elif reglesTemp[i] == "I":
                rules.append(rotation["I"])
        nombre += 2
    return nombre, rules


# permet de choisir la position de départ d'une fourmie
def placerFourmis(fourmis):
    for i in range(len(fourmis)):
        posiY = int(input("Entrez la position Y de la fourmi : "))
        posiX = int(input("Entrez la position X de la fourmi : "))
        fourmis[i]["posY"] = posiY
        fourmis[i]["posX"] = posiX


# permet de crer un tableau de dictionnaire avec les diférentes couleurs associées à leur règle
def couleur(nombre, regles):
    couleur = [{"State": i, "Regles": regles[i]} for i in range(nombre)]
    return couleur


# permet d'afficher la map avec colorama
def afficherMap(tableauMap, fourmis, old):
    fleches = {0: "↑", 1: "→", 2: "↓", 3: "←"}
    for i in range(len(tableauMap)):
        for j in range(len(tableauMap[i])):
            if old[j][i] != tableauMap[j][i]:
                posXY(j + 1, i + 3)
                print(couleurBackAffichage[tableauMap[j][i]] + " ", end="")
    for nFourmis in range(len(fourmis)):
        Y = fourmis[nFourmis]["posY"]
        X = fourmis[nFourmis]["posX"]
        posXY(Y + 1, X + 3)
        dirF = fleches[fourmis[nFourmis]["direction"]]
        print(couleurBackAffichage[tableauMap[Y][X]] + Style.BRIGHT + couleurFondAffichage[tableauMap[Y][X]] + dirF,
              end="")
    return tableauMap


# tableau avec les différentes couleurs utilisées de colorama(utilisé juste dans la fonction afficheMap)
couleurFondAffichage = [Fore.WHITE, Fore.BLACK, Fore.BLUE, Fore.RED, Fore.MAGENTA, Fore.GREEN, Fore.CYAN, Fore.YELLOW]
couleurBackAffichage = [Back.WHITE, Back.BLACK, Back.BLUE, Back.RED, Back.MAGENTA, Back.GREEN, Back.CYAN, Back.YELLOW]


# duplique la map
def dupliqueTab(old, tableauMap):
    for i in range(len(tableauMap)):
        for j in range(len(tableauMap[i])):
            old[j][i] = tableauMap[j][i]
    return old


# fonction principale du programme
def main():
    # initialisation de toute les variables
    init()
    effacerEcran()
    nmbrCondition, Regles = regles()
    tabCouleur = couleur(nmbrCondition, Regles)
    nmbrFourmis = int(input("Entrez le nombre de fourmis : "))
    fourmis = creerFourmis(nmbrFourmis)
    colloneMap = int(input("Combien de colonnes voulez-vous ? "))
    ligneMap = int(input("Combien de lignes voulez-vous ? "))
    tableauMap = creeMap(colloneMap, ligneMap)
    old = creeMap(colloneMap, ligneMap)
    placerFourmis(fourmis)
    afficherMap(tableauMap, fourmis, old)
    dupliqueTab(old, tableauMap)
    # les input servent à ralentir le programme pour pouvoir afficher chaque étape une à une
    input()
    effacerEcran()
    print(Fore.YELLOW + " Appuillez sur 'Q' si vous voulez quitter sinon appuillez sur n'importe quel touche : ")
    # boucle pour tout répéter
    while True:
        for i in range(nmbrFourmis):
            posiY, posiX, direction = recup_info_fourmis(fourmis[i])
            couleurCase = recup_couleur(tableauMap, posiY, posiX)
            # Rotations de la fourmi en fonction de la couleur de la case sur laquelle elle se trouve
            for k in range(len(tabCouleur)):
                if tabCouleur[k]["State"] == couleurCase:
                    if tabCouleur[k]["Regles"] == 0:
                        direction += 1
                        if direction > 3:
                            direction = 0
                    if tabCouleur[k]["Regles"] == 1:
                        direction = direction - 1
                        if direction < 0:
                            direction = 3
                    if tabCouleur[k]["Regles"] == 2:
                        for rota in range(2):
                            direction += 1
                            if direction > 3:
                                direction = 0
                    fourmis[i]["direction"] = direction
            # changer la couleur de la case sur laquelle la fourmi se trouve
            posiY, posiX, direction = recup_info_fourmis(fourmis[i])
            tableauMap[posiY][posiX] += 1
            if tableauMap[posiY][posiX] > nmbrCondition - 1:
                tableauMap[posiY][posiX] = 0
            # deplacement avancer de la fourmi en fonction de sa direction
            if fourmis[i]["direction"] == 0:
                if fourmis[i]["posX"] == 0:
                    fourmis[i]["posX"] = ligneMap - 1
                else:
                    fourmis[i]["posX"] -= 1
            if fourmis[i]["direction"] == 1:
                if fourmis[i]["posY"] == colloneMap - 1:
                    fourmis[i]["posY"] = 0
                else:
                    fourmis[i]["posY"] += 1
            if fourmis[i]["direction"] == 2:
                if fourmis[i]["posX"] == ligneMap - 1:
                    fourmis[i]["posX"] = 0
                else:
                    fourmis[i]["posX"] += 1
            if fourmis[i]["direction"] == 3:
                if fourmis[i]["posY"] == 0:
                    fourmis[i]["posY"] = colloneMap - 1
                else:
                    fourmis[i]["posY"] -= 1
        afficherMap(tableauMap, fourmis, old)
        dupliqueTab(old, tableauMap)
        entre = input()
        if entre == "Q":
            break