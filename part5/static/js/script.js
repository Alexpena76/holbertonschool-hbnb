/**
 * HBnB Application - Complete Enhanced JavaScript with Airbnb-Style Features
 * Handles authentication, places display, filtering, place details, reviews, and booking
 */

// =============================================================================
// API CONFIGURATION
// =============================================================================

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

let allPlaces = [];
let authToken = null;
let currentPlace = null;

// =============================================================================
// AMENITY ICON MAPPING
// =============================================================================
const amenityIcons = {
    'wifi': '📶',
    'wi-fi': '📶',
    'internet': '📶',
    'pool': '🏊',
    'swimming pool': '🏊',
    'parking': '🅿️',
    'kitchen': '🍳',
    'tv': '📺',
    'television': '📺',
    'air conditioning': '❄️',
    'ac': '❄️',
    'heating': '🔥',
    'washer': '🧺',
    'washing machine': '🧺',
    'dryer': '🌀',
    'gym': '🏋️',
    'fitness': '🏋️',
    'hot tub': '🛁',
    'jacuzzi': '🛁',
    'fireplace': '🔥',
    'balcony': '🌅',
    'patio': '🪴',
    'garden': '🌳',
    'bbq': '🍖',
    'grill': '🍖',
    'elevator': '🛗',
    'workspace': '💻',
    'desk': '💻',
    'coffee': '☕',
    'breakfast': '🥐',
    'pets': '🐕',
    'smoking': '🚬',
    'security': '🔒',
    'default': '✓'
};

// =============================================================================
// DOM CONTENT LOADED - MAIN ENTRY POINT
// =============================================================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded, initializing application...');
    
    // Check if we're on the login page
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        console.log('Login page detected, setting up login form...');
        setupLoginForm(loginForm);
    }
    
    // Check if we're on the index page
    const placesList = document.getElementById('places-list');
    if (placesList) {
        console.log('Index page detected, initializing places list...');
        checkAuthentication();
        setupPriceFilter();
    }
    
    // Check if we're on the place details page
    const placeDetails = document.getElementById('place-title-section') || document.getElementById('place-details');
    if (placeDetails) {
        console.log('Place details page detected, initializing...');
        initPlaceDetailsPage();
    }
    
    // Check if we're on the add review page
    const reviewForm = document.getElementById('review-form');
    const pageTitle = document.getElementById('page-title');
    if (reviewForm && !placeDetails && pageTitle) {
        console.log('Add review page detected, initializing...');
        initAddReviewPage();
    }
    
    console.log('Application initialization complete.');
});

// =============================================================================
// ADD REVIEW PAGE FUNCTIONS
// =============================================================================

function initAddReviewPage() {
    console.log('Initializing add review page...');
    authToken = checkAuthenticationRequired();
    
    if (!authToken) {
        return;
    }
    
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        console.error('No place ID found in URL');
        showAddReviewError('No place ID provided. Please select a place to review.');
        return;
    }
    
    console.log('Place ID for review:', placeId);
    fetchPlaceNameForReview(placeId);
    setupAddReviewForm(placeId);
}

function checkAuthenticationRequired() {
    console.log('Checking if user is authenticated (required)...');
    const token = getCookie('token');
    
    if (!token) {
        console.log('User not authenticated, redirecting to index...');
        window.location.href = '/';
        return null;
    }
    
    console.log('User is authenticated');
    return token;
}

async function fetchPlaceNameForReview(placeId) {
    console.log('Fetching place name for review page...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const place = await response.json();
            console.log('Place data received:', place);
            
            const pageTitle = document.getElementById('page-title');
            if (pageTitle) {
                pageTitle.textContent = `Reviewing: ${place.title}`;
            }
            
            document.title = `Add Review - ${place.title} - HBnB`;
        } else {
            console.error('Failed to fetch place:', response.status);
        }
    } catch (error) {
        console.error('Error fetching place name:', error);
    }
}

