import os
from quickfs import QuickFS
from dotenv import load_dotenv
load_dotenv()

from yahooquery import search

def get_ticker_and_exchange(company_name):
    # Search for the company using yahooquery
    result = search(company_name)

    # Extract the quotes from the search results
    if 'quotes' in result:
        first_match = result['quotes'][0]  # Take the first matching result
        ticker = first_match.get('symbol')
        exchange = first_match.get('exchange')
        return ticker, exchange
    else:
        return None, None


def formatData1(data, metric):
    result = [
        {"id": 0, "series": "2014", "group": metric, "value": data[0]},
        {"id": 1, "series": "2015", "group": metric, "value": data[1]},
        {"id": 2, "series": "2016", "group": metric, "value": data[2]},
        {"id": 3, "series": "2017", "group": metric, "value": data[3]},
        {"id": 4, "series": "2018", "group": metric, "value": data[4]},
        {"id": 5, "series": "2019", "group": metric, "value": data[5]},
        {"id": 6, "series": "2020", "group": metric, "value": data[6]},
        {"id": 7, "series": "2021", "group": metric, "value": data[7]},
        {"id": 8, "series": "2022", "group": metric, "value": data[8]},
        {"id": 9, "series": "2023", "group": metric, "value": data[9]},
    ]
    return result


def formatData2(data, metric):
    result = [
        {"id": 0, "series": metric, "year": 2014, "value": data[0], "size": 100},
        {"id": 1, "series": metric, "year": 2015, "value": data[1], "size": 100},
        {"id": 2, "series": metric, "year": 2016, "value": data[2], "size": 100},
        {"id": 3, "series": metric, "year": 2017, "value": data[3], "size": 100},
        {"id": 4, "series": metric, "year": 2018, "value": data[4], "size": 100},
        {"id": 0, "series": metric, "year": 2019, "value": data[5], "size": 100},
        {"id": 1, "series": metric, "year": 2020, "value": data[6], "size": 100},
        {"id": 2, "series": metric, "year": 2021, "value": data[7], "size": 100},
        {"id": 3, "series": metric, "year": 2022, "value": data[8], "size": 100},
        {"id": 4, "series": metric, "year": 2023, "value": data[9], "size": 100},
    ]
    return result


def getFinanceData(company_name):
    ticker, exchange = get_ticker_and_exchange(company_name)
    if ticker:
        print(f"\nThe ticker symbol for {company_name} is: {ticker} on the {exchange} exchange.")
    else:
        print(f"\nNo ticker symbol found for {company_name}.")
        
    api_key = os.environ["QUICKFS_API_KEY"]
    # print("\nQUICKFS_API_KEY: "+ api_key)
    client = QuickFS(api_key)
    
    # Metrics: revenue, gross_profit, eps_basic, fcf, roe, debt_to_equity
    
    symbol = ticker
    metric = "revenue"
    metric_full_names = ["Revenue Growth", "Gross Profit", "Earnings Per Share (EPS)", "Free Cash Flow (FCF)"]
    data = client.get_data_range(symbol=f'{symbol}:US', metric=metric, period='FY-9:FY')
    data1 = formatData2(data, metric_full_names[0])
    print("\n", data1)
    
    metric = "gross_profit"
    data = client.get_data_range(symbol=f'{symbol}:US', metric=metric, period='FY-9:FY')
    data2 = formatData2(data, metric_full_names[1])
    print("\n", data2)
    
    metric = "eps_basic"
    data = client.get_data_range(symbol=f'{symbol}:US', metric=metric, period='FY-9:FY')
    data3 = formatData2(data, metric_full_names[2])
    print("\n", data3)
    
    metric = "fcf"
    data = client.get_data_range(symbol=f'{symbol}:US', metric=metric, period='FY-9:FY')
    data4 = formatData2(data, metric_full_names[3])
    print("\n", data4)

    return [data1, data2, data3, data4]
