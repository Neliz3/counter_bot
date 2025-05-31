# Counter Bot 💰

A Telegram bot for managing personal finances, including income tracking, expense logging, category management,
statistics, and more. It supports multilingual features and uses both MongoDB and Redis for data management and caching.

---

## 📁 Project Structure

```
.
├── app.py                       # Entry point
├── config/                      # Configuration files
├── database/                    # Database models and integrations (MongoDB, Redis)
├── telegram_bot/                # Bot logic: handlers, filters, keyboards, localization, etc.
├── tests/                       # Unit tests
├── example.env                  # Example environment variables
├── requirements.txt             # Python dependencies
└── README.md
```

---

## 🚀 How to Launch the Bot

### 1. **Clone the Repository**

```bash
git clone https://github.com/Neliz3/counter_bot.git
cd counter_bot
```

### 2. **Create and Activate a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. **Install Requirements**

```bash
pip install -r requirements.txt
```

### 4. **Configure Environment Variables**

Copy `.env` from the example:

```bash
cp example.env .env
```

Edit `.env` and fill in the required values (e.g., `BOT_TOKEN`, `MONGO_URI`, `REDIS_URL`, etc.).

### 5. **Run the Bot**

```bash
python app.py
```

---

## ⚙️ Used Technologies

* **Python 3.10+**
* **MongoDB** – persistent data storage
* **Redis** – caching and user state management
* **aiogram** – asynchronous Telegram bot framework
* **pytest** – for testing

---

## 🧠 Bot Features & Commands

| Command         | Description                                 |
| --------------- | ------------------------------------------- |
| `/start`        | Starts the bot and initializes user session |
| `/add_income`   | Add a new income entry                      |
| `/add_spending` | Add a new expense                           |
| `/categories`   | Manage and view spending/income categories  |
| `/statistics`   | View financial statistics                   |
| `/cancel`       | Cancel the current action                   |

---

## 🥪 Running Tests

```bash
pytest tests/
```

---

## 🔮 Future Updates

### ✅ Income Setup

* Create and manage recurring or scheduled income types (e.g. salary, passive income).

### 🚨 Over-Budget Flags

* Notifications or visual indicators when spending exceeds a budgeted amount.

### 📝 Edit Last Entry

* Modify the most recent spending or income transaction for quick corrections.

---
