const API = {
    base: '/api',

    getToken() {
        return localStorage.getItem('token');
    },

    getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    setAuth(token, user) {
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
    },

    clearAuth() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    },

    async request(endpoint, options = {}) {
        const headers = { 'Content-Type': 'application/json', ...options.headers };
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Token ${token}`;
        }

        const response = await fetch(`${this.base}${endpoint}`, {
            ...options,
            headers,
        });

        let data = null;
        const text = await response.text();
        if (text) {
            try {
                data = JSON.parse(text);
            } catch {
                data = { detail: text };
            }
        }

        if (!response.ok) {
            const message = data?.detail || data?.message || JSON.stringify(data) || 'Request failed';
            throw new Error(typeof message === 'string' ? message : JSON.stringify(message));
        }

        return data;
    },

    register(payload) {
        return this.request('/register', { method: 'POST', body: JSON.stringify(payload) });
    },

    login(payload) {
        return this.request('/login', { method: 'POST', body: JSON.stringify(payload) });
    },

    getMyTickets() {
        return this.request('/tickets/my');
    },

    getAllTickets(params = '') {
        return this.request(`/tickets/all${params}`);
    },

    getTicket(id) {
        return this.request(`/tickets/${id}`);
    },

    createTicket(payload) {
        return this.request('/tickets', { method: 'POST', body: JSON.stringify(payload) });
    },

    updateTicketStatus(id, payload) {
        return this.request(`/tickets/${id}/status`, {
            method: 'PATCH',
            body: JSON.stringify(payload),
        });
    },

    addComment(id, message) {
        return this.request(`/tickets/${id}/comment`, {
            method: 'POST',
            body: JSON.stringify({ message }),
        });
    },

    closeTicket(id) {
        return this.request(`/tickets/${id}/close`, { method: 'POST' });
    },

    getReports() {
        return this.request('/tickets/reports');
    },

    getUsers(role = '') {
        return this.request(`/users${role ? `?role=${role}` : ''}`);
    },

    createUser(payload) {
        return this.request('/users', { method: 'POST', body: JSON.stringify(payload) });
    },

    updateUser(id, payload) {
        return this.request(`/users/${id}`, { method: 'PATCH', body: JSON.stringify(payload) });
    },

    deleteUser(id) {
        return this.request(`/users/${id}`, { method: 'DELETE' });
    },

    getAgents() {
        return this.request('/agents');
    },

    getFAQ(search = '') {
        return this.request(`/faq${search ? `?search=${encodeURIComponent(search)}` : ''}`);
    },

    createFAQ(payload) {
        return this.request('/faq', { method: 'POST', body: JSON.stringify(payload) });
    },

    updateFAQ(id, payload) {
        return this.request(`/faq/${id}`, { method: 'PATCH', body: JSON.stringify(payload) });
    },

    deleteFAQ(id) {
        return this.request(`/faq/${id}`, { method: 'DELETE' });
    },
};

function requireAuth(allowedRoles = []) {
    const user = API.getUser();
    if (!user || !API.getToken()) {
        window.location.href = '/login/';
        return null;
    }
    if (allowedRoles.length && !allowedRoles.includes(user.role)) {
        redirectByRole(user.role);
        return null;
    }
    return user;
}

function redirectByRole(role) {
    const routes = {
        employee: '/dashboard/employee/',
        agent: '/dashboard/agent/',
        admin: '/dashboard/admin/',
    };
    window.location.href = routes[role] || '/login/';
}

function logout() {
    API.clearAuth();
    window.location.href = '/login/';
}

function formatDate(iso) {
    return new Date(iso).toLocaleString();
}

function statusBadge(status) {
    const label = status.replace('_', ' ');
    return `<span class="badge badge-${status}">${label}</span>`;
}

function priorityBadge(priority) {
    return `<span class="badge badge-${priority}">${priority}</span>`;
}

function showAlert(container, message, type = 'error') {
    container.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
}
