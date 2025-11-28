/**
 * HBnB Application - Main JavaScript
 * Handles user authentication, places display, filtering, place details, and reviews
 */

// =============================================================================
// API CONFIGURATION
// =============================================================================

// API Configuration - Update this URL if your API is hosted elsewhere
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

// Store places data globally for filtering
let allPlaces = [];

// Store token globally for use across functions
let authToken = null;

// =============================================================================
// DOM CONTENT LOADED - MAIN ENTRY POINT
// =============================================================================

/**
 * Wait for DOM to be fully loaded before initializing
 * This ensures all HTML elements exist before we try to access them
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded, initializing application...');
    
    // Check if we're on the login page (has login-form)
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        console.log('Login page detected, setting up login form...');
        setupLoginForm(loginForm);
    }
    
    // Check if we're on the index page (has places-list section)
    const placesList = document.getElementById('places-list');
    
    if (placesList) {
        console.log('Index page detected, initializing places list...');
        // Check authentication and setup page
        checkAuthentication();
        
        // Setup price filter
        setupPriceFilter();
    }
    
    // Check if we're on the place details page (has place-details section)
    const placeDetails = document.getElementById('place-details');
    
    if (placeDetails) {
        console.log('Place details page detected, initializing...');
        // Initialize place details page
        initPlaceDetailsPage();
    }
    
    // Check if we're on the add review page (has review-form but NOT place-details)
    const reviewForm = document.getElementById('review-form');
    const pageTitle = document.getElementById('page-title');
    
    if (reviewForm && !placeDetails && pageTitle) {
        console.log('Add review page detected, initializing...');
        // Initialize add review page
        initAddReviewPage();
    }
    
    console.log('Application initialization complete.');
});

// =============================================================================
// ADD REVIEW PAGE FUNCTIONS
// =============================================================================

/**
 * Initialize the add review page
 * This page requires authentication - unauthenticated users are redirected
 */
function initAddReviewPage() {
    console.log('Initializing add review page...');
    
    // Check authentication - redirect if not logged in
    authToken = checkAuthenticationRequired();
    
    if (!authToken) {
        // User not authenticated, redirect is happening
        return;
    }
    
    // Get place ID from URL
    const placeId = getPlaceIdFromURL();
    
    if (!placeId) {
        console.error('No place ID found in URL');
        showAddReviewError('No place ID provided. Please select a place to review.');
        return;
    }
    
    console.log('Place ID for review:', placeId);
    
    // Fetch place details to show the place name
    fetchPlaceNameForReview(placeId);
    
    // Setup the review form
    setupAddReviewForm(placeId);
}

/**
 * Check if user is authenticated, redirect to index if not
 * This is used for pages that REQUIRE authentication
 * @returns {string|null} - Token if authenticated, null otherwise
 */
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

/**
 * Fetch place name to display on the review page
 * Updates the page title to show which place is being reviewed
 * @param {string} placeId - The place ID
 */
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
            
            // Update the page title
            const pageTitle = document.getElementById('page-title');
            if (pageTitle) {
                pageTitle.textContent = `Reviewing: ${place.title}`;
            }
            
            // Update the browser tab title
            document.title = `Add Review - ${place.title} - HBnB`;
        } else {
            console.error('Failed to fetch place:', response.status);
        }
    } catch (error) {
        console.error('Error fetching place name:', error);
    }
}

/**
 * Setup the add review form submission handler
 * @param {string} placeId - The place ID for the review
 */
function setupAddReviewForm(placeId) {
    console.log('Setting up add review form...');
    
    const reviewForm = document.getElementById('review-form');
    
    if (!reviewForm) {
        console.error('Review form not found');
        return;
    }
    
    reviewForm.addEventListener('submit', async (event) => {
        // Prevent default form submission (page reload)
        event.preventDefault();
        
        console.log('Review form submitted');
        
        // Get form values
        const reviewText = document.getElementById('review-text').value.trim();
        const rating = document.getElementById('rating').value;
        
        // Validate inputs
        if (!reviewText) {
            showAddReviewError('Please enter your review text');
            return;
        }
        
        if (!rating) {
            showAddReviewError('Please select a rating');
            return;
        }
        
        console.log('Review data:', { placeId, reviewText, rating });
        
        // Disable submit button to prevent double submission
        const submitButton = reviewForm.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Submitting...';
        submitButton.disabled = true;
        
        try {
            // Submit the review
            await submitReviewFromForm(placeId, reviewText, parseInt(rating));
        } finally {
            // Re-enable submit button
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        }
    });
    
    console.log('Add review form setup complete');
}

