import csv


# Read portfolio from CSV and assign variables
import csv


def read_portfolio(file):
    """reads a portfolio and returns the balance as a float and portfolio of stocks as a dict"""
    with open(file, mode='r') as file:
        reader = csv.DictReader(file)

        # Initialize variables
        balance = 0.0
        portfolio = {}

        for row in reader:
            balance = float(row['Balance'])  # Get the balance from the first row
            portfolio = {  # Build portfolio dictionary
                'AAL': int(row['AAL']),
                'AAPL': int(row['AAPL']),
                'AMZN': int(row['AMZN']),
                'CVNA': int(row['CVNA']),
                'ETSY': int(row['ETSY']),
                'INTC': int(row['INTC']),
                'NVDA': int(row['NVDA']),
                'PLTR': int(row['PLTR']),
                'TSLA': int(row['TSLA']),
                'WBA': int(row['WBA'])
            }

            # Since it's a portfolio file, there is only one row
            break

        return balance, portfolio


# Update the portfolio in the CSV file
def update_portfolio(file, balance, portfolio):
    """writes new values to portfolio for balance and stock holdings"""
    with open(file, mode='w', newline='') as file:
        fieldnames = ['Balance', 'AAL', 'AAPL', 'AMZN', 'CVNA', 'ETSY', 'INTC', 'NVDA', 'PLTR', 'TSLA', 'WBA']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            'Balance': balance,
            'AAL': portfolio['AAL'],
            'AAPL': portfolio['AAPL'],
            'AMZN': portfolio['AMZN'],
            'CVNA': portfolio['CVNA'],
            'ETSY': portfolio['ETSY'],
            'INTC': portfolio['INTC'],
            'NVDA': portfolio['NVDA'],
            'PLTR': portfolio['PLTR'],
            'TSLA': portfolio['TSLA'],
            'WBA': portfolio['WBA']
        })
