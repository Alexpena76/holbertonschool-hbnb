/**
 * HBnB Application - Login Functionality
 * Handles user authentication with JWT tokens
 */

// API Configuration
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';  // Update with your API URL

/**
 * Wait for DOM to be fully loaded before attaching event listeners
 */
document.addEventListener('DOMContentLoaded', () => {
    // Check if we're on the login page
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        console.log('Login form found, attaching event listener...');
        setupLoginForm(loginForm);
    }
    
    // Check if user is already logged in (for other pages)
    checkAuthStatus();
});

/**
 * Setup login form submission handler
 * @param {HTMLFormElement} loginForm - The login form element
 */
function setupLoginForm(loginForm) {
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
        window.location.href = 'index.html';
    }, 1000);
}

/**
 * Handle login failure
 * @param {number} statusCode - HTTP status code
 * @param {Object} data - Response data
 */
function handleLoginFailure(statusCode, data) {
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

/**
 * Store JWT token in cookie
 * @param {string} token - JWT access token
 */
function setTokenCookie(token) {
    // Calculate expiration (7 days from now)
    const expirationDays = 7;
    const date = new Date();
    date.setTime(date.getTime() + (expirationDays * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;
    
    // Set cookie with token
    document.cookie = `token=${token}; ${expires}; path=/; SameSite=Strict`;
    
    console.log('Token stored in cookie');
}

/**
 * Get JWT token from cookie
 * @returns {string|null} - JWT token or null if not found
 */
function getTokenFromCookie() {
    // Get all cookies as string
    const cookies = document.cookie.split(';');
    
    // Find token cookie
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'token') {
            return value;
        }
    }
    
    return null;
}

/**
 * Remove token cookie (for logout)
 */
function removeTokenCookie() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    localStorage.removeItem('user');
    console.log('Token removed from cookie');
}

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
 * Logout user
 */
function logoutUser() {
    removeTokenCookie();
    window.location.href = 'login.html';
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
    
    // Insert error message before form
    const loginForm = document.getElementById('login-form');
    loginForm.parentNode.insertBefore(errorDiv, loginForm);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

/**
 * Display success message to user
 * @param {string} message - Success message to display
 */
function showSuccess(message) {
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
        color: #3c3;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #cfc;
        font-weight: 500;
    `;
    
    // Insert success message before form
    const loginForm = document.getElementById('login-form');
    loginForm.parentNode.insertBefore(successDiv, loginForm);
}

/**
 * Make authenticated API request
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
        window.location.href = 'login.html';
    }
    
    return response;
}

// Export functions for use in other scripts (if using modules)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        loginUser,
        logoutUser,
        checkAuthStatus,
        getTokenFromCookie,
        authenticatedFetch
    };
}