function setupAddReviewForm(placeId) {
    console.log('Setting up add review form...');
    
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) {
        console.error('Review form not found');
        return;
    }
    
    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        console.log('Review form submitted');
        
        const reviewText = document.getElementById('review-text').value.trim();
        const rating = document.getElementById('rating').value;
        
        if (!reviewText) {
            showAddReviewError('Please enter your review text');
            return;
        }
        
        if (!rating) {
            showAddReviewError('Please select a rating');
            return;
        }
        
        console.log('Review data:', { placeId, reviewText, rating });
        
        const submitButton = reviewForm.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Submitting...';
        submitButton.disabled = true;
        
        try {
            await submitReviewFromForm(placeId, reviewText, parseInt(rating));
        } finally {
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        }
    });
    
    console.log('Add review form setup complete');
}

async function submitReviewFromForm(placeId, text, rating) {
    console.log('Submitting review from form...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                place_id: placeId,
                text: text,
                rating: rating
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            console.log('Review submitted successfully:', data);
            showAddReviewSuccess('Review submitted successfully!');
            
            document.getElementById('review-text').value = '';
            document.getElementById('rating').value = '1';
            
            setTimeout(() => {
                window.location.href = `/place/${placeId}`;
            }, 2000);
            
        } else {
            console.error('Failed to submit review:', data);
            showAddReviewError(data.error || 'Failed to submit review. Please try again.');
        }
        
    } catch (error) {
        console.error('Error submitting review:', error);
        showAddReviewError('Unable to submit review. Please check your connection and try again.');
    }
}

function showAddReviewError(message) {
    showFormMessage(message, 'error');
}

function showAddReviewSuccess(message) {
    showFormMessage(message, 'success');
}

function showFormMessage(message, type) {
    console.log(`Showing ${type} message:`, message);
    
    const existingMessage = document.querySelector('.form-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `form-message ${type}-message`;
    messageDiv.textContent = message;
    
    if (type === 'error') {
        messageDiv.style.cssText = `
            background-color: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid #fcc;
            font-weight: 500;
        `;
    } else {
        messageDiv.style.cssText = `
            background-color: #efe;
            color: #2a7;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid #cfc;
            font-weight: 500;
        `;
    }
    
    const addReviewDiv = document.querySelector('.add-review');
    const form = document.getElementById('review-form');
    
    if (addReviewDiv && form) {
        addReviewDiv.insertBefore(messageDiv, form);
    }
    
    if (type === 'error') {
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }
}

// =============================================================================
// PLACE DETAILS PAGE FUNCTIONS
// =============================================================================

function initPlaceDetailsPage() {
    console.log('Initializing place details page...');
    
    const placeId = getPlaceIdFromURL();
    
    if (!placeId) {
        console.error('No place ID found in URL');
        showPlaceDetailsError('No place ID provided in URL');
        return;
    }
    
    console.log('Place ID from URL:', placeId);
    
    authToken = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');
    
    if (!authToken) {
        console.log('User not authenticated - showing login link, hiding review form');
        
        if (loginLink) {
            loginLink.style.display = 'block';
        }
        if (addReviewSection) {
            addReviewSection.style.display = 'none';
        }
    } else {
        console.log('User authenticated - hiding login link, showing review form');
        
        if (loginLink) {
            loginLink.style.display = 'none';
        }
        if (addReviewSection) {
            addReviewSection.style.display = 'block';
        }
        
        setupReviewForm(placeId);
    }
    
    fetchPlaceDetails(authToken, placeId);
    setupBookingCalculations();
}

function getPlaceIdFromURL() {
    console.log('Extracting place ID from URL...');
    console.log('Current URL:', window.location.href);
    console.log('Pathname:', window.location.pathname);
    console.log('Search:', window.location.search);
    
    const urlParams = new URLSearchParams(window.location.search);
    let placeId = urlParams.get('id') || urlParams.get('place_id');
    
    if (placeId) {
        console.log('Place ID found in query parameters:', placeId);
        return placeId;
    }
    
    const pathParts = window.location.pathname.split('/');
    console.log('Path parts:', pathParts);
    
    for (let i = 0; i < pathParts.length; i++) {
        if ((pathParts[i] === 'place' || pathParts[i] === 'add_review') && pathParts[i + 1]) {
            placeId = pathParts[i + 1];
            console.log('Place ID found in path:', placeId);
            return placeId;
        }
    }
    
    console.log('No place ID found in URL');
    return null;
}

async function fetchPlaceDetails(token, placeId) {
    console.log('Fetching place details for:', placeId);
    
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const placeResponse = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });
        
        if (!placeResponse.ok) {
            if (placeResponse.status === 404) {
                throw new Error('Place not found');
            }
            throw new Error(`HTTP error! status: ${placeResponse.status}`);
        }
        
        const place = await placeResponse.json();
        console.log('Place details fetched successfully:', place);
        
        currentPlace = place;
        displayPlaceDetails(place);
        fetchPlaceReviews(placeId);
        updateBookingCard(place);
        
    } catch (error) {
        console.error('Error fetching place details:', error);
        showPlaceDetailsError(error.message || 'Unable to load place details. Please try again later.');
    }
}

