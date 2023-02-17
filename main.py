from Projet_MT import *

def menu():
    print('\n\n\n\n')
    print("Veuillez choisir l'action à executer, parmi les choix disponibles:" )
    print('\n')
    print("   - \33[0;35mexo1\033[0m   -> Créer une machine de Turing à partir d'un code .txt.")
    print("   - \33[0;35mexo2\033[0m   -> Execute un pas de calcul pour une machine de Turing donnée.")
    print("   - \33[0;35mexo3\033[0m   -> Pour un mot donné, execute la machine de Turing donnée.")
    print("   - \33[0;35mexo4\033[0m   -> Pour un mot donné, execute la machine de Turing donnée, tout en affichant chaque étape dans le terminal.")
    print("   - \33[0;35mexo5\033[0m   -> Teste les machines de Turing suivantes: Right, Left, Search0, Search1, Erase, Copy.")
    print("   - \33[0;35mexo6\033[0m   -> Réalise un linker, pour deux machines de turing données, dont une faisant appel à l'autre.")
    print("   - \33[0;35mexo7\033[0m   -> Réalise la multiplication de deux nombres binaires donnés, selon la méthode égyptienne.")
    print("   - \33[0;35mexo8\033[0m   -> Pour un tableau donné, trie les éléments.")
    print("   - \33[0;35mexo9\033[0m   -> Pour une machine de Turing donnée, qui remplace toutes les instructions n'impliquant pas de déplacement.")
    print("   - \33[0;35mexo10\033[0m  -> Pour une machine de Turing donnée, supprime les transitions n'étant jamais utilisées.")
    print("   - \33[0;35mquit\033[0m   -> Pour mettre fin à la simulation.")
    print('\n')
    listechoix = ['exo1','exo2','exo3','exo4','exo5','exo6','exo7','exo8','exo9','exo10','quit']
    choix = input('Quelle action souhaitez-vous réaliser?\n')
    while choix not in listechoix:
        print('Le choix saisi ne fait pas parti des actions disponibles.')
        choix = input('Quelle action souhaitez-vous réaliser?\n')
    if choix == 'exo1':
        exo1()
    elif choix == 'exo2':
        exo2()
    elif choix == 'exo3':
        exo3()
    elif choix == 'exo4':
        exo4()
    elif choix == 'exo5':
        exo5()
    elif choix == 'exo6':
        exo6()
    elif choix == 'exo7':
        exo7()
    elif choix == 'exo8':
        exo8()
    elif choix == 'exo9':
        exo9()
    elif choix == 'exo10':
        exo10()

def exo1():
    m1 = input("Veuillez donner le chemin d'une machine de Turing.\n")
    mot = input("Entrez un mot pour la machine.\n")
    mt = MT(mot,m1)
    mt.lecture()
    print("La machine a été créée sur l'adresse suivante :")
    print(mt)
    print('Le statut de la machine :')
    mt.get_status()
    nvchoix = input('Voulez-vous le faire avec une autre machine?, ou un autre mot ?\nYes/No\n')
    if nvchoix.lower() == 'yes' :
        exo1()
    elif nvchoix.lower() == 'no' :
        menu()

def exo2():
    m1 = input("Veuillez donner le chemin d'une machine de Turing.\n")
    mot = input("Entrez un mot pour la machine.\n")
    mt = MT(mot,m1)
    mt.lecture()
    mt.set_word_in_ruban()
    print("La machine a été créée sur l'adresse suivante :")
    print(mt)
    print('Le statut de la machine :')
    mt.get_status()
    print('Un pas de calcul a été réalisé, voici le statut actuel:')
    mt.pas()
    mt.get_status()
    nvchoix = input('Voulez-vous le faire avec une autre machine?, ou un autre mot ?\nYes/No\n')
    if nvchoix.lower() == 'yes' :
        exo2()
    elif nvchoix.lower() == 'no' :
        menu()

def exo3():
    m1 = input("Veuillez donner le chemin d'une machine de Turing.\n")
    mot = input("Entrez un mot pour la machine.\n")
    mt = MT(mot,m1)
    mt.lecture()
    print("La machine a été créée sur l'adresse suivante :")
    print(mt)
    mt.lancement(mot)
    print('La machine a été executée, voici le statut actuel:')
    mt.get_status()
    n = int(input('Veuillez choisir le ruban à afficher contenant le mot.\n'))
    ruban = mt.get_ruban()
    motnegatif = ruban[n-1][0][::-1]
    mt.set_mot_final((''.join(elt for elt in motnegatif if elt != '_')) + (
        ''.join(elt for elt in ruban[n-1][1] if elt != '_')))
    print('Mot résultant :', mt.get_mot_final())
    nvchoix = input('Voulez-vous le faire avec une autre machine?, ou un autre mot ?\nYes/No\n')
    if nvchoix.lower() == 'yes' :
        exo3()
    elif nvchoix.lower() == 'no' :
        menu()

def exo4():
    m1 = input("Veuillez donner le chemin d'une machine de Turing.\n")
    mot = input("Entrer un mot pour la machine.\n")
    mt = MT(mot,m1)
    mt.lecture()
    print("La machine a été créée sur l'adresse suivante :")
    print(mt)
    mt.lancement_detaille(mot)
    n = int(input('Veuillez choisir le ruban à afficher contenant le mot.\n'))
    ruban = mt.get_ruban()
    motnegatif = ruban[n-1][0][::-1]
    mt.set_mot_final((''.join(elt for elt in motnegatif if elt != '_')) + (
        ''.join(elt for elt in ruban[n-1][1] if elt != '_')))
    print('Mot résultant :', mt.get_mot_final())
    nvchoix = input('Voulez-vous le faire avec une autre machine?, ou un autre mot ?\nYes/No\n')
    if nvchoix.lower() == 'yes' :
        exo4()
    elif nvchoix.lower() == 'no' :
        menu()

