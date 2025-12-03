import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getPlace, getPlaceReviews } from '../services/api';
import { useAuth } from '../context/AuthContext';
import ReviewCard from '../components/ReviewCard';
import ReviewForm from '../components/ReviewForm';
import Loading from '../components/Loading';

function PlaceDetailsPage() {
    const { placeId } = useParams();
    const { isAuthenticated } = useAuth();
    const [place, setPlace] = useState(null);
    const [reviews, setReviews] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchReviews = useCallback(async () => {
        try {
            const data = await getPlaceReviews(placeId);
            setReviews(data);
        } catch (err) {
            setReviews([]);
        }
    }, [placeId]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const placeData = await getPlace(placeId);
                setPlace(placeData);
                document.title = `${placeData.title} - HBnB`;
                await fetchReviews();
            } catch (err) {
                setError(err.message || 'Unable to load place.');
            } finally {
                setIsLoading(false);
            }
        };
        fetchData();
    }, [placeId, fetchReviews]);

    const getAmenities = (place) => {
        if (!place.amenities || place.amenities.length === 0) return 'None';
        return place.amenities.map(a => typeof a === 'string' ? a : a.name).join(', ');
    };

    if (isLoading) return <Loading message="Loading place details..." />;
    if (error) return (
        <div className="error-message" style={{textAlign: 'center', padding: '40px'}}>
            <h2>Error</h2>
            <p>{error}</p>
            <Link to="/" className="details-button">Back to Home</Link>
        </div>
    );
    if (!place) return null;

    return (
        <div>
            <section>
                <h1>{place.title}</h1>
                <div className="place-details">
                    <div className="place-info">
                        <p><strong>Host:</strong> {place.owner_name || place.owner_id || 'Unknown'}</p>
                        <p><strong>Price per night:</strong> ${place.price}</p>
                        <p><strong>Description:</strong> {place.description || 'No description'}</p>
                        <p><strong>Amenities:</strong> {getAmenities(place)}</p>
                    </div>
                </div>
            </section>

            <section className="reviews-section">
                <h2>Reviews</h2>
                {reviews.length > 0 ? (
                    reviews.map(review => <ReviewCard key={review.id} review={review} />)
                ) : (
                    <p className="no-reviews">No reviews yet. Be the first!</p>
                )}
            </section>

            {isAuthenticated && <ReviewForm placeId={placeId} onReviewSubmitted={fetchReviews} />}
        </div>
    );
}

export default PlaceDetailsPage;