function displayPlaceDetails(place) {
    console.log('Displaying place details...');
    
    // Check if we have the enhanced layout
    const titleSection = document.getElementById('place-title-section');
    
    if (titleSection) {
        // Enhanced Airbnb-style layout
        displayEnhancedPlace(place);
    } else {
        // Original layout
        displayOriginalPlace(place);
    }
}

function displayEnhancedPlace(place) {
    console.log('Using enhanced Airbnb-style layout');
    
    // Update page title in browser tab
    document.title = `${place.title} - HBnB`;
    
    // Update title section
    const titleSection = document.getElementById('place-title-section');
    titleSection.innerHTML = `
        <h1>${escapeHtml(place.title)}</h1>
        <div class="place-subtitle">
            <span class="place-rating">
                <span class="star-icon">★</span>
                <span>5.0</span>
            </span>
            <span>·</span>
            <span>Superhost</span>
            <span>·</span>
            <span>${escapeHtml(place.location || 'Great Location')}</span>
        </div>
    `;
    
    // Update host section
    const hostSection = document.getElementById('host-section');
    if (hostSection) {
        const hostName = place.owner_name || place.owner_id || 'Host';
        const hostInitial = hostName.charAt(0).toUpperCase();
        
        hostSection.innerHTML = `
            <div class="host-header">
                <div class="host-info">
                    <h2>Hosted by ${escapeHtml(hostName)}</h2>
                    <p class="host-details">Superhost · Hosting since 2024</p>
                </div>
                <div class="host-avatar">${hostInitial}</div>
            </div>
        `;
    }
    
    // Update description
    const descSection = document.getElementById('description-section');
    if (descSection) {
        descSection.innerHTML = `
            <h2>About this place</h2>
            <p class="description-text">${escapeHtml(place.description || 'Beautiful place to stay')}</p>
        `;
    }
    
    // Update amenities
    displayAmenities(place.amenities);
    
    console.log('Enhanced place details displayed successfully');
}

function displayOriginalPlace(place) {
    console.log('Using original layout');
    
    const placeDetailsSection = document.getElementById('place-details');
    
    if (!placeDetailsSection) {
        console.error('Place details section not found');
        return;
    }
    
    document.title = `${place.title} - HBnB`;
    
    let amenitiesHtml = 'None listed';
    if (place.amenities && place.amenities.length > 0) {
        amenitiesHtml = place.amenities.map(a => escapeHtml(a.name || a)).join(', ');
    }
    
    placeDetailsSection.innerHTML = `
        <h1>${escapeHtml(place.title)}</h1>
        <div class="place-details">
            <div class="place-info">
                <p><strong>Host:</strong> ${escapeHtml(place.owner_name || place.owner_id || 'Unknown')}</p>
                <p><strong>Price per night:</strong> $${place.price}</p>
                <p><strong>Description:</strong> ${escapeHtml(place.description || 'No description available')}</p>
                <p><strong>Amenities:</strong> ${amenitiesHtml}</p>
            </div>
        </div>
    `;
    
    console.log('Original place details displayed successfully');
}

