import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Request, HTTPException, status


import os

router = APIRouter()

load_dotenv()

api_key = os.getenv("LOCATION_IQ_API_KEY")

ACCEPTED_TAGS = [
    "all",
    "airport",
    "restaurant",
    "bank",
    "atm",
    "hotel",
    "pub",
    "bus_station",
    "railway_station",
    "cinema",
    "hospital",
    "college",
    "school",
    "pharmacy",
    "supermarket",
    "fuel",
    "gym",
    "place_of_worship",
    "toilet",
    "park",
    "stadium",
    "parking",
    "cardealer",
]


def activities(lat: float, lon: float, tag: str, radius: int):
    url = "https://us1.locationiq.com/v1/nearby"

    data = {
        "key": api_key,
        "lat": lat,
        "lon": lon,
        "tag": tag,
        "radius": radius,
        "format": "json",
    }
    try:
        response = requests.get(url, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise requests.exceptions.RequestException(
                "Error: Unexpected response {}".format(response.status_code)
            )
    except requests.exceptions.RequestException as e:
        return {"error": e}


@router.post("/activities")
async def get_activities(request: Request):
    req_body = await request.json()
    lat = req_body.get("lat")
    lon = req_body.get("lon")
    tag = req_body.get("tag")
    radius = req_body.get("radius")

    if tag not in ACCEPTED_TAGS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid tag",
        )

    if not lat or not lon or not tag or not radius:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing query parameters",
        )
    try:
        result = activities(lat, lon, tag, radius)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching data",
        )

    return result
