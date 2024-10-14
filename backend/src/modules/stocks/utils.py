from datetime import datetime


def convert_tinkoff_money_in_currency(value: dict) -> float:
    return int(value["units"]) + value["nano"] / 1e9


def convert_to_timestamp(date_string: str) -> int:
    dt = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    return int(dt.timestamp())


def convert_str_to_datetime(date_string: str) -> datetime:
    date = datetime.fromisoformat(date_string.replace("Z", "+1000"))
    if date.tzinfo:
        date = date.replace(tzinfo=None)
    return date
