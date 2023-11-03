
## **CRYPTO_EWS**

## Setup CRYPTO_EWS

|Action|Command
| :-| :-
|Create a virtual environment| python -m venv .venv
|Install relevant libraries | pip install -r requirements.txt|
|Create a .env file and add it to the root | .env
|Create json launch file| Open and Paste contents of launch_items.txt (ensure commas are correct)|
|Run Make Migrations|Run & debug -> dropdown Menu -> Make Migrations |
|If  No Migration Changes |Ensure migrations folder with blank __init__.py file in |
|Run Migrations|Run & debug -> dropdown menu -> Migrate|
|Populate Tables|Run & debug -> dropdown menu -> Populate Tables|

## Enviroment Variables

|Environment variable|value|
| :-| :-
|PEG_DEVIATION_ALERT|1
|ORDERBOOKS_REFRESH_INCREMENT_MINS|1
|DEFI_LLAMA_STABLECOIN_REFRESH_INCREMENT|5
|TIMEOUT|10
|UPDATE_REFRESH_INCREMENT_MINS|10
|MANAGER_REFRESH_INCREMENT_MINS|15
|RELEVENT_NEWS_LOOKBACK_DAYS|30
|MINIMUM_LIQUIDITY_THRESHOLD|5000
|COINMARKETCAP_BASE_URL|https://coinmarketcap.com/
|COINMARKETCAP_CCY_URL|https://api.coinmarketcap.com/data-api/v3/cryptocurrency/market-pairs/latest?slug=
|OKX_BASE_TRADING_URL|https://www.okx.com/trade-spot/
|OKX_ARTICLE_BASE_URL|https://www.okx.com/help-center/
|OKX_NEWS_DICT_URL|https://www.okx.com/v2/support/home/web
|OKX_ORDERBOOK_URL|https://www.okx.com/api/v5/market/tickers?instType=SPOT
|OKX_DELIST_URL|https://www.okx.com/api/v5/public/instruments?instType=SPOT
|BINANCE_BASE_TRADING_URL|https://www.binance.com/en/trade/
|BINANCE_ORDERBOOK_URL|https://api.binance.com/api/v3/ticker/bookTicker
|BINANCE_ARTICLE_BASE_URL|https://www.binance.com/en/support/announcement/
|BINANCE_DELIST_URL|https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true
|BINANCE_NEWS_DICT_URL|https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&pageSize=20&pageNo=1
|DEFI_LLAMA_BASE_URL|https://defillama.com/
|DEFI_LLAMA_HACKS_URL|https://defillama.com/hacks
|DEFI_LLAMA_BRIDGE_HACKS|https://defillama.com/_next/data/3b1dcc58094f2a2d31f11f4ea026016f4b4b8391/hacks.json
|DEFI_LLAMA_STABLECOIN_URL|https://defillama.com/_next/data/3b1dcc58094f2a2d31f11f4ea026016f4b4b8391/stablecoins.json
|CEX_WEBHOOK_URL| <span style="color:green">*Insert CEX Teams Webhook*</span>
|DEFI_WEBHOOK_URL| <span style="color:green">*Insert Defi Teams Webhook*</span>
|STABLECOIN_WEBHOOK_URL| <span style="color:green">*Insert Stablecoin Teams Webhook*</span>
|TOKEN_VOLATILITY_WEBHOOK_URL| <span style="color:green">*Insert Token Volatility Teams Webhook*</span>
|TOKEN_LIQUIDITY_WEBHOOK_URL| <span style="color:green">*Insert Token Liquidity Teams Webhook*</span>
|STABLECOINS|<span style="color:green">*Insert stablecoins which should require notifications*</span>
|CURRENCY_NAMES| <span style="color:green">*Insert dict of Ticker:CoinMarketCap Search name, eg. "DAI:multi-collateral-dai "* </span>
|SPOT_CURRENCIES| <span style="color:green">*Insert spot currencies which should require notifications*</span>
|USDM_CURRENCIES| <span style="color:green">*Insert Binance USDM currencies which should require notifications*</span>
|BASE_CURRENCIES| <span style="color:green">*Insert base currencies of all tickers, eg. USDT, BTC, BUSD* </span>

