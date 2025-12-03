import React from 'react';
import { Link } from 'react-router-dom';

function PlaceCard({ place }) {
    return (
        <div className="place-card">
            <h3>{place.title}</h3>
            <p className="price">Price per night: ${place.price}</p>
            <Link to={`/place/${place.id}`} className="details-button">View Details</Link>
        </div>
    );
}

export default PlaceCard;