/**
 * Submit a review from the add review page
 * @param {string} placeId - The place ID
 * @param {string} text - Review text
 * @param {number} rating - Rating value (1-5)
 */
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
            
            // Clear the form
            document.getElementById('review-text').value = '';
            document.getElementById('rating').value = '1';
            
            // Redirect to place details page after short delay
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

/**
 * Show error message on add review page
 * @param {string} message - Error message
 */
function showAddReviewError(message) {
    showFormMessage(message, 'error');
}

/**
 * Show success message on add review page
 * @param {string} message - Success message
 */
function showAddReviewSuccess(message) {
    showFormMessage(message, 'success');
}

/**
 * Show a message on the add review form
 * @param {string} message - Message text
 * @param {string} type - Message type ('error' or 'success')
 */
function showFormMessage(message, type) {
    console.log(`Showing ${type} message:`, message);
    
    // Remove any existing messages
    const existingMessage = document.querySelector('.form-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `form-message ${type}-message`;
    messageDiv.textContent = message;
    
    // Style based on type
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
    
    // Insert before the form
    const addReviewDiv = document.querySelector('.add-review');
    const form = document.getElementById('review-form');
    
    if (addReviewDiv && form) {
        addReviewDiv.insertBefore(messageDiv, form);
    }
    
    // Auto-remove after 5 seconds (except for success which redirects)
    if (type === 'error') {
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }
}

// =============================================================================
// PLACE DETAILS PAGE FUNCTIONS
// =============================================================================

/**
 * Initialize the place details page
 * Fetches and displays place information, reviews, and review form
 */
function initPlaceDetailsPage() {
    console.log('Initializing place details page...');
    
    // Get place ID from URL
    const placeId = getPlaceIdFromURL();
    
    if (!placeId) {
        console.error('No place ID found in URL');
        showPlaceDetailsError('No place ID provided in URL');
        return;
    }
    
    console.log('Place ID from URL:', placeId);
    
    // Check authentication and get token
    authToken = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');
    
    if (!authToken) {
        // User is not authenticated
        console.log('User not authenticated - showing login link, hiding review form');
        
        if (loginLink) {
            loginLink.style.display = 'block';
        }
        if (addReviewSection) {
            addReviewSection.style.display = 'none';
        }
    } else {
        // User is authenticated
        console.log('User authenticated - hiding login link, showing review form');
        
        if (loginLink) {
            loginLink.style.display = 'none';
        }
        if (addReviewSection) {
            addReviewSection.style.display = 'block';
        }
        
        // Setup review form submission
        setupReviewForm(placeId);
    }
    
    // Fetch and display place details
    fetchPlaceDetails(authToken, placeId);
}

/**
 * Extract the place ID from the URL
 * Supports both query parameters (?id=xxx or ?place_id=xxx) and path parameters (/place/xxx)
 * @returns {string|null} - Place ID or null if not found
 */
function getPlaceIdFromURL() {
    console.log('Extracting place ID from URL...');
    console.log('Current URL:', window.location.href);
    console.log('Pathname:', window.location.pathname);
    console.log('Search:', window.location.search);
    
    // First, try to get from query parameters (e.g., ?id=xxx or ?place_id=xxx)
    const urlParams = new URLSearchParams(window.location.search);
    let placeId = urlParams.get('id') || urlParams.get('place_id');
    
    if (placeId) {
        console.log('Place ID found in query parameters:', placeId);
        return placeId;
    }
    
    // If not in query params, try to get from path (e.g., /place/xxx or /add_review/xxx)
    const pathParts = window.location.pathname.split('/');
    console.log('Path parts:', pathParts);
    
    // Look for 'place' or 'add_review' in the path and get the next segment
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

/**
 * Fetch place details from the API
 * @param {string|null} token - JWT token for authentication (optional)
 * @param {string} placeId - The place ID to fetch
 */
async function fetchPlaceDetails(token, placeId) {
    console.log('Fetching place details for:', placeId);
    
    try {
        // Build request headers
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Include token in Authorization header if available
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        // Fetch place details
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
        
        // Display place details
        displayPlaceDetails(place);
        
        // Fetch and display reviews for this place
        fetchPlaceReviews(placeId);
        
    } catch (error) {
        console.error('Error fetching place details:', error);
        showPlaceDetailsError(error.message || 'Unable to load place details. Please try again later.');
    }
}

/**
 * Display place details in the page
 * @param {Object} place - Place data object
 */
function displayPlaceDetails(place) {
    console.log('Displaying place details...');
    
    const placeDetailsSection = document.getElementById('place-details');
    
    if (!placeDetailsSection) {
        console.error('Place details section not found');
        return;
    }
    
    // Update page title in browser tab
    document.title = `${place.title} - HBnB`;
    
    // Build amenities string
    let amenitiesHtml = 'None listed';
    if (place.amenities && place.amenities.length > 0) {
        // Handle both array of objects and array of strings
        amenitiesHtml = place.amenities.map(a => escapeHtml(a.name || a)).join(', ');
    }
    
    // Create the place details HTML
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
    
    console.log('Place details displayed successfully');
}

/**
 * Fetch reviews for a specific place
 * @param {string} placeId - The place ID
 */
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
                // Place might not have reviews yet
                console.log('No reviews found for this place');
                displayReviews([]);
                return;
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const reviews = await response.json();
        console.log('Reviews fetched successfully:', reviews);
        
        displayReviews(reviews);
        
    } catch (error) {
        console.error('Error fetching reviews:', error);
        displayReviews([]);
    }
}

