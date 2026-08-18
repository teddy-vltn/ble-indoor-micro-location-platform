// components/Toast/Toast.js
import React from 'react';
import './toast.css';

/**
 * Component that renders a toast message.
 * @param {string} message - The message to display in the toast.
 * @param {string} type - The type of the toast. Can be 'success', 'error' or 'warning'.
 * @param {function} onClose - The function to call when the user closes the toast.
 * @returns {JSX.Element} - The rendered toast component.
 */
const Toast = ({ message, type, onClose }) => {
  return (
    <div className={`toast ${type}`}>
      {/* The message to display in the toast. */}
      <span className="toast-message">{message}</span>
      {/* The button to close the toast. */}
      <button className="toast-close" onClick={onClose}>✖</button>
    </div>
  );
};

export default Toast;
