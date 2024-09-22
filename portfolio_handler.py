import csv

# Read portfolio from CSV and assign variables
def read_portfolio(file):
    with open(file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            balance = float(row['Balance'])

            return balance, portfolio

# Update the portfolio in the CSV file
def update_portfolio(file, balance, portfolio):
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


