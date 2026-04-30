import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "sonner";
import "@/App.css";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Optimizer from "./pages/Optimizer";
import Drivers from "./pages/Drivers";
import AIAssistant from "./pages/AIAssistant";
import RestorePoints from "./pages/RestorePoints";
import Scheduler from "./pages/Scheduler";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/optimize" element={<Optimizer />} />
            <Route path="/drivers" element={<Drivers />} />
            <Route path="/ai" element={<AIAssistant />} />
            <Route path="/scheduler" element={<Scheduler />} />
            <Route path="/restore" element={<RestorePoints />} />
          </Routes>
        </Layout>
        <Toaster
          theme="dark"
          position="bottom-right"
          toastOptions={{
            style: {
              background: "#121212",
              border: "1px solid #27272A",
              borderRadius: 0,
              color: "#FFFFFF",
              fontFamily: "IBM Plex Mono, monospace",
              fontSize: "12px",
            },
          }}
        />
      </BrowserRouter>
    </div>
  );
}

export default App;