function displayAmenities(amenities) {
    const amenitiesGrid = document.getElementById('amenities-grid');
    
    if (!amenitiesGrid) {
        return;
    }
    
    if (!amenities || amenities.length === 0) {
        amenitiesGrid.innerHTML = '<p class="no-amenities">No amenities listed</p>';
        return;
    }
    
    amenitiesGrid.innerHTML = amenities.map(amenity => {
        const name = amenity.name || amenity;
        const icon = getAmenityIcon(name);
        
        return `
            <div class="amenity-item">
                <span class="amenity-icon">${icon}</span>
                <span>${escapeHtml(name)}</span>
            </div>
        `;
    }).join('');
}

function getAmenityIcon(amenityName) {
    const name = amenityName.toLowerCase();
    
    for (const [key, icon] of Object.entries(amenityIcons)) {
        if (name.includes(key)) {
            return icon;
        }
    }
    
    return amenityIcons.default;
}

async function fetchPlaceReviews(placeId) {
    console.log('Fetching reviews for place:', placeId);
    
    try {
        const response = await fetch(`${API_BASE_URL}/reviews/places/${placeId}/reviews`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            if (response.status === 404) {
                console.log('No reviews found for this place');
                displayReviews([]);
                return;
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const reviews = await response.json();
        console.log('Reviews fetched successfully:', reviews);
        
        displayReviews(reviews);
        updateReviewStats(reviews);
        
    } catch (error) {
        console.error('Error fetching reviews:', error);
        displayReviews([]);
    }
}

function displayReviews(reviews) {
    console.log('Displaying reviews...', reviews.length, 'reviews');
    
    const reviewsList = document.getElementById('reviews-list');
    
    if (!reviewsList) {
        console.error('Reviews list container not found');
        return;
    }
    
    reviewsList.innerHTML = '';
    
    if (!reviews || reviews.length === 0) {
        reviewsList.innerHTML = '<p class="no-reviews">No reviews yet. Be the first to review!</p>';
        return;
    }
    
    reviews.forEach(review => {
        const reviewCard = createReviewCard(review);
        reviewsList.appendChild(reviewCard);
    });
    
    console.log('Reviews displayed successfully');
}

function createReviewCard(review) {
    const card = document.createElement('div');
    card.className = 'review-card';
    
    const reviewerName = review.user_name || review.user_id || 'Anonymous';
    const initial = reviewerName.charAt(0).toUpperCase();
    const stars = generateStarRating(review.rating);
    
    // Check if we have the enhanced layout
    const hasEnhancedLayout = document.getElementById('place-title-section');
    
    if (hasEnhancedLayout) {
        // Enhanced layout with avatar
        card.innerHTML = `
            <div class="review-header">
                <div class="reviewer-avatar">${initial}</div>
                <div class="reviewer-info">
                    <h4>${escapeHtml(reviewerName)}</h4>
                    <p class="review-date">December 2024</p>
                </div>
            </div>
            <p class="review-content">${escapeHtml(review.text)}</p>
            <div class="review-rating">
                <span class="rating-stars">${stars}</span>
            </div>
        `;
    } else {
        // Original layout
        card.innerHTML = `
            <h4>${escapeHtml(reviewerName)}:</h4>
            <p>${escapeHtml(review.text)}</p>
            <p class="rating">Rating: <span class="rating-stars">${stars}</span></p>
        `;
    }
    
    return card;
}

function generateStarRating(rating) {
    const fullStar = '★';
    const emptyStar = '☆';
    let stars = '';
    
    for (let i = 1; i <= 5; i++) {
        stars += i <= rating ? fullStar : emptyStar;
    }
    
    return stars;
}

function updateReviewStats(reviews) {
    const count = reviews.length;
    const avgRating = count > 0 
        ? (reviews.reduce((sum, r) => sum + r.rating, 0) / count).toFixed(1)
        : '5.0';
    
    // Update enhanced layout stats
    const reviewsRating = document.getElementById('reviews-rating');
    const reviewsCount = document.getElementById('reviews-count');
    const bookingRating = document.getElementById('booking-rating');
    const bookingReviewCount = document.getElementById('booking-review-count');
    
    if (reviewsRating) reviewsRating.textContent = avgRating;
    if (reviewsCount) reviewsCount.textContent = count;
    if (bookingRating) bookingRating.textContent = avgRating;
    if (bookingReviewCount) {
        bookingReviewCount.textContent = `${count} ${count === 1 ? 'review' : 'reviews'}`;
    }
}

function setupReviewForm(placeId) {
    console.log('Setting up review form for place:', placeId);
    
    const reviewForm = document.getElementById('review-form');
    
    if (!reviewForm) {
        console.log('Review form not found on this page');
        return;
    }
    
    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        console.log('Review form submitted');
        
        const reviewText = document.getElementById('review-text').value.trim();
        const rating = document.getElementById('rating').value;
        
        if (!reviewText || !rating) {
            showReviewError('Please fill in all fields');
            return;
        }
        
        console.log('Submitting review:', { placeId, reviewText, rating });
        
        await submitReview(placeId, reviewText, parseInt(rating));
    });
    
    console.log('Review form setup complete');
}

