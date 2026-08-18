import React from 'react';
import './connectionstatus.css';  // Make sure this matches the CSS file name

const ConnectionStatus = ({ statuses }) => {

    if (!typeof statuses === 'object' || !statuses.length)
        statuses = [];

    return (
        <div>
            {statuses.map((status, index) => (
                <span key={index} className={`status-dot ${status ? 'online' : 'offline'}`}></span>
            ))}
        </div>
    );
};

export default ConnectionStatus;
