"""
coinflip API base module.

This module creates a coin flip API.

"""

import random

import prometheus_client
import requests  # type: ignore
import uvicorn
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

NAME = "sandbox_exporter"
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

heads_count = prometheus_client.Counter(
    "heads_count",
    "Number of heads",
)

tails_count = prometheus_client.Counter(
    "tails_count",
    "Number of tails",
)

flip_count = prometheus_client.Counter(
    "flip_count",
    "Number of flips",
)

# kpac_rating = prometheus_client.Gauge(
#     "kpac_rating",
#     "Current Danger Rating for KPAC",
# )


@app.get("/get-avalanche-forecasts")
async def get_avalance_forecasts():
    avalanche_api_response = get_avalanche_from_api()
    forecasts = filter_forecasts(avalanche_api_response)

    return {"forecasts": forecasts}


def get_demo():
    bray = "hello from demo"
    return bray


@app.get("/demo-get-call")
async def get_demo_call():
    # demo = get_demo()
    return get_demo()


def get_avalanche_from_api(
    url="https://api.avalanche.org/v2/public/products/map-layer",
):
    """Get the NAC api json response"""
    response = requests.get(url)
    api_resonse = response.json()
    return api_resonse


def filter_forecasts(api_response):
    """Get the forecast for all centers

    removes CAIC forecasts as they do not have a uniqe identifier
    removes any forecasts without an active rating
    returns dict{startdate, name, rating}
    """
    filtered_featuers = []

    # dictonary of responses that are being kept (my_name, NAC_name)
    feature_dict = {
        "start_date": "start_date",
        "end_date": "end_date",
        "name": "name",
        "rating": "danger_level",
    }

    for feature in api_response["features"]:
        filtered_feature = dict()
        for key, value in feature_dict.items():
            filtered_feature[key] = get_feature(feature, value)

        if not (
            (
                "CAIC" in filtered_feature["name"]
                or filtered_feature["rating"] == -1
            )
        ):
            # print(filtered_feature)
            filtered_featuers.append(filtered_feature)
    return filtered_featuers


def get_feature(feature, name):
    return feature["properties"][name]


def get_forecast(forecasts, name):
    """
    Get the forecast level for a given location from the forecasts.

    Args:
    - forecasts (list): List of forecast dictionaries.
    - location_name (str): Name of the location to find in the forecasts.

    Returns:
    - dict: Forecast dictionary the specified location, None if not found.
    """
    for forecast in forecasts:
        if forecast.get("name") == name:
            return forecast
    return None


@app.get("/flip-coins")
async def flip_coins(times=None):
    if times is None or not times.isdigit():
        raise HTTPException(
            status_code=400,
            detail="times must be set in reques and an integer",
        )
    times_as_int = int(times)

    heads = 0

    for _ in range(times_as_int):
        # this will be 0 or 1, if 1, it evaluates to True
        if random.randint(0, 1):
            heads += 1

    tails = times_as_int - heads

    heads_count.inc(heads)
    tails_count.inc(tails)
    flip_count.inc(times_as_int)

    return {
        "heads": heads,
        "tails": tails,
    }


@app.get("/metrics")
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest(),
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