## Disclaimer

This trading research repository was created as a proof of concept and should not be utilized in a trading environment. The code in this repository is provided for educational purposes only, and it is the sole responsibility of the user to determine whether the code is suitable for their intended use. The author of this repository does not make any representation or warranty as to the accuracy, completeness, or reliability of the information contained herein. The user should be aware that there are risks associated with trading and that trading decisions should only be made after careful consideration of all relevant factors. The author of this repository will not be held responsible for any losses that may result from the use of this code.

## Executive Summary

This repository provides a market risk monitoring system optimized for cryptocurrency trading, which tracks market events on the Binance and OKX exchanges, as well as in the DeFi space. Its capabilities encompass tracking hard forks, delisting’s of trading pairs, stablecoin depegging incidents, DeFi hacks, token volatility, market liquidity issues, and network migrations.

At its core, the system employs a PostgreSQL database to store retrieved live market events, flagging tokens at 'high alert' if they are affected by an event. Alerts are sent via Microsoft Teams, enabling Trading Operations teams to take prompt action to secure trading exposures and shield their P&L from potential impacts. This system also provides a live materialised view, which can be utilised by live trading infrastructure to adjust params based upon live market events.

In addition to exchange-based announcements, the infrastructure leverages information from DeFi Llama, a recognized platform for tracking decentralized finance (DeFi) metrics. This integration is particularly crucial for the real-time tracking of DeFi and bridge hacks, along with the monitoring of stablecoin peg stability. Recognizing hacks or deviations from the peg in real-time is vital, as it prevents the trading system from executing trades with assets that may have depreciated unexpectedly, preventing potential losses stemming from such events.

This functionality has been achieved through code that adheres to PEP 8 standards, ensuring readability and maintainability. The codebase is modular, following the principles of interface segregation and the robust use of design patterns along with abstract base class (ABC) logic. This strategic structuring allows for targeted enhancements and adaptations without the need for widespread changes, making the system both scalable and efficient.


## Binance Workflow:
1. The process initiates by pulling data from the `BINANCE_NEWS_DICT_URL`, gathering a detailed list of all recent Binance announcements.
2. Using **Regular Expressions (Regex)**, it performs keyword classification based on the specified terms in the `EnumLowAlertWarningKeyWords` & `EnumHighAlertWarningKeyWords` files, matching against the Title and Summaries of the annoucments. This results in a list of `BinanceRawArticle` objects that contain the matched keywords.
3. As an enhancement, the program retrieves the complete announcement details, parsing the information into a `ModelBinanceEvent`. It further inspects the HTML for specific details such as the affected tickers, affected currencies, event priority, event category, and the trading status of the token during the event. This rigorous scrutiny ensures the pertinence of the announcement to trading activities.
4. Event priority is determined based on the currencies and tickers mentioned in the `SPOT_CURRENCIES` and `USDM CURRENCIES` environment variables, which represent pairs currently listed in the enviroment.
5. Finally, the `ModelBinanceEvent` objects are stored in a database. A dedicated consumer manages this database. If the event's important date is earlier than the current timestamp, the consumer checks for unicity before dispatching the `ModelBinanceEvent.ms_teams_message` to the `Webhook_URL`.
6. Reuqest and update are completed every `UPDATE_REFRESH_INCREMENT_MINS` and Db management is done every `MANAGER_REFRESH_INCREMENT_MINS`.


