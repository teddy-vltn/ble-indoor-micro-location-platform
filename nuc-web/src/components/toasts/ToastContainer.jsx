// components/ToastContainer/ToastContainer.js
import React, { useEffect, useState } from 'react';
import ToastManager from './ToastManager';
import Toast from './Toast';
import './toast.css';

const ToastContainer = () => {
  const [toasts, setToasts] = useState([]);

  useEffect(() => {
    const updateToasts = (newToasts) => setToasts(newToasts);
    ToastManager.subscribe(updateToasts);
    return () => ToastManager.unsubscribe(updateToasts);
  }, []);

  const handleClose = (id) => {
    ToastManager.removeToast(id);
  };

  return (
    <div className="toast-container">
      {toasts.map((toast) => (
        <Toast
          key={toast.id}
          message={toast.message}
          type={toast.type}
          onClose={() => handleClose(toast.id)}
        />
      ))}
    </div>
  );
};

export default ToastContainer;