async function submitReview(placeId, text, rating) {
    console.log('Submitting review...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                place_id: placeId,
                text: text,
                rating: rating
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            console.log('Review submitted successfully:', data);
            showReviewSuccess('Review submitted successfully!');
            
            document.getElementById('review-text').value = '';
            document.getElementById('rating').value = '1';
            
            fetchPlaceReviews(placeId);
            
        } else {
            console.error('Failed to submit review:', data);
            showReviewError(data.error || 'Failed to submit review');
        }
        
    } catch (error) {
        console.error('Error submitting review:', error);
        showReviewError('Unable to submit review. Please try again later.');
    }
}

function showPlaceDetailsError(message) {
    console.error('Place details error:', message);
    
    const placeDetailsSection = document.getElementById('place-details') || document.getElementById('place-title-section');
    
    if (placeDetailsSection) {
        placeDetailsSection.innerHTML = `
            <div class="error-message" style="text-align: center; padding: 40px;">
                <h2>Error</h2>
                <p>${message}</p>
                <a href="/" class="details-button" style="margin-top: 20px;">Back to Home</a>
            </div>
        `;
    }
}

function showReviewError(message) {
    console.error('Review error:', message);
    
    const existingMessage = document.querySelector('.review-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    const addReviewSection = document.getElementById('add-review');
    if (!addReviewSection) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'review-message error-message';
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        background-color: #fee;
        color: #c33;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #fcc;
        font-weight: 500;
    `;
    
    addReviewSection.insertBefore(messageDiv, addReviewSection.querySelector('form'));
    
    setTimeout(() => messageDiv.remove(), 5000);
}

function showReviewSuccess(message) {
    console.log('Review success:', message);
    
    const existingMessage = document.querySelector('.review-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    const addReviewSection = document.getElementById('add-review');
    if (!addReviewSection) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'review-message success-message';
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        background-color: #efe;
        color: #2a7;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #cfc;
        font-weight: 500;
    `;
    
    addReviewSection.insertBefore(messageDiv, addReviewSection.querySelector('form'));
    
    setTimeout(() => messageDiv.remove(), 5000);
}

// =============================================================================
// BOOKING CARD FUNCTIONS (Enhanced Features)
// =============================================================================

function updateBookingCard(place) {
    const bookingPrice = document.getElementById('booking-price');
    if (bookingPrice) {
        bookingPrice.textContent = `$${place.price}`;
    }
    calculateBookingPrice();
}

function setupBookingCalculations() {
    const checkInDate = document.getElementById('check-in-date');
    const checkOutDate = document.getElementById('check-out-date');
    const guestsSelect = document.getElementById('guests-select');
    const reserveButton = document.querySelector('.reserve-button');
    
    if (checkInDate) checkInDate.addEventListener('change', calculateBookingPrice);
    if (checkOutDate) checkOutDate.addEventListener('change', calculateBookingPrice);
    if (guestsSelect) guestsSelect.addEventListener('change', calculateBookingPrice);
    
    if (reserveButton) {
        reserveButton.addEventListener('click', handleReservation);
    }
}

function calculateBookingPrice() {
    if (!currentPlace) return;
    
    const checkInInput = document.getElementById('check-in-date');
    const checkOutInput = document.getElementById('check-out-date');
    
    if (!checkInInput || !checkOutInput) return;
    
    const checkIn = new Date(checkInInput.value);
    const checkOut = new Date(checkOutInput.value);
    
    const nights = Math.max(1, Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24)));
    const pricePerNight = currentPlace.price;
    const cleaningFee = 50;
    
    const subtotal = pricePerNight * nights;
    const serviceFee = Math.round(subtotal * 0.14);
    const total = subtotal + cleaningFee + serviceFee;
    
    const priceCalcText = document.getElementById('price-calc-text');
    const priceCalcTotal = document.getElementById('price-calc-total');
    const serviceFeeEl = document.getElementById('service-fee');
    const totalPriceEl = document.getElementById('total-price');
    
    if (priceCalcText) priceCalcText.textContent = `$${pricePerNight} × ${nights} nights`;
    if (priceCalcTotal) priceCalcTotal.textContent = `$${subtotal}`;
    if (serviceFeeEl) serviceFeeEl.textContent = `$${serviceFee}`;
    if (totalPriceEl) totalPriceEl.textContent = `$${total}`;
}

