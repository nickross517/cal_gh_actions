import json
import logging
import pandas as pd
import sqlite3
from funcs import currency_convert

ipos_path = './data/ipo_data.jl'
log_path = './logs/transformation_logs.log'
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Started transformations for IPO data')


data=[]
with open(ipos_path) as f:
    for line in f:
        data.append(json.loads(line))

result = pd.DataFrame()
for json_row in data:
    daily_row = json.loads(json_row)
    created_date = pd.Timestamp.today().strftime('%Y-%m-%d')
    priced = pd.DataFrame(daily_row['data']['priced']['rows'])
    upcoming = pd.DataFrame(daily_row['data']['upcoming']['upcomingTable']['rows'])
    upcoming['dealStatus'] = 'Upcoming'
    filed = pd.DataFrame(daily_row['data']['filed']['rows'])
    filed['dealStatus'] = 'Filed'

    daily_df = pd.concat([priced, upcoming, filed], ignore_index=True)
    result = pd.concat([result, daily_df], ignore_index=True)

result['sharesOffered'] = result['sharesOffered'].str.replace(',','').astype('float')
result['proposedSharePriceNumeric'] = pd.to_numeric(result['proposedSharePrice'], errors='coerce')
result['dollarValueOfSharesOffered'] = currency_convert(result['dollarValueOfSharesOffered'])
result['pricedDate'] = pd.to_datetime(result['pricedDate'])

cols = {
    'dealID': 'deal_id',
    'proposedTickerSymbol': 'proposed_ticker_symbol',
    'companyName': 'company_name',
    'proposedExchange': 'proposed_exchange',
    'proposedSharePrice': 'proposed_share_price',
    'sharesOffered': 'shares_offered',
    'pricedDate': 'priced_date',
    'dollarValueOfSharesOffered': 'dollar_value_of_shares_offered',
    'dealStatus': 'deal_status',
    'expectedPriceDate': 'expected_price_date',
    'filedDate': 'filed_date',
    'proposedSharePriceNumeric': 'proposed_share_price_numeric'
}

result = result.rename(columns=cols)

logging.info('Finished transformations, starting ipo upload to db')

conn = sqlite3.connect('./data/finance.db')
existing_data = pd.read_sql('select deal_id from fact_ipo_cal', con=conn)
result = result[~result['deal_id'].isin(existing_data['deal_id'])]
try:
    if result.empty:
        print('no new records')
        logging.info('No new ipo records uploaded')
    else:
        result.to_sql('fact_ipo_cal', if_exists='append', con=conn, index=False)
    conn.close()
except Exception as e:
    conn.close()
    logging.error(f'Unspecified error {e}')