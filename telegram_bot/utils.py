import datetime as dt
import subprocess


def int_list_to_str(int_list: list[int]) -> str:
    return ''.join(map(str, int_list))


def emojize_number(text: int | str) -> str:
    text = str(text)

    emojis = (
        '⭕️',
        '1️⃣',
        '2️⃣',
        '3️⃣',
        '4️⃣',
        '5️⃣',
        '6️⃣',
        '7️⃣',
        '8️⃣',
        '9️⃣'
    )
    numbers = set(text)

    for number in numbers:
        text = text.replace(number, emojis[int(number)])

    return text


def string_to_aleo_format(board_str: str) -> str:
    aleo_string = '{ '
    for i in range(9):
        aleo_string = f'{aleo_string}r{i + 1}: {{ '
        for j in range(9):
            aleo_string = f'{aleo_string}c{j + 1}: {board_str[i * 9 + j]}u8'
            if j != 8:
                aleo_string = f'{aleo_string}, '
        if i != 8:
            aleo_string = f'{aleo_string} }}, '
    aleo_string = f'{aleo_string} }} }}'
    return aleo_string


def format_timedelta(delta: dt.timedelta):
    parts = []

    seconds = int(delta.total_seconds())
    days = seconds // 86400

    if days:
        parts.append(f'{days} day{"s" if days > 1 else ""}')

    seconds -= days * 86400
    hours = seconds // 3600

    if hours:
        parts.append(f'{hours} hour{"s" if hours > 1 else ""}')

    seconds -= hours * 3600
    minutes = seconds // 60

    if minutes:
        parts.append(f'{minutes} minute{"s" if minutes > 1 else ""}')

    seconds -= minutes * 60

    if seconds:
        parts.append(f'{seconds} second{"s" if seconds > 1 else ""}')

    return ', '.join(parts)
