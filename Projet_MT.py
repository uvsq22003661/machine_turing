import copy

class MT(object):
    def __init__(self,mot = '0000', file = './'):
        self.mot = mot
        self.file = file
        self.init = None
        self.accept = None
        self.etats = None
        self.etat_courant = None
        self.transition = None
        self.tete = None
        self.nb_ruban = None
        self.ruban = []
        self.mot_final = None

    ########### Getters ###########
    def get_mot(self):
        return self.mot

    def get_init(self):
        return self.init

    def get_accept(self):
        return self.accept

    def get_etats(self):
        return self.etats

    def get_transition(self):
        return self.transition

    def get_tete(self):
        return self.tete

    def get_nb_ruban(self):
        return self.nb_ruban

    def get_ruban(self):
        return self.ruban
    
    def get_etat_courant(self):
        return self.etat_courant

    def get_mot_final(self):
        return self.mot_final

    def get_status(self):
        print (' init : ', self.get_init(), '\n',
        'accept : ', self.get_accept(), '\n',
        'etats : ',self.get_etats(), '\n',
        'etat courant : ', self.get_etat_courant(), '\n',
        'transition : ',self.get_transition(), '\n',
        'tête : ',self.get_tete(), '\n',
        'ruban : ', self.get_ruban(), '\n',
        'mot de départ : ', self.get_mot() ,'\n',
        'mot résultant : ', self.get_mot_final()
        )

    ########### Setters ###########
    def set_mot(self, mot):
        self.mot = mot


    def set_init(self, new_init):
        self.init = new_init

    def set_accept(self, new_accept):
        self.accept = new_accept

    def set_etats(self, new_etats):
        self.etats = new_etats

    def set_transition(self, new_transition):
        self.transition = new_transition

    def set_tete(self, iruban, new_tete):
        self.tete[iruban-1] = new_tete

    def set_nb_ruban(self, nombre):
        self.nb_ruban = nombre
        self.set_init_ruban_tete()

    def set_init_ruban_tete(self):
        self.ruban = [[['_'],['_']] for n in range(0,self.get_nb_ruban())]
        self.tete = [0 for n in range(0,self.get_nb_ruban())]
    
    def set_word_in_ruban(self):
        self.get_ruban()[0][1] = []
        for c in self.mot:
            self.get_ruban()[0][1].append(c)
        self.ruban[0][1].append('_')    

    def set_ruban(self,ruban):
        self.ruban = ruban

    def set_etat_courant(self, etat):
        self.etat_courant = etat

    def set_mot_final(self,mot):
        self.mot_final = mot

    ###### Lecture du fichier ######
    def lecture(self):
        configbase = {}
        contenue = False
        with open(self.file,"r") as file:
            for line in file:
                if not contenue:
                    if "nb_ruban" in line:
                        contenue = True
                        nbruban = line.strip().split(" ")
                        self.set_nb_ruban(int(nbruban[2]))
                        configbase['transition'] = []
                    else :
                        mots = line.strip().split(" ")
                        etatsacc = mots[2].replace('[', "").replace(']', "").split(",")
                        configbase[mots[0]] = etatsacc
                else:
                    if line == '\n':
                        line = file.readline()
                    etatactuel = line.strip().split(",")                
                    line = file.readline()
                    etatsfutur = line.strip().split(",")
                    line = file.readline()
                    modifetat = line.strip().split(",")
                    configbase['transition'].append((etatactuel, etatsfutur, modifetat))
        self.set_init(configbase['init'][0])
        self.set_accept(configbase['accept'])
        self.set_etats(configbase['etats'])
        self.set_transition(configbase['transition'])
        self.set_etat_courant(configbase['init'][0])

    ############# Pas #############
    def pas(self):
        # -------- Récupération des données pour effectuer le pas --------------
        etatcourant = self.get_etat_courant()
        tete = self.get_tete()
        ruban = self.get_ruban()
        enstransition = [elt for elt in self.get_transition() if elt[0][0] == etatcourant]
        # --------------------------------------------------------------------------------
                # Retourne un booléen si aucune transition n'est disponible. Il sera
                #              utilisé par la fonction suivante.
        # --------------------------------------------------------------------------------
        if len(enstransition) == 0:
            return False
        else:
            # -------------------------------------------------------------------------------- 
            #           Parcours toutes les transitions pour voir si une correspond
            #           à l'état de nos bandes. Si oui, modifie la variable verif en
            #                      True, qui sera utilisée pour la suite.
            # -------------------------------------------------------------------------------- 
            for transition in enstransition:
                verif = False
                for n in range(1, len(transition[0])):
                    # ---------------- Si la tête est dans le négatif -----------------------
                    if tete[n-1]<0:
                        if ruban[n-1][0][-(tete[n-1]+1)] == transition[0][n]:
                            verif = True
                        elif ruban[n-1][0][-(tete[n-1]+1)] != transition[0][n]:
                            verif = False
                            break
                    # ---------------- Si la tête est dans le positif -----------------------
                    else:
                        if ruban[n-1][1][tete[n-1]] == transition[0][n]:
                            verif = True
                        elif ruban[n-1][1][tete[n-1]] != transition[0][n]:
                            verif = False
                            break
                # -------------------------------------------------------------------------------- 
                #           Si verif = True applique la transition sur la bande et sur
                #                           l'état courant.
                # -------------------------------------------------------------------------------- 
                if verif == True:
                    self.set_etat_courant(transition[1][0])
                    for n in range(1, len(transition[1])):
                        if tete[n-1]<0:
                            ruban[n-1][0][-(tete[n-1]+1)] = transition[1][n]
                            if '_' not in ruban[n-1][0] or (-(tete[n-1]+1)) == len(ruban[n-1][0])-1:
                                ruban[n-1][0].append('_')
                        else:
                            ruban[n-1][1][tete[n-1]] = transition[1][n]
                            if '_' not in ruban[n-1][1] or tete[n-1] == len(ruban[n-1][1])-1:
                                ruban[n-1][1].append('_')
                        if transition[2][n-1] == '>':
                            tete[n-1] += 1
                        elif transition[2][n-1] == '<':
                            tete[n-1] -= 1
                    break
            if verif == False : 
                return False
            else : return True

    def lancement(self, mot):
        self.set_mot(mot)
        self.set_word_in_ruban()
        execution = True
        # Applique la MT tant que des transitions sont utilisables.
        while execution:
            execution = self.pas()
        etat_courant = self.get_etat_courant()
        accept = self.get_accept()
        # Si l'état final n'est pas dans la liste des états accepetants, la machine rejette, sinon la MT accepte.
        if etat_courant in accept:
            print("Accepted")
        else :
            print("Rejected")

    def lancement_detaille(self, mot):
        self.set_mot(mot)
        self.set_word_in_ruban()
        execution = True
        print('Mot de départ : ', mot)
        # Applique la MT tant que des transitions sont utilisables.
        while execution: 
            etatactuel = self.get_etat_courant()
            rubanactuel = copy.deepcopy(self.get_ruban())
            teteactuel = list(self.get_tete())
            execution = self.pas()
            if execution == True:
                # Affichage des bandes.
                print("Etat :", etatactuel,'=>', self.get_etat_courant())
                for n in range(0,len(rubanactuel)):
                    rubannv = copy.deepcopy(self.get_ruban())
                    if teteactuel[n] < 0 :
                        rubanactuel[n][0][-(teteactuel[n]+1)] = ' '.join(('\33[0;45m',rubanactuel[n][0][-(teteactuel[n]+1)],'\033[0m'))
                    else :
                        rubanactuel[n][1][teteactuel[n]] = ' '.join(('\33[0;45m',rubanactuel[n][1][teteactuel[n]],'\033[0m'))
                    if self.get_tete()[n] < 0 :
                        rubannv[n][0][-(self.get_tete()[n]+1)] = ' '.join(('\33[0;45m',rubannv[n][0][-(self.get_tete()[n]+1)],'\033[0m'))
                    else:
                        rubannv[n][1][self.get_tete()[n]] = ' '.join(('\33[0;45m',rubannv[n][1][self.get_tete()[n]],'\033[0m'))
                    actueltmp = '[ '+' , '.join(rubanactuel[n][0][::-1])+' ] ,'+' [ '+' , '.join(rubanactuel[n][1])+' ]'
                    nouveau = '[ '+' , '.join(rubannv[n][0][::-1])+' ] ,'+' [ '+' , '.join(rubannv[n][1])+' ]'
                    print('     Tête de lecture sur le ruban %s :'%(n+1),teteactuel[n],'\32',self.get_tete()[n])
                    print('     ruban :',actueltmp,'=>',nouveau,'\n')
        etat_courant = self.get_etat_courant()
        accept = self.get_accept()
        # Si l'état final n'est pas dans la liste des états accepetants, la machine rejette, sinon la MT accepte.
        if etat_courant in accept :
            print("Accepted")
        else :
            print("Rejected")

