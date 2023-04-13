import unittest
import evaluator

"""
Unit test cases
"""
class Evaluate(unittest.TestCase):
    def test(self):
        ex = evaluator.ExpressionProcessor({'a':10,'b':20, 'var':2})

        # Test a happy path
        res1 = ex.calculate('1+(2^3-4)+a-b')
        self.assertEqual(-5, res1)
        print(f"res1:{res1}")

        # Expression with spaces
        res2 = ex.calculate('1 + 2')
        self.assertEqual(3, res2)
        print(f"res2:{res2}")

        # multi-character variables
        res3 = ex.calculate('var+b-a')
        self.assertEqual(12, res3)
        print(f"res2:{res3}")

# Run all tests
tst = Evaluate().test()