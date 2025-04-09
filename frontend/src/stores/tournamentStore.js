import { writable } from 'svelte/store';
import { getToken } from './userStore';

export const tournaments = writable([]);
export const isLoading = writable(false);
export const error = writable(null);

// Fetch all tournaments
export async function fetchTournaments() {
    isLoading.set(true);
    error.set(null);

    try {
        const response = await fetch('/api/tournaments');

        if (!response.ok) {
            throw new Error('Failed to fetch tournaments');
        }

        const data = await response.json();
        tournaments.set(data);
    } catch (err) {
        error.set(err.message);
        console.error('Error fetching tournaments:', err);
    } finally {
        isLoading.set(false);
    }
}

// Get a specific tournament by ID
export async function getTournament(id) {
    try {
        const response = await fetch(`/api/tournaments/${id}`);

        if (!response.ok) {
            throw new Error('Failed to fetch tournament');
        }

        return await response.json();
    } catch (err) {
        console.error('Error fetching tournament:', err);
        throw err;
    }
}

// Create a new tournament (admin only)
export async function createTournament(tournamentData) {
    const token = getToken();

    if (!token) {
        throw new Error('Authentication required');
    }

    try {
        const response = await fetch('/api/tournaments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(tournamentData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to create tournament');
        }

        const newTournament = await response.json();
        tournaments.update(items => [...items, newTournament]);
        return newTournament;
    } catch (err) {
        console.error('Error creating tournament:', err);
        throw err;
    }
}

// Update an existing tournament (admin only)
export async function updateTournament(id, tournamentData) {
    const token = getToken();

    if (!token) {
        throw new Error('Authentication required');
    }

    try {
        const response = await fetch(`/api/tournaments/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(tournamentData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to update tournament');
        }

        const updatedTournament = await response.json();
        tournaments.update(items => items.map(item => item.id === id ? updatedTournament : item));
        return updatedTournament;
    } catch (err) {
        console.error('Error updating tournament:', err);
        throw err;
    }
}

// Delete a tournament (admin only)
export async function deleteTournament(id) {
    const token = getToken();

    if (!token) {
        throw new Error('Authentication required');
    }

    try {
        const response = await fetch(`/api/tournaments/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to delete tournament');
        }

        tournaments.update(items => items.filter(item => item.id !== id));
        return true;
    } catch (err) {
        console.error('Error deleting tournament:', err);
        throw err;
    }
}