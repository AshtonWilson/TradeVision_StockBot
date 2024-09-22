import csv

with open('portfolio', mode='w') as file:
    fieldnames = ['Balance', 'AAL', 'AAPL', 'AMZN', 'CVNA', 'ETSY', 'INTC', 'NVDA', 'PLTR', 'TSLA', 'WBA']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow(
        {'Balance': 20000, 'AAL': 5, 'AAPL': 5, 'AMZN': 5, 'CVNA': 5, 'ETSY': 5, 'INTC': 5, 'NVDA': 5, 'PLTR': 5,
         'TSLA': 5, 'WBA': 5})
