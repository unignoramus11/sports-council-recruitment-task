import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import jwt_decode from 'jwt-decode';

// Initialize stores
export const isAuthenticated = writable(false);
export const user = writable(null);
export const isAdmin = writable(false);

// Check if we're in a browser environment before accessing localStorage
const storedToken = browser ? localStorage.getItem('token') : null;

// Function to validate JWT token
function validateToken(token) {
    if (!token) return false;

    try {
        const decodedToken = jwt_decode(token);
        const currentTime = Date.now() / 1000;

        // Check if token is expired
        if (decodedToken.exp < currentTime) {
            return false;
        }

        return decodedToken;
    } catch (error) {
        return false;
    }
}

// Initialize authentication state from stored token
export function initAuth() {
    if (!browser) return;

    const token = localStorage.getItem('token');
    const decoded = validateToken(token);

    if (decoded) {
        isAuthenticated.set(true);
        isAdmin.set(decoded.is_admin || false);
        user.set({ username: decoded.sub, isAdmin: decoded.is_admin || false });
    } else {
        // Clear invalid token
        localStorage.removeItem('token');
        isAuthenticated.set(false);
        isAdmin.set(false);
        user.set(null);
    }
}

// Login function
export async function login(username, password) {
    try {
        const response = await fetch('/token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({
                username,
                password
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }

        const data = await response.json();
        const { access_token } = data;

        // Save token to localStorage
        localStorage.setItem('token', access_token);

        // Decode token and update stores
        const decoded = jwt_decode(access_token);
        isAuthenticated.set(true);
        isAdmin.set(decoded.is_admin || false);
        user.set({ username: decoded.sub, isAdmin: decoded.is_admin || false });

        return true;
    } catch (error) {
        console.error('Login error:', error);
        return { error: error.message };
    }
}

// Logout function
export function logout() {
    localStorage.removeItem('token');
    isAuthenticated.set(false);
    isAdmin.set(false);
    user.set(null);
}

// Get authentication token
export function getToken() {
    return browser ? localStorage.getItem('token') : null;
}

// Initialize on import
if (browser) {
    initAuth();
}