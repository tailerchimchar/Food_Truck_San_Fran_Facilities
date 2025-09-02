from fastapi.responses import JSONResponse
import numpy as np
import json

class DataExplorer:
  def __init__(self, df, limit=1000):
    self._df_full = df
    self._df = df.head(limit)
    self._df_full["Applicant"] = self._df_full["Applicant"].fillna("")
    self._df_full["Status"] = self._df_full["Status"].fillna("")

  @property
  def df(self):
    return self._df
  
  def search_applicant(self, applicant, status):      
    if status:
      print(status)
      df = self._df_full.loc[
        (self._df_full["Applicant"] == applicant) & 
        (self._df_full["Status"].str.upper() == status.upper())]
    else:
      df = self._df_full.loc[(self._df_full["Applicant"] == applicant)]
      
    cols = ["locationid", "Applicant", "Status", "Address", "Latitude", "Longitude"]
    return df[cols].to_dict(orient="records")
  
  def search_street(self, address):     
    df = self._df_full.loc[self._df_full["Address"].str.contains(address, case=False, na=False)]
    cols = ["locationid", "Applicant", "Status", "Address", "Latitude", "Longitude"]

    return df[cols].to_dict(orient="records")
  
  def get_5_nearest_food_trucks(self, latitude, longitude, status: str= "APPROVED", limit: int=5):
    # distance formula = sqrt((x2-x1)^2 + (y2-y1)^2)
    #distance_from_address = sqrt(((self._df_full["Longitude"] - longitude) ** 2) + (self._df_full["Latitude"] - latitude)**2)
    df = self._df_full.loc[(self._df_full["Status"] == status.upper())]
    df["Latitude"] = df["Latitude"].round(6)
    df["Longitude"] = df["Longitude"].round(6)
    
    # drop coordinates where latitude or longitude == 0 
    df = df.loc[(df["Latitude"]  != 0) & (df["Longitude"] != 0)]
    
    dx = df["Longitude"] - float(longitude)
    dy = df["Latitude"] - float(latitude)
    
    df["Distance"] = np.sqrt(dx*dx + dy*dy)
    df = df.sort_values("Distance", ascending=True).head(limit) 
    
    cols = ["locationid", "Applicant", "Status", "Address", "Latitude", "Longitude", "Distance"]
    cols = [c for c in cols if c in df.columns]
    
    return df[cols].to_dict(orient="records")
  
  def json_response(self):
    json_data = self.df.to_json(orient="records")
    return JSONResponse(json.loads(json_data))