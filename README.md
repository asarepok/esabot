# ESA Bot

ESA Bot is a Telegram bot for academic resource management. It's designed to help students quickly access study materials without scrolling through unsorted files in Telegram channels.

Materials are organized by:
- Faculty
- Programme
- Level
- Semester
- Course

Check it out [@gctuesabot](https://t.me/gctuesabot)

---

## Features

### Student Features

- Access slides, books, past questions, timetables, and course outlines
- Request missing materials
- Receive notifications when new materials are uploaded

### Administrator Features

- Upload materials
- Organize materials by course
- View material requests

---

## Tech Stack

- Python
- PostgreSQL
- python-telegram-bot
- aiohttp
- Aerich
- Tortoise ORM

---

## Development Setup

### Clone Repository

```bash
git clone https://github.com/asarepok/esabot.git
cd esabot
```

### Install Dependencies

If you're using uv:

```bash
uv sync
```

If you're using pip:

```bash
pip install -r requirements.txt
```

### Configure Environment

```bash
cp .env.example .env
```

### Configure Database

Initialize the database:

```bash
aerich init-db
```

Apply future migrations:

```bash
aerich upgrade
```

### Start Application

```bash
python main.py
```

---

## License

This project is licensed under the Apache License 2.0.

See the [LICENSE](LICENSE) file for details.