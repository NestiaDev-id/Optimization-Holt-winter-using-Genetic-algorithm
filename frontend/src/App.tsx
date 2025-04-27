import { useState } from "react";
import { Route, Routes } from "react-router-dom";

function App() {
  const [count, setCount] = useState(0);

  return (
    <Routes>
      <Route
        path="/"
        element={
          <div className="App">
            <h1>Welcome to the App</h1>
            <button onClick={() => setCount(count + 1)}>
              Count is {count}
            </button>
          </div>
        }
      />
      <Route path="/about" element={<div>About Page</div>} />
      <Route path="/contact" element={<div>Contact Page</div>} />
    </Routes>
  );
}

export default App;
