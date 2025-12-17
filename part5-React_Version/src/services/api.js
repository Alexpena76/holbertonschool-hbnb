const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

export function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) return cookieValue;
    }
    return null;
}

export function setCookie(name, value, days = 7) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value}; expires=${date.toUTCString()}; path=/; SameSite=Strict`;
}

export function removeCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

export function getToken() { return getCookie('token'); }
export function setToken(token) { setCookie('token', token, 7); }
export function removeToken() { removeCookie('token'); localStorage.removeItem('user'); }

function buildHeaders(includeAuth = false) {
    const headers = { 'Content-Type': 'application/json' };
    if (includeAuth) {
        const token = getToken();
        if (token) headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
}

async function handleResponse(response) {
    const data = await response.json();
    if (!response.ok) {
        const error = new Error(data.error || data.message || 'API request failed');
        error.status = response.status;
        throw error;
    }
    return data;
}

export async function login(email, password) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: buildHeaders(),
        body: JSON.stringify({ email, password })
    });
    const data = await handleResponse(response);
    if (data.access_token) {
        setToken(data.access_token);
        if (data.user) localStorage.setItem('user', JSON.stringify(data.user));
    }
    return data;
}

export function logout() { removeToken(); }
export function isAuthenticated() { return !!getToken(); }

export async function getPlaces() {
    const response = await fetch(`${API_BASE_URL}/places/`, {
        method: 'GET',
        headers: buildHeaders(true)
    });
    return handleResponse(response);
}

export async function getPlace(placeId) {
    const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
        method: 'GET',
        headers: buildHeaders(true)
    });
    return handleResponse(response);
}

export async function getPlaceReviews(placeId) {
    const response = await fetch(`${API_BASE_URL}/reviews/places/${placeId}/reviews`, {
        method: 'GET',
        headers: buildHeaders()
    });
    if (response.status === 404) return [];
    return handleResponse(response);
}

export async function createReview(placeId, text, rating) {
    const token = getToken();
    if (!token) throw new Error('Authentication required');
    const response = await fetch(`${API_BASE_URL}/reviews/`, {
        method: 'POST',
        headers: buildHeaders(true),
        body: JSON.stringify({ place_id: placeId, text, rating })
    });
    return handleResponse(response);
}

export function getCurrentUser() {
    const userJson = localStorage.getItem('user');
    if (userJson) {
        try { return JSON.parse(userJson); }
        catch (e) { return null; }
    }
    return null;
}