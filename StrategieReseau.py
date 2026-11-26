
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
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:
        # TODO
        return -1, {}, []