def linker(M1,M2):
    m3 = open("M3.txt", "w") # Création du ficher où sera écrit la nouvelle machine.
    m2 = open(M2, "r")
    with open(M1,"r") as m1:
        for _ in range(4): # On recupère l'entête des machines, tout en changant les noms des états de M2.
            line = m1.readline()
            if 'accept :' in line:
                m3.write(line)
                m2accept = m2.readline().split(' ')[2].replace('[','').split(']')
                m2accept = [elt for elt in m2accept if elt !='\n']
            elif 'etats :' in line:
                lineM2 = m2.readline()
                lineM2 = lineM2.split(" ")[2].replace(']','M2]')
                for elt in m2accept:
                    lineM2 = lineM2.replace(elt,'')
                line = line.replace('\n','')
                lineM1M2= line + ',' + lineM2
                m3.write(lineM1M2)
            else :
                m3.write(line)
                m2.readline()
        while line != '': # On parcours le fichier M1, en écrivant son contenu dans M3.
            line = m1.readline()
            histo = []
            if '(M2' in line : # Si dans la ligne il y a un appel de M2, on écrit les instructions concernant M2 avant de reprendre M1.
                line = line.split(')')
                line[0] = line[0].replace('(M2,','')
                modif = m1.readline()
                init = False
                with open(M2,'r') as m2:
                    for _ in range(5):
                        m2.readline()
                    stock = []
                    use = False
                    for linem2 in m2:
                        linem2 = linem2.split(',')
                        if len(linem2) != 1:
                            linetempo = ','.join(linem2[1:len(linem2)])
                            linem2 = [linem2[0],linetempo]
                        if init == False:
                            if ',' + linem2[1] == line[1]:
                                linem2[0] = linem2[0]+'M2'
                                for elt in m2accept:
                                    linem2[0] = linem2[0].replace(elt+'M2',line[0])
                                m3.write(','.join(linem2))
                                m3.write(modif)
                                m3.write('\n')
                                save = (','.join(linem2))
                                init = True
                            else:
                                linem2[0] += 'M2'
                                lignedevenir = m2.readline()
                                lignedevenir = lignedevenir.split(',')
                                lignedevenir[0] += 'M2'
                                moperation=m2.readline()
                                saut = (m2.readline())
                                stock.append([','.join(linem2),','.join(lignedevenir),moperation,saut])
                        else :
                            if len(stock) != 0 and use == False:
                                for elt in stock:
                                    for ligne in elt:
                                        m3.write(ligne)
                                use = True
                            if len(stock) == 0 and use == False:
                                m3.write(save)
                                use = True
                            if linem2[0] != '\n':
                                linem2 = ','.join(linem2)
                            else:
                                linem2 = linem2[0]
                            if '<' in linem2 or '>' in linem2 or '-' in linem2:
                                m3.write(linem2)                               
                            else :
                                if linem2 != '\n':
                                    histo.append(linem2)
                                linem2 = linem2.split(',')
                                if linem2[0] != '\n':
                                    linem2[0] = linem2[0]+'M2'
                                for elt in m2accept:
                                    linem2[0] = linem2[0].replace(elt+'M2',line[0])
                                linem2 = ','.join(linem2)
                                m3.write(linem2)
            else:    
                m3.write(line)

