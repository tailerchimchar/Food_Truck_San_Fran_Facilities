import { useEffect, useState } from "react";

export interface FoodTruckInterface {
  locationid: number;
  Applicant: string;
  Status: string;
  Address: string;
  Latitude: number;
  Longitude: number;
}

export default function FoodTruck() {
  const [data, setData] = useState<FoodTruckInterface[]>([]);
  const serverURL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

  useEffect(() => {
    (async () => {
      try {
        const response = await fetch(`${serverURL}/api/?limit=50`);
        if (!response.ok){
          throw new Error(`Couldn't fetch data because: ${response.status}`); 
        } 
        const responseData = await response.json();
        setData(responseData);
      }
      catch(e){
        console.log("Error" + e);
      }
    })();
  }, []);


  return(
    <>
        <div className="mx-auto max-w-5xl pt-24 px-4">
      <pre className="text-left whitespace-pre-wrap">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
    </>
  )
}