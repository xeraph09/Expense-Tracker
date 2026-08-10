import unittest

import expenses


class ExpenseFunctionsTests(unittest.TestCase):
    def test_resolve_category_accepts_number(self):
        self.assertEqual(expenses.resolve_category("2"), "Transport")

    def test_resolve_category_accepts_name(self):
        self.assertEqual(expenses.resolve_category("Food"), "Food")

    def test_update_expense_changes_fields(self):
        expenses_list = [{"description": "Lunch", "category": "Food", "amount": 10.0}]
        expenses.update_expense(expenses_list, 0, "name", "Dinner")
        self.assertEqual(expenses_list[0]["description"], "Dinner")

        expenses.update_expense(expenses_list, 0, "category", "Bills")
        self.assertEqual(expenses_list[0]["category"], "Bills")

        expenses.update_expense(expenses_list, 0, "amount", 15.5)
        self.assertEqual(expenses_list[0]["amount"], 15.5)


if __name__ == "__main__":
    unittest.main()
