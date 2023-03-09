from seatgeekpkg import seatgeekpkg
import pytest
import json
import pandas as pd
import requests


import dotenv
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()

client_key = os.getenv("CLIENT_KEY")

def test_performer_int():
    with pytest.raises(AssertionError):
        example = 8471640
        artist = 'sza'
        expected = '669560'
        actual = seatgeekpkg.performer_id(example, artist)
        assert actual == expected


def test_city_abbre():
    city = 'LA'
    expected = 200
    actual = seatgeekpkg.city_status(client_key, city)
    assert actual == expected


def test_city_status():
    with pytest.raises(AssertionError):
        example = 8264639
        city = 'Los Angeles'
        expected = 200
        actual = seatgeekpkg.city_status(example, city)
        assert actual == expected