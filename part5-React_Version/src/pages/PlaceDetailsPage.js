import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getPlace, getPlaceReviews } from '../services/api';
import { useAuth } from '../context/AuthContext';
import ReviewCard from '../components/ReviewCard';
import ReviewForm from '../components/ReviewForm';
import Loading from '../components/Loading';

// Amenity icon mapping
const amenityIcons = {
    'wifi': '📶', 'wi-fi': '📶', 'internet': '📶',
    'pool': '🏊', 'swimming pool': '🏊',
    'parking': '🅿️',
    'kitchen': '🍳',
    'tv': '📺', 'television': '📺',
    'air conditioning': '❄️', 'ac': '❄️',
    'heating': '🔥',
    'washer': '🧺', 'washing machine': '🧺',
    'dryer': '🌀',
    'gym': '🏋️', 'fitness': '🏋️',
    'hot tub': '🛁', 'jacuzzi': '🛁',
    'fireplace': '🔥',
    'balcony': '🌅',
    'patio': '🪴',
    'garden': '🌳',
    'bbq': '🍖', 'grill': '🍖',
    'elevator': '🛗',
    'workspace': '💻', 'desk': '💻',
    'coffee': '☕',
    'breakfast': '🥐',
    'pets': '🐕',
    'smoking': '🚬',
    'security': '🔒',
    'default': '✓'
};