function handleReservation() {
    if (!authToken) {
        alert('Please log in to make a reservation');
        window.location.href = '/login';
        return;
    }
    
    alert('Reservation feature coming soon!');
}

// =============================================================================
// INDEX PAGE - AUTHENTICATION FUNCTIONS
// =============================================================================

function checkAuthentication() {
    console.log('Checking user authentication...');
    
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    
    if (!token) {
        console.log('User is not authenticated');
        
        if (loginLink) {
            loginLink.style.display = 'block';
        }
        
        fetchPlaces(null);
    } else {
        console.log('User is authenticated');
        
        if (loginLink) {
            loginLink.style.display = 'none';
        }
        
        fetchPlaces(token);
    }
}

function getCookie(name) {
    const cookies = document.cookie.split(';');
    
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        
        if (cookieName === name) {
            return cookieValue;
        }
    }
    
    return null;
}

// =============================================================================
// INDEX PAGE - PLACES DATA FUNCTIONS
// =============================================================================

async function fetchPlaces(token) {
    console.log('Fetching places from API...');
    
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`${API_BASE_URL}/places/`, {
            method: 'GET',
            headers: headers
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const places = await response.json();
        
        console.log('Places fetched successfully:', places);
        console.log('Number of places:', places.length);
        
        allPlaces = places;
        
        displayPlaces(places);
        
    } catch (error) {
        console.error('Error fetching places:', error);
        showPlacesError('Unable to load places. Please try again later.');
    }
}

function displayPlaces(places) {
    console.log('Displaying places...');
    
    const placesList = document.getElementById('places-list');
    
    if (!placesList) {
        console.error('Places list container not found');
        return;
    }
    
    placesList.innerHTML = '';
    
    if (!places || places.length === 0) {
        placesList.innerHTML = '<p class="no-places" style="grid-column: 1 / -1; text-align: center; padding: 40px; color: #767676;">No places available at the moment.</p>';
        return;
    }
    
    places.forEach(place => {
        const placeCard = createPlaceCard(place);
        placesList.appendChild(placeCard);
    });
    
    console.log('Places displayed successfully');
}

