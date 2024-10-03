import unittest
def buy_stock(stock, price, amount, bank_bal, portfolio_dict):
    if amount <= 0:  # Check for invalid buy amount (negative or zero)
        return bank_bal, portfolio_dict[stock]

    total_cost = price * amount
    if total_cost > bank_bal:  # Not enough balance to buy
        return bank_bal, portfolio_dict[stock]
    else:
        bank_bal -= total_cost
        portfolio_dict[stock] += amount
        return bank_bal, portfolio_dict[stock]

def sell_stock(stock, price, amount, bank_bal, portfolio_dict):
    if amount <= 0 or portfolio_dict[stock] < amount:  # Check for invalid sell amount or insufficient stock
        return bank_bal, portfolio_dict[stock]
    else:
        bank_bal += price * amount
        portfolio_dict[stock] -= amount
        return bank_bal, portfolio_dict[stock]


# Test class
class TestStockFunctions(unittest.TestCase):

    def setUp(self):
        """Set up initial conditions for the tests."""
        # Setting up an initial portfolio and balance for testing
        self.portfolio = {'T0': 5, 'T1': 10, 'T2': 0, 'T3': 100}
        self.initial_balance = 1000

    def test_buy_stock_success(self):
        """Test buying stock successfully when there are enough funds."""
        balance, new_stock_amount = buy_stock('T1', 50, 2, self.initial_balance, self.portfolio)
        self.assertEqual(balance, 900)  # 1000 - (50*2)
        self.assertEqual(new_stock_amount, 12)  # 10 existing + 2 bought

    def test_buy_stock_insufficient_funds(self):
        """Test that buying stock fails when there are insufficient funds."""
        balance, stock_amount = buy_stock('T1', 500, 3, self.initial_balance, self.portfolio)
        self.assertEqual(balance, 1000)  # Balance should remain unchanged
        self.assertEqual(stock_amount, 10)  # Stock amount should remain the same

    def test_sell_stock_success(self):
        """Test selling stock successfully when there are enough shares."""
        balance, new_stock_amount = sell_stock('T1', 50, 2, self.initial_balance, self.portfolio)
        self.assertEqual(balance, 1100)  # 1000 + (50*2)
        self.assertEqual(new_stock_amount, 8)  # 10 existing - 2 sold

    def test_sell_stock_insufficient_shares(self):
        """Test that selling stock fails when there are insufficient shares."""
        balance, stock_amount = sell_stock('T2', 50, 1, self.initial_balance, self.portfolio)
        self.assertEqual(balance, 1000)  # Balance should remain unchanged
        self.assertEqual(stock_amount, 0)  # Stock amount should remain unchanged

    def test_buy_stock_negative_amount(self):
        """Test that trying to buy a negative amount of stock does not change balance or stock."""
        balance, stock_amount = buy_stock('T1', 50, -3, self.initial_balance, self.portfolio)
        self.assertEqual(balance, 1000)  # Balance should remain unchanged
        self.assertEqual(stock_amount, 10)  # Stock amount should remain unchanged

    def test_sell_stock_negative_amount(self):
        """Test that trying to sell a negative amount of stock does not change balance or stock."""
        balance, stock_amount = sell_stock('T1', 50, -3, self.initial_balance, self.portfolio)
        self.assertEqual(balance, 1000)  # Balance should remain unchanged
        self.assertEqual(stock_amount, 10)  # Stock amount should remain unchanged

if __name__ == "__main__":
    unittest.main()