def simplification(M1):
    mt = MT('10', M1) # Création d'une MT pour simplifier la recherche dans les transitions.
    mt.lecture()
    m1 = open(M1, "r")
    equi = open("Equivalent.txt", "w") # Création du fichier qui contiendra la nouvelle machine.
    enstransitions = mt.get_transition() # On stock les transitions de MT dans une variable.
    asupprime = [] # Correspond aux éléments qui n'ont pas de déplacement.
    for transitions in enstransitions:
        if all(element == '-' for element in transitions[2]): # Si toutes les opérations de changement sont de position = -
            for elt in enstransitions : 
                if elt[0] == transitions[1]: # Si dans les autres transitions, une condition de départ d'une transition = sortie de la transition contenant le -
                    enstransitions.append((transitions[0],elt[1],elt[2])) # On rajoute la condition de départ de la transition contenant le - , la sortie et les opérations dans la liste des transitions.
                    asupprime.append((transitions,elt)) # On rajoute les transitions pour les supprimer.
                    break
    for elt in asupprime: # On supprime les transitions n'ayant pas de déplacement.
        enstransitions.remove(elt[0])
        enstransitions.remove(elt[1])
    # On modifie la liste des états pour ne laisser que les états présents dans la nouvelle machine.
    etatentrant = [f'[{x[0][0]}]' for x in enstransitions]
    etatsortant = [f'[{x[1][0]}]' for x in enstransitions]
    etatentrant.extend(etatsortant)
    etatentrant = list(dict.fromkeys(etatentrant))
    # Puis on écrit nos nouvelle données dans la nouvelle machine.
    for i in range(5):
        line = m1.readline()
        if i == 2:
            equi.write('etats : ' + ','.join(etatentrant) + '\n')
        else:
            equi.write(line)
    for i in range(0,len(enstransitions)):
        equi.write(','.join(enstransitions[i][0])+'\n')
        equi.write(','.join(enstransitions[i][1])+'\n')
        if i != len(enstransitions)-1:
            equi.write(','.join(enstransitions[i][2])+'\n')
            equi.write('\n')
        else:
            equi.write(','.join(enstransitions[i][2]))
   
