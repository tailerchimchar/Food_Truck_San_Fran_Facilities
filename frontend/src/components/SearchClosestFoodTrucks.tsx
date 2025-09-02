import {useState } from "react";
import type { FoodTruckInterface } from "./FoodTruck";

export default function SearchClosestFoodTrucksComponent({visible = false}) {
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");

  const [data, setData] = useState<FoodTruckInterface[]>([]);
  const serverURL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

  async function handleSearch() {
    try {
      const lat = parseFloat(latitude);
      const lon = parseFloat(longitude);
      const res = await fetch(`${serverURL}/api/getnearestfoodtrucks?latitude=${lat}&longitude=${lon}&limit=10`);
      if (res.status === 404) { 
        setData([]); 
        return; 
      }
      if (!res.ok) {
        throw new Error(String(res.status));
      }
      const responseData = await res.json();
      setData(responseData);
    } catch (e) {
      console.log("Error" + e);
      setData([]);
    }
  }

  return(
    <>
    <div className="m-t-10">
      <input
        type="number"
        value={latitude}
        onChange={(e) => setLatitude(e.target.value)}
        placeholder='Latitude from -90 to 90'
      />
      <input
        type="number"
        value={longitude}
        onChange={(e) => setLongitude(e.target.value)}
        placeholder='Longitude from -180 to 180'
      />
      <button onClick={handleSearch}> Search Closest Restaurants </button>
      <div className="mx-auto max-w-5xl pt-24 px-4">
      {visible && (
        <pre className="text-left whitespace-pre-wrap">
        {JSON.stringify(data, null, 2)}
      </pre> 
      )}
    </div>
    </div>
    </>
  )
}