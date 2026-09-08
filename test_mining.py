import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mining import (  # noqa: E402
    apriori_frequent_itemsets,
    brute_force_frequent_itemsets,
    canonical_rules,
    generate_rules,
    load_transactions,
    support,
)


class MiningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data_path = Path(__file__).resolve().parents[1] / "data" / "db1.txt"
        cls.transactions = load_transactions(data_path)

    def test_database_has_expected_shape(self):
        self.assertEqual(len(self.transactions), 20)
        self.assertTrue(all(len(row) == len(set(row)) for row in self.transactions))

    def test_support(self):
        self.assertAlmostEqual(
            support(frozenset({"apples"}), self.transactions), 6 / 20
        )

    def test_algorithms_return_identical_itemsets(self):
        brute = brute_force_frequent_itemsets(self.transactions, 0.10)
        apriori = apriori_frequent_itemsets(self.transactions, 0.10)
        self.assertEqual(brute, apriori)

    def test_algorithms_return_identical_rules(self):
        brute = brute_force_frequent_itemsets(self.transactions, 0.10)
        apriori = apriori_frequent_itemsets(self.transactions, 0.10)
        brute_rules = generate_rules(brute, 0.50)
        apriori_rules = generate_rules(apriori, 0.50)
        self.assertEqual(canonical_rules(brute_rules), canonical_rules(apriori_rules))

    def test_invalid_thresholds_are_rejected(self):
        with self.assertRaises(ValueError):
            apriori_frequent_itemsets(self.transactions, 0)
        with self.assertRaises(ValueError):
            generate_rules({}, 1.1)


if __name__ == "__main__":
    unittest.main()
