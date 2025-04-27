import { Route, Routes } from "react-router-dom";
import Content from "./components/Content";
import Navbar from "./components/Navbar";

export default function App() {
  return (
    <div className="min-h-screen bg-muted/50">
      <Navbar />
      <Routes>
        <Route path="/" element={<Content />} />
      </Routes>
    </div>
  );
}
