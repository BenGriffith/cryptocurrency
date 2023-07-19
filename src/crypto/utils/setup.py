from collections import namedtuple

DayDim = namedtuple(typename="DayDim", field_names="day_key name")
MonthDim = namedtuple(typename="MonthDim", field_names="month_key name")
DateDim = namedtuple(typename="DateDim", field_names="date_key year month_key day day_key week_number week_end month_end")
NameDim = namedtuple(typename="NameDim", field_names="name_key symbol slug")
TagDim = namedtuple(typename="TagDim", field_names="tag_key tag")
NameTag = namedtuple(typename="NameTag", field_names="name_key date_key tag_key")
QuoteDim = namedtuple(typename="QuoteDim", field_names="name_key date_key quote")
PriceFact = namedtuple(typename="PriceFact", field_names="name_key date_key price")
