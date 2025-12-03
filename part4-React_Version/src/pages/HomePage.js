import React, { useState, useEffect, useMemo } from 'react';
import { getPlaces } from '../services/api';
import PlaceCard from '../components/PlaceCard';
import PriceFilter from '../components/PriceFilter';
import Loading from '../components/Loading';

function HomePage() {
    const [places, setPlaces] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [priceFilter, setPriceFilter] = useState('all');

    useEffect(() => {
        const fetchPlaces = async () => {
            try {
                const data = await getPlaces();
                setPlaces(data);
            } catch (err) {
                setError('Unable to load places.');
            } finally {
                setIsLoading(false);
            }
        };
        fetchPlaces();
    }, []);

    const filteredPlaces = useMemo(() => {
        if (priceFilter === 'all') return places;
        return places.filter(place => place.price <= parseFloat(priceFilter));
    }, [places, priceFilter]);

    if (isLoading) return <Loading message="Loading places..." />;
    if (error) return <div className="error-message">{error}</div>;

    return (
        <div>
            <h1>Available Places</h1>
            <PriceFilter value={priceFilter} onChange={setPriceFilter} />
            <section className="places-grid">
                {filteredPlaces.length > 0 ? (
                    filteredPlaces.map(place => <PlaceCard key={place.id} place={place} />)
                ) : (
                    <p className="no-places">No places found.</p>
                )}
            </section>
        </div>
    );
}

export default HomePage;