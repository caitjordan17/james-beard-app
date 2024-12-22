import React, { useEffect, useState } from 'react'

function App() {
  const [restaurants, setRestaurants] = useState([])

  useEffect(() => {
    fetch('http://localhost:5555/api/awards')
      .then((response) => response.json())
      .then((data) => setRestaurants(data))
  }, [])

  console.log(restaurants)
  return (
    <div className="App">
      <h1>Awards</h1>
      <ul>
        {restaurants.map((item) => (
          <li key={item.id}>
            {item.restaurant} - {item.year}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