function createPlaceCard(place) {
    const card = document.createElement('div');
    card.className = 'place-card';
    
    card.dataset.price = place.price;
    card.dataset.placeId = place.id;
    
    card.innerHTML = `
        <h3>${escapeHtml(place.title)}</h3>
        <p class="price">Price per night: $${place.price}</p>
        <a href="/place/${place.id}" class="details-button">View Details</a>
    `;
    
    return card;
}

function escapeHtml(text) {
    if (!text) return '';
    
    const div = document.createElement('div');
    div.textContent = text;
    
    return div.innerHTML;
}

function showPlacesError(message) {
    console.error('Places error:', message);
    
    const placesList = document.getElementById('places-list');
    
    if (placesList) {
        placesList.innerHTML = `
            <div class="error-message" style="grid-column: 1 / -1; text-align: center; padding: 40px;">
                <p>${message}</p>
            </div>
        `;
    }
}

// =============================================================================
// INDEX PAGE - PRICE FILTER FUNCTIONS
// =============================================================================

function setupPriceFilter() {
    console.log('Setting up price filter...');
    
    const priceFilter = document.getElementById('price-filter');
    
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            console.log('Price filter changed to:', selectedPrice);
            filterPlacesByPrice(selectedPrice);
        });
        
        console.log('Price filter setup complete');
    } else {
        console.log('Price filter element not found');
    }
}

function filterPlacesByPrice(maxPrice) {
    console.log('Filtering places by price:', maxPrice);
    
    const placeCards = document.querySelectorAll('.place-card');
    
    let visibleCount = 0;
    
    placeCards.forEach(card => {
        const placePrice = parseFloat(card.dataset.price);
        
        if (maxPrice === 'all') {
            card.style.display = 'block';
            visibleCount++;
        } else {
            const maxPriceNum = parseFloat(maxPrice);
            
            if (placePrice <= maxPriceNum) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        }
    });
    
    console.log('Visible places after filtering:', visibleCount);
    
    checkVisiblePlaces();
}

function checkVisiblePlaces() {
    const placesList = document.getElementById('places-list');
    const placeCards = document.querySelectorAll('.place-card');
    
    let visibleCount = 0;
    placeCards.forEach(card => {
        if (card.style.display !== 'none') {
            visibleCount++;
        }
    });
    
    const existingMessage = document.querySelector('.no-results-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    if (visibleCount === 0 && placeCards.length > 0) {
        const noResultsDiv = document.createElement('div');
        noResultsDiv.className = 'no-results-message';
        noResultsDiv.style.cssText = `
            grid-column: 1 / -1;
            text-align: center;
            padding: 40px;
            color: #767676;
            font-size: 1.1rem;
        `;
        noResultsDiv.textContent = 'No places found within this price range.';
        placesList.appendChild(noResultsDiv);
    }
}

// =============================================================================
// LOGIN FORM FUNCTIONS
// =============================================================================

function setupLoginForm(loginForm) {
    console.log('Setting up login form...');
    
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        console.log('Login form submitted');
        
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        
        if (!email || !password) {
            showError('Please enter both email and password');
            return;
        }
        
        if (!isValidEmail(email)) {
            showError('Please enter a valid email address');
            return;
        }
        
        const submitButton = loginForm.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;
        submitButton.textContent = 'Logging in...';
        submitButton.disabled = true;
        
        try {
            await loginUser(email, password);
        } catch (error) {
            console.error('Login error:', error);
            showError('An unexpected error occurred. Please try again.');
        } finally {
            submitButton.textContent = originalButtonText;
            submitButton.disabled = false;
        }
    });
    
    console.log('Login form setup complete');
}

