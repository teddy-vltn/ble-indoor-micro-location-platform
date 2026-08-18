import React, { useState, useEffect, useRef } from 'react';
import { StatusDot } from '../statusDot/StatusDot';
import './customdropdown.css';
import { useTranslation } from 'react-i18next';

/**
 * CustomDropdown component
 * Renders a dropdown with options and a base option of 'all'
 * @param {function} onChange - function to handle option selection
 * @param {array} options - array of objects with value and label properties
 * @param {boolean} reset - boolean to reset dropdown to base option
 */
const CustomDropdown = ({ onChange, options, reset }) => {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false); // State to track dropdown open/close
  const [selectedOption, setSelectedOption] = useState(t('all')); // State to track selected option label
  const [selectedOptionValue, setSelectedOptionValue] = useState(''); // State to track selected option value
  const dropdownRef = useRef(null); // Reference to the dropdown element

  /**
   * Adds a base option of 'all' to the options array
   * @param {array} options - array of objects with value and label properties
   * @returns {array} - array of objects with value and label properties, including the base option
   */
  const addBaseOption = (options) => {
    return [{ value: '', label: t('all') }, ...options];
  };

  const dropdownOptions = addBaseOption(options); // Array of options with base option

  // Event listener to handle clicking outside the dropdown
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, []);

  // Reset dropdown to base value when the reset prop changes
  useEffect(() => {
    setSelectedOption(t('all'));
    setSelectedOptionValue('');
  }, [reset, t]);

  /**
   * Handles click event on an option
   * @param {string} optionValue - value of the selected option
   */
  const handleOptionClick = (optionValue) => {
    const selectedOption = dropdownOptions.find((option) => option.value === optionValue);
    if (selectedOption) {
      onChange(optionValue);
      setIsOpen(false);
      setSelectedOption(selectedOption.label);
      setSelectedOptionValue(optionValue);
    }
  };

  return (
    // Render the dropdown component
    <div className="custom-dropdown" ref={dropdownRef}>
      {/* Render the selected option */}
      <div className="custom-dropdown-option" onClick={() => setIsOpen(!isOpen)}>
        {selectedOption !== t('all') && <StatusDot status={selectedOptionValue} />}
        <span>{selectedOption}</span>
      </div>
      {/* Render the options list */}
      {isOpen && (
        <div className="custom-dropdown-options">
          {dropdownOptions.map((option) => (
            <div
              key={option.value}
              className="custom-dropdown-selected"
              onClick={() => handleOptionClick(option.value)}
            >
              {option.label !== t('all') && <StatusDot status={option.value} />}
              {option.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CustomDropdown;
