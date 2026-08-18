import React from 'react';
import './statusdot.css'; // Ensure this path is correct

const Status = Object.freeze({
    online: 'online',
    offline: 'offline',
    unknown: 'unknown',
});

const StatusColors = Object.freeze({
    [Status.online]: 'forestgreen',
    [Status.offline]: 'red',
    [Status.unknown]: '#808080',
});

/**
 * Converts a status value to a Status constant.
 * 
 * @param {string|boolean} status - The status value to convert.
 * If boolean, it's assumed to be online if true, offline if false.
 * If string, it's assumed to be one of 'online', 'offline', 'unknown'.
 * @returns {string} - The corresponding Status constant.
 */
const getStatus = (status) => {
    // If the status is a boolean, map it to the appropriate Status constant
    if (typeof status === 'boolean') {
        return status ? Status.online : Status.offline;
    }

    // If the status is null or undefined, map it to the unknown Status constant
    if (status === null || status === undefined) {
        return Status.unknown;
    }

    // If the status is a string, map it to the appropriate Status constant
    // (assuming the string is one of 'online', 'offline', 'unknown')
    return status.toLowerCase(); 
};

/**
 * Renders a colored dot representing the status of something.
 * @param {string|boolean} status - The status of the thing to display.
 * If boolean, it's assumed to be online if true, offline if false.
 * If string, it's assumed to be one of 'online', 'offline', 'unknown'.
 * @returns {JSX.Element} - A colored dot element.
 */
const StatusDot = ({ status }) => {
    // Get the corresponding color for the status
    const statusColor = StatusColors[getStatus(status)];

    // Render a span element with a colored dot
    // The style prop sets the background color of the dot
    return (
        <span
            className="status-dot"
            style={{ backgroundColor: statusColor }}
        ></span>
    );
};

export { Status, StatusDot, getStatus };