## OKX Workflow:
1. The process initiates by pulling data from the `OKX_NEWS_DICT_URL`, gathering a detailed list of all recent OKX announcements.
2. Using **Regular Expressions (Regex)**, it performs keyword classification based on the specified terms in the `EnumLowAlertWarningKeyWords` & `EnumHighAlertWarningKeyWords` files, matching against the Title and Summaries of the annoucments. This results in a list of `OkxRawArticle` objects that contain the matched keywords.
3. As an enhancement, the program retrieves the complete announcement details, parsing the information into a `ModelOkxEvent`. It further inspects the HTML for specific details such as the affected tickers, affected currencies, event priority, event category, and the trading status of the token during the event. This rigorous scrutiny ensures the pertinence of the announcement to trading activities.
4. Event priority is determined based on the currencies and tickers mentioned in the `SPOT_CURRENCIES` and `USDM CURRENCIES` environment variables, which represent pairs currently listed in the enviroment.
5. Finally, the `ModelOkxEvent` objects are stored in a database. A dedicated consumer manages this database. If the event's important date is earlier than the current timestamp, the consumer checks for unicity before dispatching the `ModelOkxEvent.ms_teams_message` to the `Webhook_URL`.
6. Reuqest and update are completed every `UPDATE_REFRESH_INCREMENT_MINS` and Db management is done every `MANAGER_REFRESH_INCREMENT_MINS`.

## DeFiLlama Workflow 

1. The workflow begins by sending a request to the DeFi Llama website `DEFI_LLAMA_BASE_URL`, extracting a unique hash from the HTML script tags to create a new API request URL, thus evading the standard rate limiting.
2. It employs web scraping and open API endpoints to collect information on stablecoin depegging and hacking events for further analysis.
3. Collected data is then processed into a `ModelEvent` structure. Hack events are uniquely identified by title and ID for reporting, while stablecoin depegs are tracked over an extended period for continuous reporting. These incidents are classified as high priority with affected network tokens identified by the hack or the base token of the compromised network.
4. The processed events are encapsulated as alerts in `ModelEvent` objects, which are then either updated or newly created in the system based on their uniqueness and relevance.
5. The system sends out alerts and maintains the `ModelEvent` records in a database, managed by a specialized process that ensures data integrity and relevance.
6. The entire process for data retrieval, updates, and database management is executed at predefined intervals specified by `DEFI_LLAMA_STABLECOIN_REFRESH_INCREMENT` and `DEFI_LLAMA_UPDATE_REFRESH_INCREMENT_MINS` environment variables, ensuring timely and efficient data handling.

## Token Volatility Risk View
1. The system initiates by pulling orderbook data from Binance and OKX, targeting pairs listed under `SPOT_CURRENCIES` and `USDM CURRENCIES` from environment variables, with Binance data taking precedence and OKX as secondary.
2. An observer is linked to the store_token_price_change cache, structured as a dictionary with update increments as keys. It flags pair updates when their price shifts surpass set increment levels.
3. Update increments (1, 5, 15, 30, 60 minutes, 3, 6, 12, and 24 hours) `EnumOrderbookUpdatedIncrement` are determined for the current cycle. The cache is updated accordingly, and the observer is alerted if the price update exceeds the defined threshold in `EnumWarningPriceChange`
4. Once notified, the observer creates a `ModelTokenVolatilityEvent`. If it’s a new event, it's saved; if a matching event exists, tickers are rolled forward to the new event to reflect the latest high-priority status for 24 hours post-volatility event.
5. trading operations teams can receives notifications about these volatility events through team messaging, and the materialized view is updated to show the new data.
6. This data retrieval and update cycle, including database updates, runs at regular intervals as set by the `ORDERBOOKS_REFRESH_INCREMENT_MINS` environment variable, ensuring data is managed promptly and efficiently.

## CoinMarketCap 


## Teams Alert System:

- **Alert System:** The repository is now equipped to send alert notifications through the **Microsoft Teams webhook** specified in the environment variables. This ensures timely and efficient communication of any critical events.

![Teams Message](illustrations/ews_teams_message.png)



- **Materialized View:** Users benefit from a materialized view that provides an at-a-glance understanding of all ongoing events, ensuring no critical information slips through the cracks.

