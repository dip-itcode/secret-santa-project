import React from "react";
import { BrowserRouter as Router, Routes, Route, NavLink } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import GeneratePage from "./pages/GeneratePage";
import HistoryPage from "./pages/HistoryPage";
import "./styles/App.css";

export default function App() {
  return (
    <Router>
      <Toaster position="top-right" />
      <div className="app">
        <header className="header">
          <div className="header-inner">
            <div className="logo">🎅 Secret Santa</div>
            <nav className="nav">
              <NavLink to="/" end className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
                Generate
              </NavLink>
              <NavLink to="/history" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
                History
              </NavLink>
            </nav>
          </div>
        </header>

        <main className="main">
          <Routes>
            <Route path="/" element={<GeneratePage />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </main>

        <footer className="footer">
          <p>© {new Date().getFullYear()} Acme Corp — Secret Santa System</p>
        </footer>
      </div>
    </Router>
  );
}
