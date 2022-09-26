# Counter Telegram Bot

Counter is Telegram Bot for dealing with Google Sheets.


## Installation
```python3 -m venv env```


```. env/bin/activate```


```pip install -r requirements.txt```


### Step-by-step:
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


## How to use it?
1. Open [Google Sheets template](https://docs.google.com/spreadsheets/d/1C-Z0OPYnyKPSjn8_YvrpE4uFIPiw0xQrSTn2OHhPVO4/edit#gid=1785411570)
2. Click 'File'
3. Click 'Make a copy'
4. Choose a name and click 'Make a copy'
5. Click 'Share' and share access for editing with
`telegram-bot-service@counter-bot-361806.iam.gserviceaccount.com`
   
6. Copy URL of a page and send it to Counter Bot
7. Use Counter Bot and see results!
