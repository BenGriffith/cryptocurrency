from collections import namedtuple

from typing import NamedTuple

class DayDim(NamedTuple):
    day_key: int
    name: str

class MonthDim(NamedTuple):
    month_key: int
    name: str

class DateDim(NamedTuple):
    date_key: str
    year: int
    month_key: int
    day: int
    day_key: int
    week_number: int
    week_end: str
    month_end: str

class NameDim(NamedTuple):
    name_key: str
    symbol: str
    slug: str

class TagDim(NamedTuple):
    tag_key: int
    tag: str

class NameTag(NamedTuple):
    name_key: str
    date_key: str
    tag_key: int

class QuoteDim(NamedTuple):
    name_key: str
    date_key: str
    quote: list

class PriceFact(NamedTuple):
    name_key: str
    date_key: str
    price: float

class SupplyFact(NamedTuple):
    name_key: str
    date_key: str
    circulating: float
    total: float

class RankFact(NamedTuple):
    name_key: str
    date_key: str
    rank: int

class TradingFact(NamedTuple):
    name_key: str
    date_key: str
    volume: float