
from Terrain import Terrain, Case

class StrategieReseau:
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:
        return -1, {}, []

class StrategieReseauManuelle(StrategieReseau):
    #def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:
    #    # TODO
    #    return -1, {}, []

     def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:

        # Recuperer la position de l'entree
        entree = t.get_entree()

        if entree == (-1, -1):
            return -1, {}, []

        # Initialiser le reseau
        noeuds = {0: entree}
        arcs = []

        print("Entree :", entree)

        while True:

            print("Noeuds :", noeuds)
            print("Arcs :", arcs)

            # Demander les coordonnees du nouveau noeud
            texte = input("Ligne colonne (ou fin) : ")

            if texte.strip().lower() == "fin":
                break

            # Recuperer les coordonnees
            try:
                valeurs = texte.split()
                i = int(valeurs[0])
                j = int(valeurs[1])

                if len(valeurs) != 2:
                    print("Entrez deux coordonnees.")
                    continue

            except (ValueError, IndexError):
                print("Coordonnees incorrectes.")
                continue

            # Verifier les limites du terrain
            if i < 0 or i >= len(t.cases):
                print("Ligne incorrecte.")
                continue

            if j < 0 or j >= len(t.cases[i]):
                print("Colonne incorrecte.")
                continue

            # Verifier que la position est libre
            if (i, j) in noeuds.values():
                print("Un noeud existe deja.")
                continue

            # Chercher les noeuds voisins
            voisins = []

            for n in noeuds:

                a, b = noeuds[n]

                distance = abs(i - a) + abs(j - b)

                if distance == 1:
                    voisins.append(n)

            if len(voisins) == 0:
                print("Aucun noeud voisin.")
                continue

            print("Noeuds voisins :", voisins)

            # Choisir le noeud auquel se connecter
            try:
                parent = int(input("Connecter au noeud : "))

            except ValueError:
                print("Identifiant incorrect.")
                continue

            if parent not in voisins:
                print("Le noeud choisi n'est pas voisin.")
                continue

            # Ajouter le nouveau noeud
            nouveau = len(noeuds)

            noeuds[nouveau] = (i, j)

            # Ajouter la connexion
            arcs.append((parent, nouveau))

        return 0, noeuds, arcs

class StrategieReseauAuto(StrategieReseau):
    #def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:
    #    # TODO
    #    return -1, {}, []

    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:

        # Recuperer la position de l'entree
        entree = t.get_entree()

        if entree == (-1, -1):
            return -1, {}, []

        # Initialiser le reseau
        noeuds = {0: entree}
        arcs = []

        # Positions deja connectees au reseau
        connectes = [entree]

        # Parcourir les clients
        for client in t.get_clients():

            if client in connectes:
                continue

            # Initialiser les variables de recherche
            couts = {}
            parents = {}
            a_parcourir = []
            visites = []

            # Les noeuds du reseau sont les points de depart
            for position in connectes:
                couts[position] = 0
                a_parcourir.append(position)

            # Chercher le chemin de cout minimum
            while len(a_parcourir) > 0:

                # Selectionner la position avec le cout minimum
                position = a_parcourir[0]

                for p in a_parcourir:
                    if couts[p] < couts[position]:
                        position = p

                a_parcourir.remove(position)
                visites.append(position)

                # Arreter si le client est atteint
                if position == client:
                    break

                i, j = position

                # Les quatre cases voisines
                voisins = [
                    (i - 1, j),
                    (i + 1, j),
                    (i, j - 1),
                    (i, j + 1)
                ]

                for voisin in voisins:

                    a, b = voisin

                    # Verifier les limites du terrain
                    if a < 0 or a >= len(t.cases):
                        continue

                    if b < 0 or b >= len(t.cases[a]):
                        continue

                    if voisin in visites:
                        continue

                    # Calculer le cout du nouveau noeud
                    cout_noeud = 1

                    if t[a][b] == Case.OBSTACLE:
                        cout_noeud = 2

                    # Ajouter le cout de la connexion
                    nouveau_cout = couts[position] + cout_noeud + 1.5

                    # Enregistrer un nouveau chemin ou un chemin moins cher
                    if voisin not in couts or nouveau_cout < couts[voisin]:

                        couts[voisin] = nouveau_cout
                        parents[voisin] = position

                        if voisin not in a_parcourir:
                            a_parcourir.append(voisin)

            # Verifier qu'un chemin existe
            if client not in visites:
                return -1, {}, []

            # Reconstruire le chemin depuis le client
            chemin = []
            position = client

            while position not in connectes:

                chemin.append(position)
                position = parents[position]

            # Ajouter le chemin au reseau
            precedent = position

            while len(chemin) > 0:

                position = chemin.pop()

                nouveau = len(noeuds)

                noeuds[nouveau] = position

                # Chercher l'identifiant du noeud precedent
                for n in noeuds:
                    if noeuds[n] == precedent:
                        parent = n
                        break

                # Ajouter la connexion
                arcs.append((parent, nouveau))

                connectes.append(position)

                precedent = position

        return 0, noeuds, arcs