import copy as cp

class automate:
    """
    classe de manipulation des automates
    l'alphabet est l'ensemble des caractères alphabétiques minuscules
    et "E" pour epsilon, et "O" pour l'automate vide
    """

    def __init__(self, expr="O"):
        """
        construit un automate élémentaire pour une expression régulière expr
        réduite à un caractère de l'alphabet, ou automate vide si "O"
        identifiant des états = entier de 0 à n-1 pour automate à n états
        état initial = état 0
        """

        # alphabet
        self.alphabet = list("abc")
        # l'expression doit contenir un et un seul caractère de l'alphabet
        if expr not in (self.alphabet + ["O", "E"]):
            raise ValueError("l'expression doit contenir un et un seul\
                           caractère de l'alphabet " + str(self.alphabet))
        # nombre d'états
        if expr == "O":
            # langage vide
            self.n = 1
        elif expr == "E":
            self.n = 1
        else:
            self.n = 2
        # états finals: liste d'états (entiers de 0 à n-1)
        if expr == "O":
            self.final = []
        elif expr == "E":
            self.final = [0]
        else:
            self.final = [1]
        # transitions: dico indicé par (état, caractère) qui donne
        # la liste des états d'arrivée
        self.transition = {} if (expr in ["O", "E"]) else {(0, expr): [1]}
        # nom de l'automate: obtenu par application des règles de construction
        self.name = "" if expr == "O" else "(" + expr + ")"

    def __str__(self):
        """affichage de l'automate par fonction print"""
        res = "Automate " + self.name + "\n"
        res += "Nombre d'états " + str(self.n) + "\n"
        res += "Etats finals " + str(self.final) + "\n"
        res += "Transitions:\n"
        for k, v in self.transition.items():
            res += str(k) + ": " + str(v) + "\n"
        res += "*********************************"
        return res

    def ajoute_transition(self, q0, a, qlist):
        """ ajoute la liste de transitions (q0, a, q1) pour tout q1
            dans qlist à l'automate
            qlist est une liste d'états
        """
        if not isinstance(qlist, list):
            raise TypeError("Erreur de type: ajoute_transition requiert une",
                            "liste à ajouter")
        if (q0, a) in self.transition:
            self.transition[(q0, a)] = self.transition[(q0, a)] + qlist
        else:
            self.transition.update({(q0, a): qlist})


def concatenation(a1, a2):  # ines
    """Retourne l'automate qui reconnaît la concaténation des
    langages reconnus par les automates a1 et a2"""
    a1 = cp.deepcopy(a1)
    a2 = cp.deepcopy(a2)

    # on crée un nouvel automate a avec:
    res = automate("O")
    # alphabet = union des alphabets
    res.alphabet = sorted(list(set(a1.alphabet + a2.alphabet)))
    # etats = union des états
    decalage = a1.n
    res.n = a1.n + a2.n
    res.initial = 0
    # q0 = l'état initial de q0

    # Transition = l'union des transitions de a1 et a2 union
    res.transition = cp.deepcopy(a1.transition)
    for (depart, symbole), arrivees in a2.transition.items():
        res.ajoute_transition(depart + decalage,
                              symbole,
                              [etat + decalage for etat in arrivees])
    # pour chaque état final de a1 on crée une transition vers 
    # l'état initial de a2
    for etat_final in a1.final:
        res.ajoute_transition(etat_final, "E", [decalage])

    # états finaux = états finaux de a2
    res.final = [etat + decalage for etat in a2.final]
    res.name = a1.name + "." + a2.name
    return res


def union(a1, a2):  # ines
    """Retourne l'automate qui reconnaît l'union des
    langages reconnus par les automates a1 et a2"""
    a1 = cp.deepcopy(a1)
    a2 = cp.deepcopy(a2)

    # on crée un nouvel automate a avec:
    res = automate("O")
    # alphabet = union des alphabets
    res.alphabet = sorted(list(set(a1.alphabet + a2.alphabet)))
    # etats = union des états a1 et a2 union un nouveau q0
    decalage_a1 = 1
    decalage_a2 = 1 + a1.n
    res.n = 1 + a1.n + a2.n
    # q0 = le nouvel état q0
    res.initial = 0
    # Transition = l'union des transitions de a1 et a2 union
    res.transition = {}
    for (depart, symbole), arrivees in a1.transition.items():
        res.ajoute_transition(depart + decalage_a1,
                              symbole,
                              [etat + decalage_a1 for etat in arrivees])
    for (depart, symbole), arrivees in a2.transition.items():
        res.ajoute_transition(depart + decalage_a2,
                              symbole,
                              [etat + decalage_a2 for etat in arrivees])
    # le nouveau q0 relié aux états initiaux de a1 et a2
    res.ajoute_transition(0, "E", [decalage_a1])
    res.ajoute_transition(0, "E", [decalage_a2])
    # états finaux = états finaux de a1 union ceux de a2
    res.final = ([etat + decalage_a1 for etat in a1.final] +
                 [etat + decalage_a2 for etat in a2.final])
    res.name = a1.name + "+" + a2.name
    return res