def pas_dead(self):
    # Similaire à pas, mais renvoie soit le booléen True et la transition soit (False,False).
    etatcourant = self.get_etat_courant()
    tete = self.get_tete()
    ruban = self.get_ruban()
    enstransition = [elt for elt in self.get_transition() if elt[0][0] == etatcourant]
    if len(enstransition) == 0:
        return (False,False)
    else: 
        for transition in enstransition:
            verif = False
            for n in range(1, len(transition[0])):
                if tete[n-1]<0:
                    if ruban[n-1][0][-(tete[n-1]+1)] == transition[0][n]:
                        verif = True
                    elif ruban[n-1][0][-(tete[n-1]+1)] != transition[0][n]:
                        verif = False
                        break
                else:
                    if ruban[n-1][1][tete[n-1]] == transition[0][n]:
                        verif = True
                    elif ruban[n-1][1][tete[n-1]] != transition[0][n]:
                        verif = False
                        break
            if verif == True:
                self.set_etat_courant(transition[1][0])
                for n in range(1, len(transition[1])):
                    if tete[n-1]<0:
                        ruban[n-1][0][-(tete[n-1]+1)] = transition[1][n]
                        if '_' not in ruban[n-1][0] or (-(tete[n-1]+1)) == len(ruban[n-1][0])-1:
                            ruban[n-1][0].append('_')
                    else:
                        ruban[n-1][1][tete[n-1]] = transition[1][n]
                        if '_' not in ruban[n-1][1] or tete[n-1] == len(ruban[n-1][1])-1:
                            ruban[n-1][1].append('_')
                    if transition[2][n-1] == '>':
                        tete[n-1] += 1
                    elif transition[2][n-1] == '<':
                        tete[n-1] -= 1
                break
        if verif == False : 
            return (False,False)
        else : return (True,transition)

