Gets data from sources and adds it to the respective json lines files and sqlite tables and saves it using GitHub actions. JSON lines files are used as a raw/bronze layer if needed later and the sqlite DB is used as a silver/gold layer. Logs are for analysis and the GH action is setup to send me an email if something breaks (unlikely since this is such a small project but nice to have in case). 

EPS table example (column names below):
![image](https://github.com/user-attachments/assets/dde92bdb-c0ec-46d2-9cdb-80d13982ff4e)
last_yr_rpt_date, last_yr_eps, time, ticker, name, market_cap, fiscal_quarter_end, eps_forecast, num_ests, created_date, pk


IPO table example (column names below):
![image](https://github.com/user-attachments/assets/46f3f2c9-c3f2-4a25-886f-933e8f906735)
deal_id, proposed_ticker_symbol, company_name, proposed_exchange, proposed_share_price, shares_offered, priced_date, dollar_value_of_shares_offered, deal_status, expected_price_date, filed_date, proposed_share_price_numeric

I'm not sure how the earnings calendar is created at the source but it seems fairly reliable for mid/large cap companies and a bit off for smaller cap companies that might not send out a press release with their expected earnings dates. No clue how the IPO calendar is calculated, I would guess some process scrapes the IPO filings from SEC/Edgar. 
