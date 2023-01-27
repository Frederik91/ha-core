"""Norwegian Electricity Prices API Client."""

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

    async def async_get_current_price(self) -> float:
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

        current_price = json["PriceNow"]
        return current_price

    async def async_get_current_score(self) -> int:
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

        current_score = json["ScoreNow"]
        return current_score