def lancement_dead(self,mot):
    # Similaire à lancement, sauf qu'il écrit uniquement les transitions utilisées dans un fichier no_dead.txt
    self.set_mot(mot)
    self.set_word_in_ruban()
    m3 = open("no_dead.txt", "a") # Création du fichier, où sera écrit la nouvelle machine.
    execution = True
    while execution:
        execution,transiton = pas_dead(self)
        # Si à l'éxecution du pas, il trouve une transition, il l'écrit dans la nouvelle machine.
        if type(transiton) != bool:
            m3.write(','.join(transiton[0]) + '\n')
            m3.write(','.join(transiton[1]) + '\n')
            m3.write(','.join(transiton[2]) + '\n')
            m3.write('\n')
    ruban = self.get_ruban()
    etat_courant = self.get_etat_courant()
    accept = self.get_accept()
    if etat_courant in accept :
        motnegatif = ruban[0][0][::-1]
        self.set_mot_final((''.join(elt for elt in motnegatif if elt != '_')) + (
            ''.join(elt for elt in ruban[0][1] if elt != '_')))
        print("Le code de la machine donnée, sans le code mort, à était écrit sur le fichier no_dead.txt")
    else :
        print("Les éléments de M1 ne permettent pas d'atteindre un etat acceptant.")

def deletecode(M1):
    mt = MT('10',M1)
    mt.lecture()
    m3 = open("no_dead.txt", "w")
    with open(M1,"r") as m1:
        for _ in range(5):
            m3.write(m1.readline())
    m3.close()
    mot = input('Veuillez entrer un mot qui fonctionne avec votre machine.\n')
    lancement_dead(mt,mot)

def exo2():
    mtexo2 = MT('10','Exemple.txt')
    mtexo2.lecture()
    mtexo2.pas()

def exo3():
    mtexo3 = MT('10','Exemple.txt')
    mtexo3.lecture()
    mtexo3.lancement('10')

def exo4():
    mtexo4 = MT('10','Exemple.txt')
    mtexo4.lecture()
    mtexo4.lancement_detaille('10')

def exo7():
    linker('Exo7M1.txt','Exo7M2.txt')
    mtexo7 = MT('11#10','M3.txt')
    mtexo7.lecture()
    mtexo7.lancement_detaille('11#10')
    ruban = mtexo7.get_ruban()
    motnegatif = ruban[2][0][::-1]
    mtexo7.set_mot_final((''.join(elt for elt in motnegatif if elt != '_')) + (
        ''.join(elt for elt in ruban[2][1] if elt != '_')))
    print('Mot résultant :', mtexo7.get_mot_final())

def exo8():
    linker('Exo8M1.txt','Exo8M2.txt')
    mtexo8 = MT('01#00#11#00#10','M3.txt')
    mtexo8.lecture()
    mtexo8.lancement_detaille('01#00#11#00#10')
    ruban = mtexo8.get_ruban()
    motnegatif = ruban[0][0][::-1]
    mtexo8.set_mot_final((''.join(elt for elt in motnegatif if elt != '_')) + (
        ''.join(elt for elt in ruban[0][1] if elt != '_')))
    print('Mot résultant :', mtexo8.get_mot_final())

def exo9():
    simplification('Exo9.txt')

def exo10():
    fichier = input('Veuillez entrer un fichier, pour supprimer le code mort.\n')
    deletecode(fichier)

#exo2()
#exo3()
#exo4()
#exo7()
#exo8()
#exo9()
#exo10()