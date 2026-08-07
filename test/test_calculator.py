import unittest
from src.main import Calculator

class TestOperaciones(unittest.TestCase):
    def test_sumar(self):
        resultado = Calculator().sum(3, 2)
        self.assertEqual(resultado, 5)

if __name__ == '__main__':
    unittest.main()
