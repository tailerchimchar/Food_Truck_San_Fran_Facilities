from fastapi.testclient import TestClient
import pandas as pd
import pytest
from api import app

client = TestClient(app)

@pytest.fixture
def API_Manager():
  app.state.df = pd.read_csv("data/Testing_Food_Data.csv")
  yield
  del app.state.df
  
def test_canary(API_Manager):
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {"message": "Hello World"}
  
def test_health_check(API_Manager):
  response = client.get("/health")
  assert response.status_code == 200
  assert response.json() == { "status": "healthy"}
  
def test_search_applicant(API_Manager):
  response = client.get("/api/searchapplicant", params={"applicant": "The Geez Freeze"})
  data = response.json()[0]
  assert response.status_code == 200
  assert data["Applicant"] == "The Geez Freeze"
  assert data["Status"] == "APPROVED"
  assert data["Address"] == "3750 18TH ST"
  
def test_search_applicant_not_there(API_Manager):
  response = client.get("/api/searchapplicant", params={"applicant": "testing not there"})
  assert response.status_code == 404
  assert response.json() == {
  "detail": "Applicant not found"
}

def test_search_street_full_name(API_Manager):
  response = client.get("/api/searchstreet", params={"address": "3750 18TH ST"})
  data = response.json()[0] 
  assert response.status_code == 200
  assert data["Address"] == "3750 18TH ST"
  assert data["Status"] == "APPROVED"
  assert data["Applicant"] == "The Geez Freeze"

@pytest.mark.parametrize("index, expected",[
  (0, "3750 18TH ST"),
  (1, "2535 TAYLOR ST"),
  (2, "217 SANSOME ST"),
])
def test_search_street_half_name(API_Manager, index, expected):
  response = client.get("/api/searchstreet", params={"address": "ST"})
  data = response.json()
  assert response.status_code == 200
  assert data[index]["Address"] == expected
  
def test_get_closest_food_trucks(API_Manager):
  response = client.get("/api/getnearestfoodtrucks", params={"latitude": 37.805885350100986, "longitude": -122.41594524663745, "limit": 2})
  data = response.json()
  assert response.status_code == 200
  assert len(data) == 2
  assert data[0]["Applicant"] == "Datam SF LLC dba Anzu To You"
  assert data[1]["Applicant"] == "Truly Food & More"
  
def test_get_closest_food_trucks_latitude_errors(API_Manager):
  response = client.get("/api/getnearestfoodtrucks", params={"latitude": 91, "longitude": 91, "limit": 2})
  assert response.status_code == 400
  assert response.json() == {
  "detail": "Latitude must be between -90 and 90."
}

def test_get_closest_food_trucks_limit_errors(API_Manager):
  response = client.get("/api/getnearestfoodtrucks", params={"latitude": 37, "longitude": 122, "limit": -1})
  assert response.status_code == 400
  assert response.json() == {
  "detail": "Limit must be greater than 0."
}