def etoile(a):  # pour laurine
    """Retourne l'automate qui reconnaît l'étoile de Kleene du
    langage reconnu par l'automate a"""
    # On note l'étoile de Kleene d'un langage L L* qui est définie par :
    #  L* = Union (L^n) avec 0 < n < +infini
    # Exemple : pour un automate a reconnaissant le langage L, l'automate a*
    #  doit reconnaitre le langage L* = {epsilon} U L U L^2 U ... U L^n-1 U L^n

    # Etape 1 : on copie pour éviter les effets de bord
    a = cp.deepcopy(a)
    anciens_etats_finaux = a.final.copy()

    q0 = 0

    # Etape 2 : L'état initial devient final
    if q0 not in a.final: 
        a.final.append(q0)

    # Etape 3 : Ajouter des epsilon transition entre les anciens états finaux
    # (qf) et les états initiaux (q0)

    for qf in anciens_etats_finaux: 
        a.ajoute_transition(qf, "E", [q0])  # q0 correspond à liste contenant q0

    return a


def acces_epsilon(a):
    """ retourne la liste pour chaque état des états accessibles par epsilon
        transitions pour l'automate a
        res[i] est la liste des états accessible pour l'état i
    """
    # on initialise la liste résultat qui contient au moins l'état i
    # pour chaque état i
    res = [[i] for i in range(a.n)]
    for i in range(a.n):
        candidats = list(range(i)) + list(range(i+1, a.n))
        new = [i]
        while True:
            # liste des epsilon voisins des états ajoutés en dernier:
            voisins_epsilon = []
            for e in new:
                if (e, "E") in a.transition.keys():
                    voisins_epsilon += [j for j in a.transition[(e, "E")]]
            # on calcule la liste des nouveaux états:
            new = list(set(voisins_epsilon) & set(candidats))
            # si la nouvelle liste est vide on arrête:
            if new == []:
                break
            # sinon on retire les nouveaux états ajoutés aux états candidats
            candidats = list(set(candidats) - set(new))
            res[i] += new
    return res


def supression_epsilon_transitions(a):
    """ retourne l'automate équivalent sans epsilon transitions
    """
    # on copie pour éviter les effets de bord
    a = cp.deepcopy(a)
    res = automate()
    res.name = a.name
    res.n = a.n
    res.final = a.final
    # pour chaque état on calcule les états auxquels il accède
    # par epsilon transitions.
    acces = acces_epsilon(a)
    # on retire toutes les epsilon transitions
    res.transition = {c: j for c, j in a.transition.items() if c[1] != "E"}
    for i in range(a.n):
        # on ajoute i dans les états finals si accès à un état final:
        if (set(acces[i]) & set(a.final)):
            if i not in res.final:
                res.final.append(i)
        # on ajoute les nouvelles transitions en parcourant
        # toutes les transitions
        for c, v in a.transition.items():
            if c[1] != "E" and c[0] in acces[i]:
                res.ajoute_transition(i, c[1], v)
    return res


def determinisation(a):  # emel
    """ retourne l'automate équivalent déterministe
        la construction garantit que tous les états sont accessibles
        automate d'entrée sans epsilon-transitions
    """
    a2 = cp.deepcopy(a)
    # on vérifie que l'automate ne contient pas de E-transition
    # si oui, on les supprime

    a2 = supression_epsilon_transitions(a2)
    # on initialise notre automate resultat
    a3 = automate("O")
    a3.name = a2.name + " déterminisé"
    a3.alphabet = a2.alphabet
    a3.initial = 0

    # on initialise nos structures
    etat_initial = (0,)
    a_traiter = [etat_initial]
    etats_connus = {etat_initial}
    transitions = {}  # on stocke temporairement nos transitions avec les tuples

    while a_traiter:
        etat_courant = a_traiter.pop(0)

        for lettre in a3.alphabet:
            dest_potentielle = []

            for sous_etat in etat_courant:
                if (sous_etat, lettre) in a2.transition:
                    dest_potentielle.extend(a2.transition[(sous_etat, lettre)])

            if dest_potentielle:
                nouveau_etat = tuple(sorted(set(dest_potentielle)))
                transitions[(etat_courant, lettre)] = [nouveau_etat]

                if nouveau_etat not in etats_connus:
                    etats_connus.add(nouveau_etat)
                    a_traiter.append(nouveau_etat)

    # convertion des tuples en entiers
    convertion = {etat: i for i, etat in enumerate(etats_connus)}

    a3.n = len(convertion)
    a3.transition = {}

    for (depart, lettre), arrivee in transitions.items():
        a3.ajoute_transition(convertion[depart], lettre, [convertion[arrivee[0]]])

    # états finaux
    a3.final = []
    for ensemble, i in convertion.items():
        if any(elt in a2.final for elt in ensemble):
            a3.final.append(i)

    return a3


