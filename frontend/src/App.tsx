import './App.css';
import Header from './components/Header';
import FoodTruck from './components/FoodTruck';
import { useState } from 'react';
import SearchApplicantComponent from './components/SearchApplicantForm';
import SearchStreetComponent from './components/SearchStreetForm';
import SearchClosestFoodTrucksComponent from './components/SearchClosestFoodTrucks';

const App = () => {
  const [showAllFoodTrucks, setShowAllFoodTrucks] = useState(false); 
  const [showApplicant, setShowApplicant] = useState(false); 
  const [showStreets, setShowStreets] = useState(false); 
  const [showClosestFoodTrucks, setShowClosestFoodTrucks] = useState(false); 

  const toggleVisibilityFoodTrucks = () => {
    setShowAllFoodTrucks(!showAllFoodTrucks); 
  };

  return (
    <>
    <div className="App">
      <header className="App-header">
        < Header />
         <main className="pt-16"> 
          <div>
            <p> Tip: Press "Search Applicant" after populating the input. Then press "Show Applicant Results" to show the results. You can press "Show Applicant Results" again to hide the information.</p>
            <h3> Search for applicant here</h3>
            <SearchApplicantComponent visible = {showApplicant}/>
              <button onClick={() => setShowApplicant(s => !s)}>
                Show Applicant Results
              </button>


            <h3> Search for street/address here</h3>
            <SearchStreetComponent visible = {showStreets}/>
              <button onClick={() => setShowStreets(s => !s)}>
                Show Street Results
              </button>
              

            <h3> Search for 10 closest restaurants to this position</h3>
            <SearchClosestFoodTrucksComponent visible={showClosestFoodTrucks}/>
            <button onClick={() => setShowClosestFoodTrucks(s => !s)}>
              Show Closest San Francisco Food Trucks
            </button>

            <h3> Click to see the full dataset</h3>
            <button onClick={toggleVisibilityFoodTrucks}>
              Show All San Francisco Food Trucks
            </button>

          </div>
          <p></p>

          <div className = "mt-12">
            {showAllFoodTrucks && <FoodTruck />}
          </div>
       </main>
      </header>
    </div>
    </>
  );
};

export default App;