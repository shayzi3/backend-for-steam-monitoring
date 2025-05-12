from enum import Enum


class Language(Enum):
     RU = "RU"
     EN = "EN"
     UA = "UA"
     
     
     
class Currency(Enum):
     RUB = "RUB"
     EUR = "EUR"
     USD = "USD"
     UAH = "UAH"
     
     
     @property
     def int_value(self) -> int:
          return {
               "RUB": 5,
               "USD": 1,
               "UAH": 18,
               "EUR": 3
          }.get(self.value)
          
          
     @classmethod
     def from_int_value(cls, value: int) -> "Currency":
          return {
               5: Currency.RUB,
               1: Currency.USD,
               18: Currency.UAH,
               3: Currency.EUR
          }.get(value)
     
     