'use strict';

class ModalManager {
  constructor() {
    this.container = document.getElementById('modal-container');
  }

  open({ title, body, footer, width = '600px', onClose }) {
    if (!this.container) this.container = document.getElementById('modal-container');

    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay active';
    overlay.innerHTML = `
      <div class="modal-dialog" style="max-width: ${width};">
        <div class="modal-header">
          <h3 class="card-title">${title}</h3>
          <button class="btn btn-secondary btn-sm" style="border:none; padding:4px 8px;" id="modal-close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">${body}</div>
        ${footer ? `<div class="modal-footer">${footer}</div>` : ''}
      </div>
    `;

    this.container.innerHTML = '';
    this.container.appendChild(overlay);

    const close = () => {
      overlay.classList.remove('active');
      setTimeout(() => {
        overlay.remove();
        if (onClose) onClose();
      }, 200);
    };

    overlay.querySelector('#modal-close-btn').addEventListener('click', close);
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) close();
    });

    return { close, element: overlay };
  }

  close() {
    if (this.container) this.container.innerHTML = '';
  }
}

window.Modal = new ModalManager();
