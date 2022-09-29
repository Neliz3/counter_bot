# Counter-hack Bot

#### Telegram Bot for dealing with Google Sheets in Python using sqlite3, python-telegram-bot and gspread library
[Counter-hack](https://t.me/counter_hack_bot) helps to count money (or something else in future) getting numbers and categories from a user.

* [Sqlite3](https://docs.python.org/3/library/sqlite3.html) database is used for data storage.

* The bot, receiving a request from the user, processes it using the [python-telegram-bot](https://pypi.org/project/python-telegram-bot/#introduction)
  library, which interacts with the Telegram bot API.

* [gspread](https://docs.gspread.org/en/latest/index.html) is a Python API for Google Sheets.


## Table of contents
* [How to use it](#How-to-use-it)
* [Setup](#Setup)
    * [Technologies Used](#Technologies-Used)
    * [Installation](#Installation)
    * [Step by step installation](#Step-by-step-installation-(for-developers))
    * [Project status](#Project-status)
    * [Room for improvement](#Room-for-improvement)
        * [Future features](#Future-features)
        * [Future changing](#Future-changing)

## How to use it
1. Open [Google Sheets template](https://docs.google.com/spreadsheets/d/1C-Z0OPYnyKPSjn8_YvrpE4uFIPiw0xQrSTn2OHhPVO4/edit#gid=1785411570)
2. Click 'Share access' for editing with
`telegram-bot-service@counter-bot-361806.iam.gserviceaccount.com`
3. Copy URL of a page and send it to [Counter-hack bot](https://t.me/counter_hack_bot)


## Setup
* All packages are located in requirements.txt
* Environmental variables are located in .env
  (you must change example.env file)
  

### Technologies Used
* Python 3.8
* sqlite3
* python-telegram-bot
* gspread

### Installation
```python3 -m venv env```


```. env/bin/activate```


```pip install -r requirements.txt```


### Step by step installation (for developers)
Install [python-telegram-bot](https://pypi.org/project/python-telegram-bot/#introduction)
library

```bash
pip install python-telegram-bot --upgrade
```

Then install ...

```bash
pip install telegram
```

Then library for getting environmental variables:

```bash
pip install python-dotenv
```

Install [a gspread library](https://docs.gspread.org/en/latest/index.html) (a Python API for Google Sheets)

```bash
pip install gspread
```


### Project status
Project is in progress

### Room for improvement
#### Future features
* Adding new languages
* Adding feature for an admin to get more statistic information
* Bot will create its own table with all values, user need only click start, pass authentication and choose a template

#### Future changing
* Replace polling with webhook
* Check if the name of a sheet is equal to a month and create a new one if not