async function loginUser(email, password) {
    console.log('Attempting login for:', email);
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                email: email, 
                password: password 
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            console.log('Login successful!');
            handleLoginSuccess(data);
        } else {
            console.error('Login failed:', data);
            handleLoginFailure(response.status, data);
        }
        
    } catch (error) {
        console.error('Network error:', error);
        showError('Unable to connect to the server. Please check your connection.');
        throw error;
    }
}

function handleLoginSuccess(data) {
    console.log('Handling login success...');
    
    const token = data.access_token;
    
    if (!token) {
        showError('Login successful but no token received');
        return;
    }
    
    setTokenCookie(token);
    
    if (data.user) {
        localStorage.setItem('user', JSON.stringify(data.user));
    }
    
    showSuccess('Login successful! Redirecting...');
    
    setTimeout(() => {
        window.location.href = '/';
    }, 1000);
}

function handleLoginFailure(statusCode, data) {
    console.log('Handling login failure, status:', statusCode);
    
    let errorMessage = 'Login failed. Please try again.';
    
    switch (statusCode) {
        case 400:
            errorMessage = 'Invalid email or password format';
            break;
        case 401:
            errorMessage = 'Invalid email or password';
            break;
        case 404:
            errorMessage = 'User not found';
            break;
        case 500:
            errorMessage = 'Server error. Please try again later';
            break;
        default:
            if (data.error) {
                errorMessage = data.error;
            } else if (data.message) {
                errorMessage = data.message;
            }
    }
    
    showError(errorMessage);
}

// =============================================================================
// COOKIE MANAGEMENT FUNCTIONS
// =============================================================================

function setTokenCookie(token) {
    console.log('Storing token in cookie...');
    
    const expirationDays = 7;
    const date = new Date();
    date.setTime(date.getTime() + (expirationDays * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;
    
    document.cookie = `token=${token}; ${expires}; path=/; SameSite=Strict`;
    
    console.log('Token stored in cookie successfully');
}

function getTokenFromCookie() {
    return getCookie('token');
}

function removeTokenCookie() {
    console.log('Removing token from cookie...');
    
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    
    localStorage.removeItem('user');
    
    console.log('Token removed from cookie');
}

function logoutUser() {
    console.log('Logging out user...');
    removeTokenCookie();
    window.location.href = '/login';
}

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

function checkAuthStatus() {
    const token = getTokenFromCookie();
    
    if (token) {
        console.log('User is authenticated');
        return true;
    } else {
        console.log('User is not authenticated');
        return false;
    }
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showError(message) {
    console.error('Showing error:', message);
    
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        background-color: #fee;
        color: #c33;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #fcc;
        font-weight: 500;
    `;
    
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.parentNode.insertBefore(errorDiv, loginForm);
    } else {
        const main = document.querySelector('main');
        if (main) {
            main.insertBefore(errorDiv, main.firstChild);
        }
    }
    
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 5000);
}

function showSuccess(message) {
    console.log('Showing success:', message);
    
    const existingMessage = document.querySelector('.success-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    successDiv.style.cssText = `
        background-color: #efe;
        color: #2a7;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #cfc;
        font-weight: 500;
    `;
    
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.parentNode.insertBefore(successDiv, loginForm);
    }
}

async function authenticatedFetch(url, options = {}) {
    const token = getTokenFromCookie();
    
    if (!token) {
        throw new Error('No authentication token found');
    }
    
    options.headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
    
    const response = await fetch(url, options);
    
    if (response.status === 401) {
        console.log('Token expired or invalid, redirecting to login...');
        removeTokenCookie();
        window.location.href = '/login';
    }
    
    return response;
}

// =============================================================================
// EXPORT FUNCTIONS (for module usage if needed)
// =============================================================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        loginUser,
        logoutUser,
        checkAuthStatus,
        getTokenFromCookie,
        authenticatedFetch,
        fetchPlaces,
        displayPlaces,
        filterPlacesByPrice,
        fetchPlaceDetails,
        displayPlaceDetails,
        getCookie,
        escapeHtml,
        generateStarRating
    };
}