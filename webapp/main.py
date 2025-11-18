import os
import base64
from typing import Union
from os.path import dirname, abspath, join
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")


class Body(BaseModel):
    length: Union[int, None] = 20


class CountryRequest(BaseModel):
    country: str


@app.get('/')
def root():
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)


@app.post('/generate')
def generate(body: Body):
    """
    Generate a pseudo-random token ID of twenty characters by default. Example POST request body:

    {
        "length": 20
    }
    """
    string = base64.b64encode(os.urandom(64))[:body.length].decode('utf-8')
    return {'token': string}


@app.post('/cities')
def get_cities(request: CountryRequest):
    """
    Get cities for a given country. Example POST request body:

    {
        "country": "France"
    }
    """
    # Sample data - in a real application, this would come from a database
    cities_data = {
        "France": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"],
        "Germany": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne"],
        "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao"],
        "Italy": ["Rome", "Milan", "Naples", "Turin", "Florence"],
        "USA": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
        "Japan": ["Tokyo", "Osaka", "Yokohama", "Nagoya", "Sapporo"],
        "UK": ["London", "Birmingham", "Manchester", "Leeds", "Glasgow"],
    }
    
    country = request.country
    cities = cities_data.get(country, [])
    
    if not cities:
        return {
            'country': country,
            'cities': [],
            'message': f'No cities found for {country}'
        }
    
    return {
        'country': country,
        'cities': cities
    }

