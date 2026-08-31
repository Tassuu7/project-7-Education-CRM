'use strict';

/**
 * Client-Side SPA Hash Router
 */

class Router {
  constructor() {
    this.routes = {};
    this.container = null;
  }

  init() {
    this.container = document.getElementById('view-container');
    window.addEventListener('hashchange', () => this.handleRoute());
    this.handleRoute();
  }

  register(path, view) {
    this.routes[path] = view;
  }

  navigate(path) {
    window.location.hash = path;
  }

  handleRoute() {
    const rawHash = window.location.hash || '#/';
    const path = rawHash.split('?')[0];

    // Re-render sidebar to highlight active route
    if (window.renderSidebar) window.renderSidebar();

    const view = this.routes[path] || this.routes['#/'];
    if (view && this.container) {
      this.container.innerHTML = '';
      view.render(this.container);
      window.scrollTo(0, 0);
    }
  }
}

window.Router = new Router();
