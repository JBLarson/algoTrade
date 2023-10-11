import yfinance as yf
import json

def fetchStock10(ticker):
    # Get data for the past 5 years
    data = yf.download(ticker, period="10y")

    # Ensure data retrieval
    if data.empty:
        raise ValueError("No data found for this ticker")

    # Convert the data to JSON format
    data_json = data.reset_index().to_json(orient='records', date_format='iso')

    # Save the JSON data to a file
    filename = "stockData/"+str(f"{ticker}.json")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data_json)
    
    print(f"Data saved to {filename}")