function PlaceDetailsPage() {
    const { placeId } = useParams();
    const { isAuthenticated } = useAuth();
    const [place, setPlace] = useState(null);
    const [reviews, setReviews] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    
    // Booking calculator state
    const [checkInDate, setCheckInDate] = useState('2024-01-15');
    const [checkOutDate, setCheckOutDate] = useState('2024-01-20');
    const [guests, setGuests] = useState(2);

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

    const getAmenityIcon = (amenityName) => {
        const name = amenityName.toLowerCase();
        for (const [key, icon] of Object.entries(amenityIcons)) {
            if (name.includes(key)) {
                return icon;
            }
        }
        return amenityIcons.default;
    };

    const calculateBooking = () => {
        if (!place) return { nights: 1, subtotal: 0, serviceFee: 0, total: 0 };
        
        const checkIn = new Date(checkInDate);
        const checkOut = new Date(checkOutDate);
        const nights = Math.max(1, Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24)));
        const subtotal = place.price * nights;
        const cleaningFee = 50;
        const serviceFee = Math.round(subtotal * 0.14);
        const total = subtotal + cleaningFee + serviceFee;
        
        return { nights, subtotal, cleaningFee, serviceFee, total };
    };

    const booking = calculateBooking();
    const avgRating = reviews.length > 0 
        ? (reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length).toFixed(1)
        : '5.0';

    if (isLoading) return <Loading message="Loading place details..." />;
    if (error) return (
        <div className="error-message" style={{textAlign: 'center', padding: '40px'}}>
            <h2>Error</h2>
            <p>{error}</p>
            <Link to="/" className="details-button">Back to Home</Link>
        </div>
    );
    if (!place) return null;

    const hostName = place.owner_name || place.owner_id || 'Host';
    const hostInitial = hostName.charAt(0).toUpperCase();

    return (
        <div>
            {/* Title Section */}
            <div className="place-title-section">
                <h1>{place.title}</h1>
                <div className="place-subtitle">
                    <span className="place-rating">
                        <span className="star-icon">★</span>
                        <span>{avgRating}</span>
                    </span>
                    <span>·</span>
                    <span>Superhost</span>
                    <span>·</span>
                    <span>{place.location || 'Great Location'}</span>
                </div>
            </div>

            {/* Image Gallery */}
            <div className="image-gallery">
                <div className="image-gallery-main">🏠</div>
                <div className="image-gallery-item">🏠</div>
                <div className="image-gallery-item">🏠</div>
                <div className="image-gallery-item">🏠</div>
                <div className="image-gallery-item">🏠</div>
            </div>

            {/* Main Content Wrapper (Two Columns) */}
            <div className="place-content-wrapper">
                {/* Left Column: Place Details */}
                <div className="place-main-content">
                    {/* Host Section */}
                    <section className="host-section">
                        <div className="host-header">
                            <div className="host-info">
                                <h2>Hosted by {hostName}</h2>
                                <p className="host-details">Superhost · Hosting since 2024</p>
                            </div>
                            <div className="host-avatar">{hostInitial}</div>
                        </div>
                    </section>

                    {/* Property Highlights */}
                    <section className="property-highlights">
                        <div className="highlight-item">
                            <div className="highlight-icon">🏡</div>
                            <div className="highlight-content">
                                <h3>Entire place</h3>
                                <p>You'll have the place to yourself</p>
                            </div>
                        </div>
                        <div className="highlight-item">
                            <div className="highlight-icon">✨</div>
                            <div className="highlight-content">
                                <h3>Enhanced Clean</h3>
                                <p>This host committed to enhanced cleaning process</p>
                            </div>
                        </div>
                        <div className="highlight-item">
                            <div className="highlight-icon">📍</div>
                            <div className="highlight-content">
                                <h3>Great location</h3>
                                <p>Recent guests gave the location a 5-star rating</p>
                            </div>
                        </div>
                    </section>

                    {/* Description Section */}
                    <section className="description-section">
                        <h2>About this place</h2>
                        <p className="description-text">
                            {place.description || 'Beautiful place to stay'}
                        </p>
                    </section>

                    {/* Amenities Section */}
                    <section className="amenities-section">
                        <h2>What this place offers</h2>
                        <div className="amenities-grid">
                            {place.amenities && place.amenities.length > 0 ? (
                                place.amenities.map((amenity, index) => {
                                    const name = typeof amenity === 'string' ? amenity : amenity.name;
                                    const icon = getAmenityIcon(name);
                                    return (
                                        <div key={index} className="amenity-item">
                                            <span className="amenity-icon">{icon}</span>
                                            <span>{name}</span>
                                        </div>
                                    );
                                })
                            ) : (
                                <p>No amenities listed</p>
                            )}
                        </div>
                    </section>
                </div>

                {/* Right Column: Booking Card */}
                <aside className="booking-card">
                    <div className="price-section">
                        <div className="price-line">
                            <span className="price">${place.price}</span>
                            <span className="price-period">night</span>
                        </div>
                        <div className="rating-info">
                            <span className="rating-stars">★</span>
                            <span>{avgRating}</span>
                            <span>·</span>
                            <span className="rating-count">{reviews.length} {reviews.length === 1 ? 'review' : 'reviews'}</span>
                        </div>
                    </div>

                    <div className="booking-dates">
                        <div className="date-input-group">
                            <div className="date-input">
                                <label>Check-in</label>
                                <input 
                                    type="date" 
                                    value={checkInDate} 
                                    onChange={(e) => setCheckInDate(e.target.value)}
                                />
                            </div>
                            <div className="date-input">
                                <label>Checkout</label>
                                <input 
                                    type="date" 
                                    value={checkOutDate} 
                                    onChange={(e) => setCheckOutDate(e.target.value)}
                                />
                            </div>
                        </div>
                        <div className="guests-input">
                            <label>Guests</label>
                            <select value={guests} onChange={(e) => setGuests(Number(e.target.value))}>
                                <option value="1">1 guest</option>
                                <option value="2">2 guests</option>
                                <option value="3">3 guests</option>
                                <option value="4">4 guests</option>
                                <option value="5">5 guests</option>
                                <option value="6">6 guests</option>
                            </select>
                        </div>
                    </div>

                    <button className="reserve-button" onClick={() => alert('Reservation feature coming soon!')}>
                        Reserve
                    </button>
                    <p className="booking-notice">You won't be charged yet</p>

                    <div className="price-breakdown">
                        <div className="price-row">
                            <span>${place.price} × {booking.nights} nights</span>
                            <span>${booking.subtotal}</span>
                        </div>
                        <div className="price-row">
                            <span>Cleaning fee</span>
                            <span>${booking.cleaningFee}</span>
                        </div>
                        <div className="price-row">
                            <span>Service fee</span>
                            <span>${booking.serviceFee}</span>
                        </div>
                        <div className="price-row total">
                            <span>Total</span>
                            <span>${booking.total}</span>
                        </div>
                    </div>
                </aside>
            </div>

            {/* Reviews Section */}
            <section className="reviews-section">
                <div className="reviews-header">
                    <h2>★ {avgRating} · {reviews.length} {reviews.length === 1 ? 'review' : 'reviews'}</h2>
                </div>
                {reviews.length > 0 ? (
                    <div className="reviews-grid">
                        {reviews.map(review => (
                            <ReviewCard key={review.id} review={review} />
                        ))}
                    </div>
                ) : (
                    <p className="no-reviews">No reviews yet. Be the first to review!</p>
                )}
            </section>

            {/* Add Review Form */}
            {isAuthenticated && (
                <div className="add-review">
                    <h2>Leave a review</h2>
                    <ReviewForm placeId={placeId} onReviewSubmitted={fetchReviews} />
                </div>
            )}
        </div>
    );
}

export default PlaceDetailsPage;