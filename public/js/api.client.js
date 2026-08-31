'use strict';

/**
 * Robust HTTP API Client
 */

class ApiClient {
  constructor(baseUrl = '/api/v1') {
    this.baseUrl = baseUrl;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    };

    if (window.AppState.token) {
      headers['Authorization'] = `Bearer ${window.AppState.token}`;
    }

    try {
      const res = await fetch(url, {
        ...options,
        headers
      });

      // Handle download responses (CSV / binary)
      const contentType = res.headers.get('content-type') || '';
      if (contentType.includes('text/csv')) {
        return await res.text();
      }

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.message || `Request failed with status ${res.status}`);
      }

      return data;
    } catch (err) {
      console.error(`[API Error] ${options.method || 'GET'} ${endpoint}:`, err);
      if (window.Toast) {
        window.Toast.error(err.message || 'Network request failed.');
      }
      throw err;
    }
  }

  get(endpoint, params = {}) {
    const qs = new URLSearchParams(params).toString();
    const full = qs ? `${endpoint}?${qs}` : endpoint;
    return this.request(full, { method: 'GET' });
  }

  post(endpoint, body = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(body)
    });
  }

  put(endpoint, body = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body)
    });
  }

  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

window.API = new ApiClient();
