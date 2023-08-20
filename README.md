# 🦁 Leo & Telegram Sudoku Bot 🧩
#### Combine the power of **🦁 Leo** and **✈️ Telegram** to play Sudoku like never before!

![Sudoku](https://i.imgur.com/5PqQoJb.jpg)

## 🚀 Introduction

This project showcases the seamless integration between the cutting-edge language of the future, **🦁 Leo** from the Aleo team, and a Python-based Telegram bot. The goal? To validate Sudoku solutions and engage users in thrilling Sudoku challenges!

## 🎥 Video Demonstration
Watch our [YouTube video demonstration](https://www.youtube.com/watch?v=PLACEHOLDER) for a hands-on look into how the bot works!

## ✨ Features
- **Sudoku Generation**: Automatic generation of Sudoku puzzles ranging from easy to extreme difficulties.
- **Compete & Conquer**: Race against other users and see where you stand. Once you complete a puzzle, your results are stored in a user rating viewable by everyone.
- **Aleo Wallet Integration**: Create a wallet in the Aleo network. This opens up avenues for deeper blockchain interactions, like Sudoku speed challenges or player competitions.
- **Wallet Display Control**: Choose whether to show or hide your wallet address among the top players.

## 📂 Project Structure
The project is bifurcated into:
1. 🦁 Leo Code
2. 🤖 Telegram Bot

Both components are neatly organized in respective folders of this repository.

## 🔧 Installation & Setup
Follow these steps for a smooth installation:
1. Open your terminal.
2. Execute `git clone https://github.com/Compich/Aleo-Sudoku-Bot.git`
3. Navigate with `cd telegram_bot` and then `pip install -r requirements.txt`
4. Proceed to `telegram_bot/config`
5. Rename `example.py` to `__init.py__`
6. Edit `example.py` in your preferred text editor and set the necessary values.
7. Repeat the database configuration in the `telegram_bot/alembic.ini` file on line 63 in the `sqlalchemy.url` parameter
8. Run the `alembic upgrade head` command to create all tables in the database

### ⚙️ Configuration Details
- `LEO_EXECUTABLE`: Path to the executable file for Leo.
- `SUDOKU_ALEO_DIR`: Path to the Leo implementation of the project (usually located beside `telegram_bot`).
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`: Your database credentials.
- `BOT_TOKEN`: Your Telegram bot token. Get yours from [BotFather](https://t.me/BotFather).

To fire up the bot: `python3 aleo_sudoku_bot`

## 📌 Prerequisites
- [🦁 Leo Language](https://developer.aleo.org/leo/installation)
- [🐍 Python 3.10+](https://www.python.org/downloads/)

> 📣 Note: If you're not keen on local installation, use our live bot: [AleoSudokuBot](https://t.me/AleoSudokuBot)

## 🎮 Running the 🦁 Leo Module Independently
If you fancy running the **🦁 Leo** module solo:
1. Head over to the `sudoku_aleo` directory.
2. Run `leo run check_for_complete "FIELD"`

Replace `FIELD` with a string in this format:
"{ r1: { c1: 7u8, c2: 0u8, ... }, r2: { c1: ... } ... r9: { c1: ... } }"

For example:<br>
```
"{ 
    r1: { c1: 7u8, c2: 0u8, c3: 0u8, c4: 0u8, c5: 5u8, c6: 3u8, c7: 0u8, c8: 0u8, c9: 0u8 }, 
    r2: { c1: 5u8, c2: 0u8, c3: 0u8, c4: 1u8, c5: 0u8, c6: 2u8, c7: 9u8, c8: 7u8, c9: 8u8 }, 
    r3: { c1: 4u8, c2: 2u8, c3: 0u8, c4: 9u8, c5: 0u8, c6: 0u8, c7: 6u8, c8: 5u8, c9: 0u8 }, 
    r4: { c1: 6u8, c2: 0u8, c3: 0u8, c4: 0u8, c5: 0u8, c6: 1u8, c7: 8u8, c8: 9u8, c9: 0u8 }, 
    r5: { c1: 0u8, c2: 1u8, c3: 0u8, c4: 8u8, c5: 0u8, c6: 7u8, c7: 5u8, c8: 6u8, c9: 4u8 }, 
    r6: { c1: 9u8, c2: 0u8, c3: 8u8, c4: 5u8, c5: 0u8, c6: 4u8, c7: 2u8, c8: 0u8, c9: 1u8 }, 
    r7: { c1: 8u8, c2: 9u8, c3: 7u8, c4: 4u8, c5: 2u8, c6: 0u8, c7: 0u8, c8: 1u8, c9: 0u8 }, 
    r8: { c1: 0u8, c2: 6u8, c3: 0u8, c4: 3u8, c5: 0u8, c6: 0u8, c7: 0u8, c8: 0u8, c9: 9u8 }, 
    r9: { c1: 1u8, c2: 5u8, c3: 3u8, c4: 7u8, c5: 8u8, c6: 0u8, c7: 4u8, c8: 0u8, c9: 6u8 } 
}"
```

If the output is `0`, congrats! Your Sudoku is spot-on. Any other number indicates an error. Numbers from `1-9` denote issues in rows, while `10-18` indicate columns (e.g., 10 means the 1st column).

## 🏆 Final Note
Best of luck! We hope to see you at the top of the leaderboard! 🌟
