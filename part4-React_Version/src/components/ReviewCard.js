import React from 'react';

function generateStarRating(rating) {
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        stars += i <= rating ? '★' : '☆';
    }
    return stars;
}

function ReviewCard({ review }) {
    const reviewerName = review.user_name || review.user_id || 'Anonymous';
    return (
        <div className="review-card">
            <h4>{reviewerName}:</h4>
            <p>{review.text}</p>
            <p className="rating">Rating: <span>{generateStarRating(review.rating)}</span></p>
        </div>
    );
}

export default ReviewCard;