import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

/**
 * Component that displays the time ago from a given timestamp.
 * It updates the displayed time every second and when the language changes.
 * @param {number} timestamp - The timestamp in seconds.
 * @returns {JSX.Element} - The JSX element displaying the time ago.
 */
const TimeAgo = ({ timestamp }) => {
  // Get translation function and i18n instance
  const { t, i18n } = useTranslation();
  // State to store the time ago string
  const [timeAgo, setTimeAgo] = useState('');

  // Effect that updates the time ago string every second and when the language changes
  useEffect(() => {
    /**
     * Function that updates the time ago string.
     */
    const updateTimeAgo = () => {
      setTimeAgo(formatTimeAgo(timestamp));
    };

    // Update the time ago string initially and start the interval
    updateTimeAgo();
    const interval = setInterval(updateTimeAgo, 1000);

    // Add event listener to update the time ago string when the language changes
    i18n.on('languageChanged', updateTimeAgo);

    // Cleanup function to clear the interval and remove the event listener
    return () => {
      clearInterval(interval);
      i18n.off('languageChanged', updateTimeAgo);
    };
  }, [timestamp, i18n]);

  /**
   * Function that formats the time ago string based on the given timestamp.
   * @param {number} timestamp - The timestamp in seconds.
   * @returns {string} - The formatted time ago string.
   */
  const formatTimeAgo = (timestamp) => {
    // Get the current date and the past date
    const now = new Date();
    const past = new Date(timestamp * 1000);
    // Calculate the time difference in milliseconds
    const diff = now - past;

    // Calculate the time differences in different units
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    const months = Math.floor(days / 30);
    const years = Math.floor(days / 365);

    // Return the formatted time ago string based on the time differences
    if (years > 0) return t('waiting');
    if (months > 0) return t('months-ago', [months]);
    if (days > 0) return t('days-ago', [days, days > 1 ? 's' : '']);
    if (hours > 0) return t('hours-ago', [hours, hours > 1 ? 's' : '']);
    if (minutes > 0) return t('minutes-ago', [minutes, minutes > 1 ? 's' : '']);
    return t('seconds-ago', [seconds, seconds > 1 ? 's' : '']);
  };

  // Return the JSX element displaying the time ago string
  return <span>{timeAgo}</span>;
};

export default TimeAgo;
