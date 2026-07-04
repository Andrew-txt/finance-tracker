from decimal import Decimal
import aiohttp

from src.operations.domain.currency_exchanger import ICurrencyRates


class CurrencyExchangeRatesAdapter(ICurrencyRates):
    def __init__(self, base_url):
        self.base_url = base_url

    async def fetch_data(self, base: str, target: str):
        url = f"{self.base_url}/v1/currencies/{base}.min.json"
        timeout = aiohttp.ClientTimeout(total=5.0)
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    
                    data = await response.json()
                    base_map = data.get(base, {})
                    rate = base_map.get(target)

            if rate is not None and isinstance(rate, (float, int)):
                return Decimal(rate)
            raise KeyError("Rate not found")
            
        except Exception as e:                      
            return e
        