/**
 * Display reviews in the reviews section
 * @param {Array} reviews - Array of review objects
 */
function displayReviews(reviews) {
    console.log('Displaying reviews...', reviews.length, 'reviews');
    
    const reviewsList = document.getElementById('reviews-list');
    
    if (!reviewsList) {
        console.error('Reviews list container not found');
        return;
    }
    
    // Clear current content
    reviewsList.innerHTML = '';
    
    if (!reviews || reviews.length === 0) {
        reviewsList.innerHTML = '<p class="no-reviews">No reviews yet. Be the first to review!</p>';
        return;
    }
    
    // Create a card for each review
    reviews.forEach(review => {
        const reviewCard = createReviewCard(review);
        reviewsList.appendChild(reviewCard);
    });
    
    console.log('Reviews displayed successfully');
}

/**
 * Create a review card element
 * @param {Object} review - Review data object
 * @returns {HTMLElement} - Review card div element
 */
function createReviewCard(review) {
    // Create the card container
    const card = document.createElement('div');
    card.className = 'review-card';
    
    // Generate star rating display
    const stars = generateStarRating(review.rating);
    
    // Get reviewer name (use user_name if available, otherwise user_id)
    const reviewerName = review.user_name || review.user_id || 'Anonymous';
    
    // Build the card HTML
    card.innerHTML = `
        <h4>${escapeHtml(reviewerName)}:</h4>
        <p>${escapeHtml(review.text)}</p>
        <p class="rating">Rating: <span class="rating-stars">${stars}</span></p>
    `;
    
    return card;
}

/**
 * Generate star rating HTML
 * @param {number} rating - Rating value (1-5)
 * @returns {string} - Star rating HTML string
 */
function generateStarRating(rating) {
    const fullStar = '★';
    const emptyStar = '☆';
    let stars = '';
    
    // Loop through 1-5 and add full or empty star
    for (let i = 1; i <= 5; i++) {
        stars += i <= rating ? fullStar : emptyStar;
    }
    
    return stars;
}

/**
 * Setup the review form submission handler (for place details page)
 * @param {string} placeId - The place ID for the review
 */
function setupReviewForm(placeId) {
    console.log('Setting up review form for place:', placeId);
    
    const reviewForm = document.getElementById('review-form');
    
    if (!reviewForm) {
        console.log('Review form not found on this page');
        return;
    }
    
    reviewForm.addEventListener('submit', async (event) => {
        // Prevent default form submission
        event.preventDefault();
        
        console.log('Review form submitted');
        
        // Get form values
        const reviewText = document.getElementById('review-text').value.trim();
        const rating = document.getElementById('rating').value;
        
        // Validate inputs
        if (!reviewText || !rating) {
            showReviewError('Please fill in all fields');
            return;
        }
        
        console.log('Submitting review:', { placeId, reviewText, rating });
        
        // Submit the review
        await submitReview(placeId, reviewText, parseInt(rating));
    });
    
    console.log('Review form setup complete');
}

