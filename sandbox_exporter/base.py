"""
sandbox_exporter base module.

This module creates a coin flip API.
It serves port
Start it by
Run it by

"""
import random

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/flip-coins")
async def flip_coins(times=None):
    if times is None or not times.isdigit():
        raise HTTPException(
            status_code = 400,
            detail="times must be set in reques and an integer",
        )
    times_as_int = int(times)

    heads = 0

    for _ in range(times_as_int):
        # this will be 0 or 1, if 1, it evaluates to True
        if random.randint(0,1):
            heads += 1

    tails = times_as_int - heads

    return {
        "heads": heads,
        "tails": tails,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
