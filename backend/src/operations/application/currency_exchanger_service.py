from decimal import Decimal
from typing import Dict, Tuple
import aiohttp
from abc import ABC, abstractmethod

from src.building_blocks.enum import CurrencyEnum
from src.operations.application.adapters import CurrencyExchangeRatesAdapter

FALLBACK_RATES: Dict[Tuple[str, str], Decimal] = {
    (CurrencyEnum.USD, CurrencyEnum.RUB): Decimal(str(95.0)),
    (CurrencyEnum.USD, CurrencyEnum.EUR): Decimal(str(0.92)),
    (CurrencyEnum.EUR, CurrencyEnum.RUB): Decimal(str(103.26)),
    (CurrencyEnum.RUB, CurrencyEnum.USD): Decimal(str(0.0105)),
    (CurrencyEnum.EUR, CurrencyEnum.USD): Decimal(str(1.087)),
    (CurrencyEnum.RUB, CurrencyEnum.EUR): Decimal(str(0.0097))
}


async def exchange_rate_service(adapter: CurrencyExchangeRatesAdapter, base: str, target: str):
    try:
        rate = await adapter.fetch_data(base=base, target=target)
        return rate
    except Exception as e:
        return FALLBACK_RATES.get((base, target), Decimal(1))
    

