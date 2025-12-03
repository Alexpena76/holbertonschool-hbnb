import React, { useState } from 'react';
import { createReview } from '../services/api';

function ReviewForm({ placeId, onReviewSubmitted }) {
    const [reviewText, setReviewText] = useState('');
    const [rating, setRating] = useState('1');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccess(null);

        if (!reviewText.trim()) {
            setError('Please enter your review');
            return;
        }

        setIsSubmitting(true);
        try {
            await createReview(placeId, reviewText.trim(), parseInt(rating));
            setSuccess('Review submitted!');
            setReviewText('');
            setRating('1');
            if (onReviewSubmitted) onReviewSubmitted();
            setTimeout(() => setSuccess(null), 3000);
        } catch (err) {
            setError(err.message || 'Failed to submit review');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
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
    );
}

export default ReviewForm;