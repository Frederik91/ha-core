"""Norwegian Electricity Prices API Client."""
import datetime

import httpx


class ApiClient:
    """Class to interact with the API."""

    def __init__(self, currency: str, area_code: str) -> None:
        """Initialize."""
        self.currency = currency
        self.area_code = area_code
        self.client = httpx.AsyncClient(
            base_url="https://electricitypriceapi.azurewebsites.net"
        )

    async def get_current_price_score(self):
        """Get the current price."""

        request_url = (
            "/api/PriceScoreToday?area="
            + self.area_code
            + "&currency="
            + self.currency
            + "&format=json"
        )

        response = await self.client.get(request_url, timeout=5)
        json = response.json()

        current_hour = datetime.datetime.now().hour
        current_price = json["HourPrices"].items()[current_hour].value()

        return current_price

    async def get_current_score(self):
        """Get the current price score."""

        request_url = (
            "/api/PriceScoreToday?area="
            + self.area_code
            + "&currency="
            + self.currency
            + "&format=json"
        )

        response = await self.client.get(request_url, timeout=5)
        json = response.json()

        current_hour = datetime.datetime.now().hour
        current_score = json["HourScores"].items()[current_hour].value()

        return current_score
