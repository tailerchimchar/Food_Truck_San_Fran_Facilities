from typing import Optional
from fastapi import FastAPI, HTTPException, Query
import pandas as pd
from data_processing import DataExplorer
from fastapi.middleware.cors import CORSMiddleware

#  reads it only one time
# make sure tha the session is injected into the endpoint instead of being created directly into the endpoint
# dependency that gets us the end point 
async def lifespan(app: FastAPI):
  app.state.df = pd.read_csv("data/Mobile_Food_Facility_Permit.csv")
  yield
  del app.state.df
  
app = FastAPI(lifespan=lifespan)

origins = [
  "http://localhost:5173"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# api.py
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
  
@app.get("/api/")
async def read_csv(limit: int = Query(500, gt=0, lt=10000)):
  data = DataExplorer(app.state.df, limit)
  return data.json_response()

@app.get("/api/searchapplicant")
async def search_by_applicant(applicant: str, status: str = None):
  data = DataExplorer(app.state.df)
  results = data.search_applicant(applicant, status)

  if not results:
    raise HTTPException(status_code=404, detail="Applicant not found")
  
  return results

@app.get("/api/searchstreet")
async def search_by_street(address: str):
  data = DataExplorer(app.state.df)
  results = data.search_street(address)

  if not results:
    raise HTTPException(status_code=404, detail="Street not found")
  
  return results

@app.get("/api/getnearestfoodtrucks")
async def get_nearest_food_trucks(latitude: float, longitude: float, limit: int = 5, status: str = "APPROVED"):
  if abs(latitude) > 90:
    raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90.")
  if abs(longitude) > 180:
      raise HTTPException(status_code=400, detail="Longitude must be between -90 and 90.")
  if limit <= 0:
    raise HTTPException(status_code=400, detail="Limit must be greater than 0.")

  data = DataExplorer(app.state.df)
  return data.get_5_nearest_food_trucks(latitude, longitude, status=status, limit=limit)

