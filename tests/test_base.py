from sandbox_exporter.base import NAME
from sandbox_exporter.base import get_forecast
from sandbox_exporter.base import app
from sandbox_exporter import base
from fastapi.testclient import TestClient
import datetime
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

    # Mocked cached response
    @pytest.fixture
    def mock_current_date(self):
        return datetime.datetime(2024, 2, 20)

    @pytest.fixture
    def client(self):
        return TestClient(app)

    @pytest.fixture
    def mock_print(self):
        bray = "hello from mock"
        return bray

    @pytest.mark.asyncio
    async def test_get_avalance_forecasts(
        self, client, monkeypatch, mock_print
    ):

        # Make the request to the endpoint
        monkeypatch.setattr(base, "get_demo", lambda: mock_print)
        response = client.get("/demo-get-call")

        # Assertions
        assert response.status_code == 200
        assert response.json() == "hello from mock"

        # Ensure that get_avalanche_from_api was not called since the cached response is up-to-date
        # get_avalanche_from_api.assert_not_called()
