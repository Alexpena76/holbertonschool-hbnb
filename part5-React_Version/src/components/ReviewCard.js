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
    const initial = reviewerName.charAt(0).toUpperCase();
    
    return (
        <div className="review-card">
            <div className="review-header">
                <div className="reviewer-avatar">{initial}</div>
                <div className="reviewer-info">
                    <h4>{reviewerName}</h4>
                    <p className="review-date">December 2024</p>
                </div>
            </div>
            <p className="review-content">{review.text}</p>
            <div className="review-rating">
                <span className="rating-stars">{generateStarRating(review.rating)}</span>
            </div>
        </div>
    );
}

export default ReviewCard;