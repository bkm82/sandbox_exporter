from sandbox_exporter.base import NAME
from sandbox_exporter.base import get_forecast
import pytest


def test_base():
    assert NAME == "sandbox_exporter"


class Test_forecast:
    @pytest.fixture
    def forecast_fixture(self):
        mock_forecast = (
            {
                "start_date": "2024-02-19T14:04:00",
                "end_date": "2024-02-20T07:00:00",
                "name": "Tetons",
                "rating": 2,
            },
            {
                "start_date": "2024-02-19T13:56:00",
                "end_date": "2024-02-20T12:00:00",
                "name": "San Francisco Peaks / Kachina Peaks Wilderness",
                "rating": 2,
            },
            {
                "start_date": "2024-02-19T13:02:00",
                "end_date": "2024-02-20T12:00:00",
                "name": "Uintas",
                "rating": 3,
            },
        )
        return mock_forecast

    def test_get_kpac(self, forecast_fixture):
        kpac_rating = get_forecast(
            forecasts=forecast_fixture,
            name="San Francisco Peaks / Kachina Peaks Wilderness",
        )
        assert kpac_rating.get("rating") == 2

    def test_get_end_date(self, forecast_fixture):
        kpac_end_date = get_forecast(
            forecasts=forecast_fixture,
            name="San Francisco Peaks / Kachina Peaks Wilderness",
        )
        assert kpac_end_date.get("end_date") == "2024-02-20T12:00:00"
