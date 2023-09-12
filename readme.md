
## **WX_EWS**
![Wirex_logo](wirex_logo.png)

## Setup WX_EWS

|Action|Command
| :-| :-
|Create a virtual environment| python -m venv .venv
|Install relevant libraries | pip install -r requirements.txt|
|Create a .env file and add it to the root | .env
|Create json launch file| Open and Paste contents of launch_items.txt (ensure commas are correct)|
|register models in  deribit_arb_app\models.py | Models in list_of models.txt|
|Run Make Migrations|Run & debug -> dropdown Menu -> Make Migrations |
|If  No Migration Changes |Ensure migrations folder with blank __init__.py file in |
|Run Migrations|Run & debug -> dropdown menu -> Migrate|

## Enviroment Variables

|Environment variable|value|
| :-| :-
|SPOT_CURRENCIES|
|USDM_CURRENCIES|
|REFRESH_INCREMENT_MINS|10
|RELEVENT_NEWS_LOOKBACK_DAYS|30
|WEBHOOK_URL|Create Webhook to send messages for teams
|BINANCE_ARTICLE_BASE_URL|https://www.binance.com/en/support/announcement/
|BINANCE_NEWS_DICT_URL|https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&pageSize=20&pageNo=1

## Executive Summary
This repository provides infrastructure to monitor Binance Announcements based upon classified Keywords. 

This Program works by initially pulling from the BINANCE_NEWS_DICT_URL to get a comprehensive list of all recent Binance announcements. Then it utilises Key Word Classification via Regex to identify Keywords which have been specified in the EnumLowAlertWarningKeyWords & EnumHighAlertWarningKeyWords Files and returns a List of BinanceRawArticle objects which included the keywords. 
After this classification, the program pulls the entire raw announcements, parsing it into a ModelBinanceEvent and further checking the HTML for specific information such as affected tickers, affected currencies, event priority, event category and token trading status during event. This acts as a secondary filter to ensure that the announcement is pertinent to trading operations. Event priority is assigned based upon if the affected currencies & affected tickers are listed within SPOT_CURRENCIES and USDM CURRENCIES [these Env variables reflect Pairs currently listed within Wirex].

Finally, these ModelBinanceEvent Objects are saved to DB, this DB is managed by a consumer which views at a ModelBinanceEvent’s important dates, if this date is less that the current timestamp, it will check for unicity and then send the ModelBinanceEvent.ms_teams_message into the Webhook_URL. 