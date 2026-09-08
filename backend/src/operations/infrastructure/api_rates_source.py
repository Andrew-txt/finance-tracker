from decimal import Decimal
from typing import Dict, Tuple

import aiohttp

from src.building_blocks.enum import CurrencyEnum
from src.operations.domain.currency_exchanger import IExternalSourceRatesProvider

FALLBACK_RATES: Dict[Tuple[str, str], Decimal] = {
    (CurrencyEnum.USD, CurrencyEnum.RUB): Decimal(str(95.0)),
    (CurrencyEnum.USD, CurrencyEnum.EUR): Decimal(str(0.92)),
    (CurrencyEnum.EUR, CurrencyEnum.RUB): Decimal(str(103.26)),
    (CurrencyEnum.RUB, CurrencyEnum.USD): Decimal(str(0.0105)),
    (CurrencyEnum.EUR, CurrencyEnum.USD): Decimal(str(1.087)),
    (CurrencyEnum.RUB, CurrencyEnum.EUR): Decimal(str(0.0097))
}


class ExchangeAPIRatesProvider(IExternalSourceRatesProvider):
    def __init__(self):
        self.base_url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest"


    async def healthcheck(self) -> bool:
        url = f"{self.base_url}/v1/currencies.min.json"
        timeout = aiohttp.ClientTimeout(total=5.0)
       
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return True
                return False


    async def get_rate(self, base: CurrencyEnum, target: CurrencyEnum) -> Decimal:
        url = f"{self.base_url}/v1/currencies/{base}.min.json"
        timeout = aiohttp.ClientTimeout(total=5.0)
        
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()

                    base_map = data.get(base, {})
                    rate = base_map.get(target)

            if rate and isinstance(rate, (float, int)):
                return Decimal(rate)
        except aiohttp.ClientResponseError as e: 
            return FALLBACK_RATES.get((base, target), Decimal(1))


    # class CurrencyExchangeRatesAdapter(CurrencyRate):
    # def __init__(self, base_url):
    #     self.base_url = base_url

    # async def fetch_data(self, base: str, target: str):
    #     url = f"{self.base_url}/v1/currencies/{base}.min.json"
    #     timeout = aiohttp.ClientTimeout(total=5.0)
    #     try:
    #         async with aiohttp.ClientSession(timeout=timeout) as session:
    #             async with session.get(url) as response:
    #                 response.raise_for_status()
                    
    #                 data = await response.json()
    #                 base_map = data.get(base, {})
    #                 rate = base_map.get(target)

    #         if rate is not None and isinstance(rate, (float, int)):
    #             return Decimal(rate)
    #         raise KeyError("Rate not found")
            
    #     except Exception as e:                      
    #         return e