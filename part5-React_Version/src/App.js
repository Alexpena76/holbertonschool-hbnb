import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import PlaceDetailsPage from './pages/PlaceDetailsPage';
import AddReviewPage from './pages/AddReviewPage';
import LoginPage from './pages/LoginPage';
import Header from './components/Header';
import Footer from './components/Footer';

function App() {
    return (
        <div className="app">
            <Header />
            <main>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/place/:placeId" element={<PlaceDetailsPage />} />
                    <Route path="/add_review/:placeId" element={<AddReviewPage />} />
                    <Route path="/login" element={<LoginPage />} />
                </Routes>
            </main>
            <Footer />
        </div>
    );
}

export default App;