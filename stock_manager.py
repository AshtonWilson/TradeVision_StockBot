import unittest
def buy_stock(stock, price, amount, bank_bal, portfolio_dict):
    if (price * amount) > bank_bal:
        return bank_bal, portfolio_dict[stock]
    else:
        bank_bal -= (price * amount)
        portfolio_dict[stock] += amount
        return bank_bal, portfolio_dict

def sell_stock(stock, price, amount, bank_bal, portfolio_dict):
    if portfolio_dict[stock] < amount:
        return bank_bal, portfolio_dict[stock]
    else:
        bank_bal += (price*amount)
        portfolio_dict[stock] -= amount
        return bank_bal, portfolio_dict


if __name__ == "__main__":
    test_portfolio = {'T0': -5, 'T1': 0, 'T2': 5, 'T3': 100}

    print(buy_stock('T0', 100, 10, 0, test_portfolio))