def completion(a): # emel
    """ retourne l'automate a complété
        l'automate en entrée doit être déterministe
    """
    a2 = cp.deepcopy(a)
    poubelle = a2.n 
    poubelle_utilisee = False
    a2.name = a2.name + " complet "

    for etat in range(a2.n):
        lettres_presentes = []
        for transition in a2.transition:
            if transition[0] == etat:
                lettres_presentes.append(transition[1])

        for lettre in a2.alphabet:
            if lettre not in lettres_presentes:
                a2.ajoute_transition(etat, lettre, [poubelle])
                poubelle_utilisee = True

    if poubelle_utilisee:
        a2.n += 1
        for lettre in a2.alphabet:
            a2.ajoute_transition(poubelle, lettre, [poubelle])

    return a2


def minimisation(a):
    """ retourne l'automate minimum
        a doit être déterministe complet
        algo par raffinement de partition (algo de Moore)
    """
    # on copie pour éviter les effets de bord
    a = cp.deepcopy(a)
    res = automate()
    res.name = a.name

    # Étape 1 : partition initiale = finaux / non finaux
    part = [set(a.final), set(range(a.n)) - set(a.final)]
    # on retire les ensembles vides
    part = [e for e in part if e != set()]  
    # Étape 2 : raffinement jusqu’à stabilité
    modif = True
    while modif:
        modif = False
        new_part = []
        for e in part:
            # sous-ensembles à essayer de séparer
            classes = {}
            for q in e:
                # signature = tuple des indices des blocs atteints pour chaque lettre
                signature = []
                for c in a.alphabet:
                    for i, e2 in enumerate(part):
                        if a.transition[(q, c)][0] in e2:
                            signature.append(i)
                # on ajoute l'état q à la clef signature calculée
                classes.setdefault(tuple(signature), set()).add(q)
            if len(classes) > 1:
                # s'il y a >2 signatures différentes on a séparé des états dans e
                modif = True
                new_part.extend(classes.values())
            else:
                new_part.append(e)
        part = new_part
    # on réordonne la partition pour que le premier sous-ensemble soit celui qui contient l'état initial
    for i, e in enumerate(part):
        if 0 in e:
            part[0], part[i] = part[i], part[0]
            break
    # Étape 3 : on construit le nouvel automate minimal
    mapping = {}
    # on associe à chaque état q le nouvel état i
    # obtenu comme étant l'indice du sous-ensemble de part
    for i, e in enumerate(part):
        for q in e:
            mapping[q] = i

    res.n = len(part)
    res.final = list({mapping[q] for q in a.final if q in mapping})
    for i, e in enumerate(part):
        # on récupère un élément de e:
        representant = next(iter(e))
        for c in a.alphabet:
            q = a.transition[(representant, c)][0]
            res.transition[(i, c)] = [mapping[q]]
    return res


def tout_faire(a):
    a1 = supression_epsilon_transitions(a)
    a2 = determinisation(a1)
    a3 = completion(a2)
    a4 = minimisation(a3)
    return a4


def egal(a1, a2): # pour laurine
    """ retourne True si a1 et a2 sont isomorphes
        a1 et a2 doivent être minimaux
    """
    #Etape 1 : Minimisation de a1 et a2 
    a1 = tout_faire(a1)
    a2 = tout_faire(a2)

    # Etape 2 : Comparaison des deux automates
    # Deux automates sont égaux si et seulement si, après minimisation, on trouve le même nombre d'états, les mêmes états finaux, les mêmes transitiions et le même alphabet

    if a1.n != a2.n :  # comparaison du nb d'états
        return False
    if set(a1.final) != set(a2.final): # comparaison de la liste (sans doublons et dans le même ordre) états finaux
        return False
    if a1.transition != a2.transition: # comparaison des transitions
        return False
    if a1.alphabet != a2.alphabet: # comparaison de l'alphabet
        return False
    return True

    
# TESTS
# test union
a0 = automate("a")
a1 = automate("b")
a2 = union(a0, a1)

# test concatenation
a3 = concatenation(a0, a1)
print(a3)

# test etoile
a4 = etoile(a0)
print("etoile a4\n", a4)

# test determinisation
a5 = determinisation(a2)
print(a5)

# test completion
aab_deter = determinisation(a2)
a6 = completion(aab_deter)
print(a6)

# test egal
a7 = (concatenation(a5, a0))
print("egal a0, a7", egal(a0, a7))
print("egal a2, a2", egal(a2, a2))