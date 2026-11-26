
from Terrain import Terrain, Case
from StrategieReseau import StrategieReseau, StrategieReseauAuto

class Reseau:
    def __init__(self):
        self.strat = StrategieReseauAuto()
        self.noeuds = {}
        self.arcs = []

        self.noeud_entree = -1

    def definir_entree(self, n: int) -> None:
        if n in self.noeuds.keys():
            self.noeud_entree = n
        else:
            self.noeud_entree = -1

    def ajouter_noeud(self, n: int, coords: tuple[int, int]):
        if n >= 0:
            self.noeuds[n] = coords

    def ajouter_arc(self, n1: int, n2: int) -> None:
        if n1 > n2:
            tmp = n2
            n2 = n1
            n1 = tmp
        if n1 not in self.noeuds.keys() or n2 not in self.noeuds.keys():
            return
        if (n1, n2) not in self.arcs:
            self.arcs.append((n1, n2))

    def set_strategie(self, strat: StrategieReseau):
        self.strat = strat

#    def valider_reseau(self) -> bool:
#        # TODO
#       return False

    def valider_reseau(self) -> bool:

        # Verifier que le noeud d'entree existe
        if self.noeud_entree not in self.noeuds:
            return False

        # Verifier que deux noeuds n'occupent pas la meme position
        positions = []

        for n in self.noeuds:
            position = self.noeuds[n]

            if position in positions:
                return False

            positions.append(position)

        # Creer un dictionnaire pour stocker les voisins de chaque noeud
        voisins = {}

        for n in self.noeuds:
            voisins[n] = []

        # Verifier les connexions entre les noeuds
        for n1, n2 in self.arcs:

            # Verifier que les deux noeuds sont differents
            if n1 == n2:
                return False

            # Verifier que les deux noeuds existent
            if n1 not in self.noeuds or n2 not in self.noeuds:
                return False

            # Recuperer les positions des deux noeuds
            p = self.noeuds[n1]
            q = self.noeuds[n2]

            # Calculer la distance entre les deux noeuds
            distance = abs(p[0] - q[0]) + abs(p[1] - q[1])

            # Les noeuds doivent etre voisins horizontalement ou verticalement
            if distance != 1:
                return False

            # Enregistrer les connexions dans les deux sens
            voisins[n1].append(n2)
            voisins[n2].append(n1)

        # Verifier que tous les noeuds sont connectes au noeud d'entree
        visites = []
        a_parcourir = [self.noeud_entree]

        while len(a_parcourir) > 0:

            n = a_parcourir.pop()

            if n not in visites:
                visites.append(n)

                # Ajouter les voisins qui n'ont pas encore ete visites
                for voisin in voisins[n]:
                    if voisin not in visites and voisin not in a_parcourir:
                        a_parcourir.append(voisin)

        # Verifier que tous les noeuds ont ete visites
        if len(visites) == len(self.noeuds):
            return True
        else:
            return False

#    def valider_distribution(self, t: Terrain) -> bool:
#        # TODO
#        return False

    def valider_distribution(self, t: Terrain) -> bool:

        # Verifier que le reseau est valide
        if not self.valider_reseau():
            return False

        # Verifier la position du noeud d'entree
        if self.noeuds[self.noeud_entree] != t.get_entree():
            return False

        # Recuperer les positions de tous les noeuds
        positions = []

        for n in self.noeuds:
            positions.append(self.noeuds[n])

        # Verifier que tous les noeuds sont dans le terrain
        for position in positions:

            i = position[0]
            j = position[1]

            # Verifier que la ligne existe
            if i < 0 or i >= len(t.cases):
                return False

            # Verifier que la colonne existe
            if j < 0 or j >= len(t.cases[i]):
                return False

        # Verifier que chaque client possede un noeud
        for client in t.get_clients():

            if client not in positions:
                return False

        return True

    def configurer(self, t: Terrain):
        self.noeud_entree, self.noeuds, self.arcs  = self.strat.configurer(t)

    def afficher(self) -> None:
        # TODO
        pass

    def afficher_avec_terrain(self, t: Terrain) -> None:
        for ligne, l in enumerate(t.cases):
            for colonne, c in enumerate(l):
                if (ligne, colonne) not in self.noeuds.values():
                    if c == Case.OBSTACLE:
                        print("X", end="")
                    if c == Case.CLIENT:
                        print("C", end="")
                    if c == Case.VIDE:
                        print("~", end="")
                    if c == Case.ENTREE:
                        print("E", end="")
                    else:
                        print(" ", end="")
                else:
                    if c == Case.OBSTACLE:
                        print("T", end="")
                    if c == Case.CLIENT:
                        print("C", end="")
                    if c == Case.VIDE:
                        print("+", end="")
                    if c == Case.ENTREE:
                        print("E", end="")
                    else:
                        print(" ", end="")
            print()

    def calculer_cout(self, t: Terrain) -> float:
        cout = 0
        for _ in self.arcs:
            cout += 1.5
        for n in self.noeuds.values():
            if t[n[0]][n[1]] == Case.OBSTACLE:
                cout += 2
            else:
                cout += 1
        return cout