/**
 * Submit a new review (for place details page)
 * @param {string} placeId - The place ID
 * @param {string} text - Review text
 * @param {number} rating - Rating value (1-5)
 */
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
            
            // Clear the form
            document.getElementById('review-text').value = '';
            document.getElementById('rating').value = '1';
            
            // Refresh the reviews list
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

/**
 * Show error message on place details page
 * @param {string} message - Error message
 */
function showPlaceDetailsError(message) {
    console.error('Place details error:', message);
    
    const placeDetailsSection = document.getElementById('place-details');
    
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

/**
 * Show error message for review submission (place details page)
 * @param {string} message - Error message
 */
function showReviewError(message) {
    console.error('Review error:', message);
    
    // Remove any existing messages
    const existingMessage = document.querySelector('.review-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    const addReviewSection = document.getElementById('add-review');
    if (!addReviewSection) return;
    
    // Create error message element
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
    
    // Insert before the form
    addReviewSection.insertBefore(messageDiv, addReviewSection.querySelector('form'));
    
    // Auto-remove after 5 seconds
    setTimeout(() => messageDiv.remove(), 5000);
}

/**
 * Show success message for review submission (place details page)
 * @param {string} message - Success message
 */
function showReviewSuccess(message) {
    console.log('Review success:', message);
    
    // Remove any existing messages
    const existingMessage = document.querySelector('.review-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    const addReviewSection = document.getElementById('add-review');
    if (!addReviewSection) return;
    
    // Create success message element
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
    
    // Insert before the form
    addReviewSection.insertBefore(messageDiv, addReviewSection.querySelector('form'));
    
    // Auto-remove after 5 seconds
    setTimeout(() => messageDiv.remove(), 5000);
}

// =============================================================================
// INDEX PAGE - AUTHENTICATION FUNCTIONS
// =============================================================================

/**
 * Check user authentication and control login link visibility
 * If authenticated, fetch and display places
 * This is for pages where authentication is OPTIONAL (like index)
 */
function checkAuthentication() {
    console.log('Checking user authentication...');
    
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    
    if (!token) {
        // User is not authenticated - show login link
        console.log('User is not authenticated');
        
        if (loginLink) {
            loginLink.style.display = 'block';
        }
        
        // Still fetch places (public endpoint)
        fetchPlaces(null);
    } else {
        // User is authenticated - hide login link
        console.log('User is authenticated');
        
        if (loginLink) {
            loginLink.style.display = 'none';
        }
        
        // Fetch places with authentication
        fetchPlaces(token);
    }
}

/**
 * Get a cookie value by its name
 * @param {string} name - Cookie name
 * @returns {string|null} - Cookie value or null if not found
 */
function getCookie(name) {
    // Get all cookies as a string and split by semicolon
    const cookies = document.cookie.split(';');
    
    // Loop through each cookie
    for (let cookie of cookies) {
        // Split the cookie into name and value
        const [cookieName, cookieValue] = cookie.trim().split('=');
        
        // Check if this is the cookie we're looking for
        if (cookieName === name) {
            return cookieValue;
        }
    }
    
    // Cookie not found
    return null;
}

// =============================================================================
// INDEX PAGE - PLACES DATA FUNCTIONS
// =============================================================================

/**
 * Fetch places data from the API
 * @param {string|null} token - JWT token for authentication (optional)
 */
async function fetchPlaces(token) {
    console.log('Fetching places from API...');
    
    try {
        // Build request headers
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Include token in Authorization header if available
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        // Make GET request to fetch places
        const response = await fetch(`${API_BASE_URL}/places/`, {
            method: 'GET',
            headers: headers
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Parse JSON response
        const places = await response.json();
        
        console.log('Places fetched successfully:', places);
        console.log('Number of places:', places.length);
        
        // Store places globally for filtering
        allPlaces = places;
        
        // Display the places
        displayPlaces(places);
        
    } catch (error) {
        console.error('Error fetching places:', error);
        showPlacesError('Unable to load places. Please try again later.');
    }
}

/**
 * Display places in the places-list section
 * @param {Array} places - Array of place objects
 */
function displayPlaces(places) {
    console.log('Displaying places...');
    
    // Get the places list container
    const placesList = document.getElementById('places-list');
    
    if (!placesList) {
        console.error('Places list container not found');
        return;
    }
    
    // Clear current content
    placesList.innerHTML = '';
    
    // Check if there are places to display
    if (!places || places.length === 0) {
        placesList.innerHTML = '<p class="no-places" style="grid-column: 1 / -1; text-align: center; padding: 40px; color: #767676;">No places available at the moment.</p>';
        return;
    }
    
    // Create a card for each place
    places.forEach(place => {
        const placeCard = createPlaceCard(place);
        placesList.appendChild(placeCard);
    });
    
    console.log('Places displayed successfully');
}

/**
 * Create a place card element
 * @param {Object} place - Place data object
 * @returns {HTMLElement} - Place card div element
 */
function createPlaceCard(place) {
    // Create the card container
    const card = document.createElement('div');
    card.className = 'place-card';
    
    // Store price and ID in data attributes for filtering and linking
    card.dataset.price = place.price;
    card.dataset.placeId = place.id;
    
    // Build the card HTML content (no description on index page per design)
    card.innerHTML = `
        <h3>${escapeHtml(place.title)}</h3>
        <p class="price">Price per night: $${place.price}</p>
        <a href="/place/${place.id}" class="details-button">View Details</a>
    `;
    
    return card;
}

/**
 * Escape HTML to prevent XSS attacks
 * This converts special characters to HTML entities
 * @param {string} text - Text to escape
 * @returns {string} - Escaped text
 */
function escapeHtml(text) {
    if (!text) return '';
    
    // Create a temporary div element
    const div = document.createElement('div');
    
    // Set the text content (this automatically escapes HTML)
    div.textContent = text;
    
    // Return the escaped HTML
    return div.innerHTML;
}

/**
 * Show error message when places cannot be loaded
 * @param {string} message - Error message to display
 */
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

/**
 * Setup the price filter dropdown event listener
 */
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

/**
 * Filter displayed places based on selected price
 * @param {string} maxPrice - Maximum price value or 'all'
 */
function filterPlacesByPrice(maxPrice) {
    console.log('Filtering places by price:', maxPrice);
    
    // Get all place cards
    const placeCards = document.querySelectorAll('.place-card');
    
    let visibleCount = 0;
    
    placeCards.forEach(card => {
        // Get the price from the data attribute
        const placePrice = parseFloat(card.dataset.price);
        
        if (maxPrice === 'all') {
            // Show all places
            card.style.display = 'block';
            visibleCount++;
        } else {
            // Convert maxPrice to number for comparison
            const maxPriceNum = parseFloat(maxPrice);
            
            // Show or hide based on price comparison
            if (placePrice <= maxPriceNum) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        }
    });
    
    console.log('Visible places after filtering:', visibleCount);
    
    // Check if any places are visible
    checkVisiblePlaces();
}

/**
 * Check if any places are visible after filtering
 * Show a message if no places match the filter
 */
function checkVisiblePlaces() {
    const placesList = document.getElementById('places-list');
    const placeCards = document.querySelectorAll('.place-card');
    
    // Count visible cards
    let visibleCount = 0;
    placeCards.forEach(card => {
        if (card.style.display !== 'none') {
            visibleCount++;
        }
    });
    
    // Remove existing no-results message if any
    const existingMessage = document.querySelector('.no-results-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Show message if no places match the filter
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

/**
 * Setup login form submission handler
 * @param {HTMLFormElement} loginForm - The login form element
 */
function setupLoginForm(loginForm) {
    console.log('Setting up login form...');
    
    loginForm.addEventListener('submit', async (event) => {
        // Prevent default form submission (page reload)
        event.preventDefault();
        
        console.log('Login form submitted');
        
        // Get form values
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        
        // Validate inputs
        if (!email || !password) {
            showError('Please enter both email and password');
            return;
        }
        
        // Validate email format
        if (!isValidEmail(email)) {
            showError('Please enter a valid email address');
            return;
        }
        
        // Show loading state
        const submitButton = loginForm.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;
        submitButton.textContent = 'Logging in...';
        submitButton.disabled = true;
        
        try {
            // Attempt login
            await loginUser(email, password);
        } catch (error) {
            console.error('Login error:', error);
            showError('An unexpected error occurred. Please try again.');
        } finally {
            // Restore button state
            submitButton.textContent = originalButtonText;
            submitButton.disabled = false;
        }
    });
    
    console.log('Login form setup complete');
}

/**
 * Send login request to API
 * @param {string} email - User email
 * @param {string} password - User password
 */
async function loginUser(email, password) {
    console.log('Attempting login for:', email);
    
    try {
        // Make POST request to login endpoint
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
        
        // Parse JSON response
        const data = await response.json();
        
        // Check if login was successful
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

/**
 * Handle successful login
 * @param {Object} data - Response data containing access token
 */
function handleLoginSuccess(data) {
    console.log('Handling login success...');
    
    // Extract token from response
    const token = data.access_token;
    
    if (!token) {
        showError('Login successful but no token received');
        return;
    }
    
    // Store token in cookie
    setTokenCookie(token);
    
    // Store user info if available (optional)
    if (data.user) {
        localStorage.setItem('user', JSON.stringify(data.user));
    }
    
    // Show success message
    showSuccess('Login successful! Redirecting...');
    
    // Redirect to main page after short delay
    setTimeout(() => {
        window.location.href = '/';
    }, 1000);
}

/**
 * Handle login failure
 * @param {number} statusCode - HTTP status code
 * @param {Object} data - Response data
 */
function handleLoginFailure(statusCode, data) {
    console.log('Handling login failure, status:', statusCode);
    
    let errorMessage = 'Login failed. Please try again.';
    
    // Provide specific error messages based on status code
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

/**
 * Store JWT token in cookie
 * @param {string} token - JWT access token
 */
function setTokenCookie(token) {
    console.log('Storing token in cookie...');
    
    // Calculate expiration (7 days from now)
    const expirationDays = 7;
    const date = new Date();
    date.setTime(date.getTime() + (expirationDays * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;
    
    // Set cookie with token
    // path=/ makes it available on all pages
    // SameSite=Strict helps prevent CSRF attacks
    document.cookie = `token=${token}; ${expires}; path=/; SameSite=Strict`;
    
    console.log('Token stored in cookie successfully');
}

/**
 * Get JWT token from cookie
 * @returns {string|null} - JWT token or null if not found
 */
function getTokenFromCookie() {
    return getCookie('token');
}

/**
 * Remove token cookie (for logout)
 */
function removeTokenCookie() {
    console.log('Removing token from cookie...');
    
    // Set cookie with expired date to delete it
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    
    // Also remove user data from localStorage
    localStorage.removeItem('user');
    
    console.log('Token removed from cookie');
}

/**
 * Logout user
 * Removes token and redirects to login page
 */
function logoutUser() {
    console.log('Logging out user...');
    removeTokenCookie();
    window.location.href = '/login';
}

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

/**
 * Check if user is authenticated
 * @returns {boolean} - True if user has valid token
 */
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

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {boolean} - True if valid email format
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Display error message to user
 * @param {string} message - Error message to display
 */
function showError(message) {
    console.error('Showing error:', message);
    
    // Remove any existing error messages
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Create error message element
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
    
    // Insert error message before form (login page) or at top of main (index page)
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.parentNode.insertBefore(errorDiv, loginForm);
    } else {
        const main = document.querySelector('main');
        if (main) {
            main.insertBefore(errorDiv, main.firstChild);
        }
    }
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 5000);
}

/**
 * Display success message to user
 * @param {string} message - Success message to display
 */
function showSuccess(message) {
    console.log('Showing success:', message);
    
    // Remove any existing messages
    const existingMessage = document.querySelector('.success-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create success message element
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
    
    // Insert success message before form
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.parentNode.insertBefore(successDiv, loginForm);
    }
}

/**
 * Make authenticated API request
 * This is a helper function for making API calls with authentication
 * @param {string} url - API endpoint URL
 * @param {Object} options - Fetch options
 * @returns {Promise<Response>} - Fetch response
 */
async function authenticatedFetch(url, options = {}) {
    const token = getTokenFromCookie();
    
    if (!token) {
        throw new Error('No authentication token found');
    }
    
    // Add Authorization header
    options.headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
    
    const response = await fetch(url, options);
    
    // If unauthorized, redirect to login
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

// Export functions for use in other scripts (if using modules)
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