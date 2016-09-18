from unittest import TestCase
import termod
class TestGasLaws(TestCase):
    def test_variable(self):
        gas = termod.GasLaws()
        variables = ("T", "P", "V", "N")
        gas.variable = "HH"
        self.assertNotEqual(gas.variable,"HH")
        for var in variables:
            gas.variable = var
            self.assertEqual(gas.variable,var)

    def test_MendKlapeiron(self):
        t = 298
        p = 100000
        v = 1
        n = 1
        gas = termod.GasLaws()
        gas.moll = n
        gas.temperature = t
        gas.pressure = p
        gas.volume = v
        #
        gas.variable = "T"
        self.assertEqual(gas.MendKlapeiron(), p * v / 8.31 / n)
        #
        gas.variable = "P"
        self.assertEqual(gas.MendKlapeiron(), 8.31 * t * n / v)
        #
        gas.variable = "V"
        self.assertEqual(gas.MendKlapeiron(), 8.31 * t * n / p)
        #
        gas.variable = "N"
        self.assertEqual(gas.MendKlapeiron(), p * v / 8.31 / t)

    #def test_VanDerVaals(self):
    #    self.fail()