def exo5():
    nvchoix = input('Quelle machine souhaitez-vous tester parmi les choix suivants:?\nRight, Left, Search0, Search1, Erase, Copy\n')
    if nvchoix == 'Right':
        print('Le test de Right sera effectué avec des données prédéfinies')
        mt = MT('100','RIGHT.txt')
        mt.lecture()
        mt.set_word_in_ruban()
        print('Le statut de la machine :')
        mt.get_status()
        mt.lancement_detaille('100')
    elif nvchoix == 'Left':
        print('Le test de Left sera effectué avec des données prédéfinies')
        mt = MT('100','LEFT.txt')
        mt.lecture()
        mt.set_word_in_ruban()
        mt.set_tete(1, 2)
        print('Le statut de la machine :')
        mt.get_status()
        mt.lancement_detaille('100')
    elif nvchoix == 'Search0':
        print('Le test de Search0 sera effectué avec des données prédéfinies')
        print('On va chercher le premier 0 du mot.')
        mt = MT('100','Search0.txt')
        mt.lecture()
        print('Le statut de la machine :')
        mt.get_status()
        mt.lancement_detaille('100')
    elif nvchoix == 'Search1':
        print('Le test de Search1 sera effectué avec des données prédéfinies')
        print('On va chercher le premier 1 du mot.')
        mt = MT('001','Search1.txt')
        mt.lecture()
        print('Le statut de la machine :')
        mt.get_status()
        mt.lancement_detaille('001')  
    elif nvchoix == 'Erase':
        print('Le test de Erase sera effectué avec des données prédéfinies')
        print('On va effacer le ruban 1.')
        mt = MT('100','ERASE.txt')
        mt.lecture()
        print('Le statut de la machine :')
        mt.get_status()
        mt.lancement_detaille('100')
    elif nvchoix == 'Copy':
        print('Le test de Copy sera effectué avec des données prédéfinies')
        print('On va copier le 1er ruban sur le 2eme.')
        mt = MT('100','COPY.txt')
        mt.lecture()
        print('Le statut de la machine :')
        mt.get_status()
        mt.lancement_detaille('100')
    nvchoix = input('Voulez-vous le faire avec une autre machine?, ou un autre mot ?\nYes/No\n')
    if nvchoix.lower() == 'yes' :
        exo5()
    elif nvchoix.lower() == 'no' :
        menu()

def exo6():
    m1 = input("Veuillez donner le chemin d'une machine de Turing.\n")
    m2 = input("Veuillez donner le chemin d'une deuxième machine de Turing.\n")
    linker(m1,m2)
    print('La nouvelle machine a été écrite sur le fichier M3.')
    nvchoix = input('Voulez-vous le faire avec une autre machine?, ou un autre mot ?\nYes/No\n')
    if nvchoix.lower() == 'yes' :
        exo4()
    elif nvchoix.lower() == 'no' :
        menu()

def exo7():
    print('Multiplier deux nombres en binaire, selon  la méthode égyptienne')
    mot = input("Entrez 2 nombres binaires pour la machine, sous le format 00#11.\n")
    linker('Exo7M1.txt','Exo7M2.txt')
    mtexo7 = MT(mot,'M3.txt')
    mtexo7.lecture()
    mtexo7.lancement_detaille(mot)
    ruban = mtexo7.get_ruban()
    motnegatif = ruban[2][0][::-1]
    mtexo7.set_mot_final((''.join(elt for elt in motnegatif if elt != '_')) + (
        ''.join(elt for elt in ruban[2][1] if elt != '_')))
    print('Mot résultant :', mtexo7.get_mot_final())
    nvchoix = input('Voulez-vous le faire avec une autre machine?, ou un autre mot ?\nYes/No\n')
    if nvchoix.lower() == 'yes' :
        exo4()
    elif nvchoix.lower() == 'no' :
        menu()

def exo8():
    print('Trier un tableau')
    mot = input("Entrez un tableau pour la machine, sous le format 00#11#00.\n")
    linker('Exo8M1.txt','Exo8M2.txt')
    mtexo8 = MT(mot,'M3.txt')
    mtexo8.lecture()
    mtexo8.lancement_detaille(mot)
    ruban = mtexo8.get_ruban()
    motnegatif = ruban[0][0][::-1]
    mtexo8.set_mot_final((''.join(elt for elt in motnegatif if elt != '_')) + (
        ''.join(elt for elt in ruban[0][1] if elt != '_')))
    print('Mot résultant :', mtexo8.get_mot_final())
    nvchoix = input('Voulez-vous le faire avec une autre machine?, ou un autre mot ?\nYes/No\n')
    if nvchoix.lower() == 'yes' :
        exo4()
    elif nvchoix.lower() == 'no' :
        menu()

def exo9():
    m1 = input("Veuillez donner le chemin d'une machine de Turing.\n")
    simplification(m1)
    print('La nouvelle machine a été écrite sur le fichier M3.')
    nvchoix = input('Voulez-vous le faire avec une autre machine?, ou un autre mot ?\nYes/No\n')
    if nvchoix.lower() == 'yes' :
        exo4()
    elif nvchoix.lower() == 'no' :
        menu()

def exo10():
    m1 = input("Veuillez donner le chemin d'une machine de Turing. Pour supprimer le code mort.\n")
    deletecode(m1)
    print('La nouvelle machine a été écrite sur le fichier M3.')
    nvchoix = input('Voulez-vous le faire avec une autre machine?, ou un autre mot ?\nYes/No\n')
    if nvchoix.lower() == 'yes' :
        exo4()
    elif nvchoix.lower() == 'no' :
        menu()

menu()