import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getPlace, createReview } from '../services/api';
import { useAuth } from '../context/AuthContext';
import Loading from '../components/Loading';

function AddReviewPage() {
    const { placeId } = useParams();
    const navigate = useNavigate();
    const { isAuthenticated, isLoading: authLoading } = useAuth();
    const [place, setPlace] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [reviewText, setReviewText] = useState('');
    const [rating, setRating] = useState('1');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    useEffect(() => {
        if (!authLoading && !isAuthenticated) {
            navigate('/');
        }
    }, [isAuthenticated, authLoading, navigate]);

    useEffect(() => {
        const fetchPlace = async () => {
            if (!placeId || !isAuthenticated) return;
            try {
                const data = await getPlace(placeId);
                setPlace(data);
                document.title = `Add Review - ${data.title} - HBnB`;
            } catch (err) {
                setError('Unable to load place.');
            } finally {
                setIsLoading(false);
            }
        };
        fetchPlace();
    }, [placeId, isAuthenticated]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        if (!reviewText.trim()) {
            setError('Please enter your review');
            return;
        }
        setIsSubmitting(true);
        try {
            await createReview(placeId, reviewText.trim(), parseInt(rating));
            setSuccess('Review submitted! Redirecting...');
            setTimeout(() => navigate(`/place/${placeId}`), 2000);
        } catch (err) {
            setError(err.message || 'Failed to submit review');
        } finally {
            setIsSubmitting(false);
        }
    };

    if (authLoading || isLoading) return <Loading />;
    if (!isAuthenticated) return null;

    return (
        <div>
            <h1>Reviewing: {place?.title || 'Unknown Place'}</h1>
            <div className="add-review">
                <h2>Add a Review</h2>
                {error && <div className="error-message">{error}</div>}
                {success && <div className="success-message">{success}</div>}
                <form className="review-form" onSubmit={handleSubmit}>
                    <label htmlFor="review-text">Your Review:</label>
                    <textarea
                        id="review-text"
                        value={reviewText}
                        onChange={(e) => setReviewText(e.target.value)}
                        placeholder="Share your experience..."
                        required
                        disabled={isSubmitting}
                    />
                    <label htmlFor="rating">Rating:</label>
                    <select id="rating" value={rating} onChange={(e) => setRating(e.target.value)} disabled={isSubmitting}>
                        <option value="1">1 Star</option>
                        <option value="2">2 Stars</option>
                        <option value="3">3 Stars</option>
                        <option value="4">4 Stars</option>
                        <option value="5">5 Stars</option>
                    </select>
                    <button type="submit" disabled={isSubmitting}>
                        {isSubmitting ? 'Submitting...' : 'Submit Review'}
                    </button>
                </form>
            </div>
        </div>
    );
}

export default AddReviewPage;