import requests
import json
import pandas as pd

HEADERS = {
           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
           "Origin": "https://www2.sgx.com",
           "Referer": "https://www2.sgx.com/securities/securities-prices"}

# Getting selected stockcodes and corresponding bought price, quantities
with open('selected.txt') as f:
    selected_sc = f.readlines()

selected_sc = [x.replace('\n', '') for x in selected_sc]
portfolio = {x.split(',')[0]: float(x.split(',')[1]) for x in selected_sc}

# Start downloading stocks info from sgx into dataframe
req = requests.get(
            "https://api.sgx.com/securities/v1.1?excludetypes=bonds&params=nc,adjusted-vwap,b,bv,p,c,change_vs_pc,change_vs_pc_percentage,cx,cn,dp,dpc,du,ed,fn,h,iiv,iopv,lt,l,o,p_,pv,ptd,s,sv,trading_time,v_,v,vl,vwap,vwap-currency",
            headers=HEADERS)
data = json.loads(req.text)['data']
df = pd.DataFrame(data['prices'])
df = df.rename(
        columns={'b': 'Bid',
                 'lt': 'Last',
                 'bv': 'Bid_Volume',
                 'c': 'Change',
                 'sv': 'Ask_volume',
                 'h': 'High',
                 'l': 'Low',
                 'o': 'open',
                 'p': 'Change_percent',
                 's': 'Ask',
                 'vl': 'Volume',
                 'nc': 'Stock_code'}
        )

# Closing price of the portfolio
df = df[df['Stock_code'].isin(portfolio.keys())][['Stock_code', 'Last']]
df['bought_price'] = df['Stock_code'].map(portfolio)
df['percentage_changes'] = (df['Last'] - df['bought_price'])*100
# Format the percentages changes to display 2 decimal places
df['percentage_changes'] = df['percentage_changes'].apply(
                                lambda x: '{0:.2f}%'.format(x))
df.to_csv('result.csv', index=False)
