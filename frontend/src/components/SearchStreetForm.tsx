import {useState } from "react";
import type { FoodTruckInterface } from "./FoodTruck";

export default function SearchStreetComponent({visible = false}) {
  const [addressName, setAddressName] = useState("");
  const [data, setData] = useState<FoodTruckInterface[]>([]);
  const serverURL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

  async function handleSearch() {
    try {
      const res = await fetch(`${serverURL}/api/searchstreet?address=${addressName}`);
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
        type="text"
        value={addressName}
        onChange={(e) => setAddressName(e.target.value)}
        placeholder='Search for specific street'
      />
      <button onClick={handleSearch}> Search Street </button>
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