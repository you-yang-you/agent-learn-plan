import requests

CITY_COORDS = {
    "北京": {"lat": 39.9, "lon": 116.4},
    "上海": {"lat": 31.2, "lon": 121.5},
    "广州": {"lat": 23.1, "lon": 113.3},
}

def get_weather(city_name: str) -> dict:
    if city_name not in CITY_COORDS:
        raise ValueError(f"暂不支持该城市: {city_name}")

    coords = CITY_COORDS[city_name]
    r = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "current_weather": True,
        },
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["current_weather"]

# 北京
w = get_weather("北京")
print(f"北京当前温度: {w['temperature']}°C, 风速: {w['windspeed']} km/h")

import asyncio, httpx, time

def fetch_sync(i: int):
    r = requests.get(f"https://httpbin.org/get?i={i}", timeout=10)
    return r.status_code

async def fetch_one(client: httpx.AsyncClient, i: int):
    r = await client.get(f"https://httpbin.org/get?i={i}")
    return r.status_code

start = time.perf_counter()
sync_codes = [fetch_sync(i) for i in range(5)]
sync_elapsed = time.perf_counter() - start
print("5 个同步请求耗时: %.2fs" % sync_elapsed)
print("同步状态码:", sync_codes)

async def main():
    async with httpx.AsyncClient(timeout=10) as client:
        t0 = time.perf_counter()
        codes = await asyncio.gather(
            *[fetch_one(client, i) for i in range(5)]
        )
        elapsed = time.perf_counter() - t0
    print("5 个并发请求异步耗时: %.2fs" % elapsed)
    print("异步状态码:", codes)

asyncio.run(main())