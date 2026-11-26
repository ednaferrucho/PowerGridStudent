
import unittest
import xmlrunner

from Terrain import Terrain, Case

class TestTerrain(unittest.TestCase):

 #   def test_chargement(self):
#        # TODO
#        self.fail()
    def test_chargement(self):

        # Creer un terrain
        t = Terrain()

        # Charger le terrain depuis un fichier
        t.charger("terrains/t1.txt")

        # Verifier que le terrain contient des cases
        self.assertTrue(len(t.cases) > 0)

        # Verifier que la premiere ligne contient des cases
        self.assertTrue(len(t.cases[0]) > 0)

    def test_get_entree(self):
        t = Terrain()
        t.cases = [
                [Case.VIDE, Case.VIDE, Case.ENTREE],
                [Case.CLIENT, Case.CLIENT, Case.CLIENT],
        ]
        entree = t.get_entree()
        self.assertIsNotNone(entree)
        self.assertEqual(entree[0], 0)
        self.assertEqual(entree[1], 2)

    def test_accesseur(self):
        t = Terrain()
        t.cases = [
                [Case.ENTREE, Case.VIDE, Case.VIDE],
                [Case.CLIENT, Case.CLIENT, Case.CLIENT],
        ]
        self.assertEqual(t[0][0], Case.ENTREE)
        self.assertEqual(t[0][1], Case.VIDE)
        self.assertEqual(t[1][2], Case.CLIENT)

if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"))

