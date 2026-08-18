import React, { useState, useEffect } from 'react';
import './tablefilter.css';
import CustomDropdown from './CustomDropdown';
import { useTranslation } from 'react-i18next';

import moment from 'moment';
import { TimePicker } from '@mui/x-date-pickers-pro';

/**
 * TableFilter component
 *
 * @param {Object} props - The component props
 * @param {Object} props.filters - The current filters object
 * @param {Function} props.setFilters - The function to set the filters
 * @param {Array} props.columnConfigs - The column configs array
 *
 * @returns {JSX.Element} - The rendered TableFilter component
 */
const TableFilter = ({ filters, setFilters, columnConfigs }) => {
  // Get the translation function from the React i18next module
  const { t } = useTranslation();

  // State hooks
  const [localFilters, setLocalFilters] = useState(filters);
  const [reset, setReset] = useState(false);

  // Effect hook to update local filters when filters prop changes
  useEffect(() => {
    setLocalFilters(filters);
  }, [filters]);

  /**
   * Handles the filter change event
   *
   * @param {string} field - The field name
   * @param {string|boolean} value - The new value
   * @param {Function} onChange - The onChange function for the field
   */
  const handleFilterChange = (field, value, onChange) => {
    const newFilters = { ...localFilters, [field]: value };
    setLocalFilters(newFilters);
    setFilters(newFilters);
    if (onChange) {
      onChange(value);
    }
  };

  /**
   * Resets the filters
   */
  const resetFilters = () => {
    const resetFilters = {};
    columnConfigs.forEach((column) => {
      resetFilters[column.field] = '';
    });
    setLocalFilters(resetFilters);
    setFilters(resetFilters);
    setReset(prevReset => !prevReset);
  };

  /**
   * Renders the filter input based on the column type
   *
   * @param {Object} column - The column config object
   * @returns {JSX.Element|null} - The rendered filter input or null
   */
  const renderFilterInput = (column) => {
    if (column.filter === false) return null;

    switch (column.type) {
      case 'text':
      case 'list':
        return (
          <input
            type="text"
            value={localFilters[column.field] || ''}
            onChange={(e) => handleFilterChange(column.field, e.target.value, column.onChange)}
          />
        );
      case 'bool':
        return (
          <select
            value={localFilters[column.field] || ''}
            onChange={(e) => handleFilterChange(column.field, e.target.value, column.onChange)}
          >
            <option value="">{t('all')}</option>
            <option value="true">{t('yes')}</option>
            <option value="false">{t('no')}</option>
          </select>
        );
      case 'dot':
      case 'dot.bool':
      case 'dot.list':
        return (
          <CustomDropdown
            onChange={(value) => handleFilterChange(column.field, value, column.onChange)}
            options={column.type === 'dot.bool' ?
              [
                { value: true, label: t('yes') },
                { value: false, label: t('no') },
              ] :
              [
                { value: 'online', label: t('online') },
                { value: 'offline', label: t('offline') },
                { value: 'unknown', label: t('uncertain') },
              ]}
            reset={reset}
          />
        );
      case 'select':
        return (
          <select
            value={localFilters[column.field] || ''}
            onChange={(e) => handleFilterChange(column.field, e.target.value, column.onChange)}
            disabled={column.disabled}
          >
            {column.options.map((option, index) => (
              <option key={index} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        );
      case 'hour':
        const isDisabled = column.disabled || column.baseValue === null
        const maxValue = column.maxValue < column.baseValue ? moment() : moment(column.maxValue * 1000)
        const minValue = column.minValue > column.baseValue ? moment() : moment(column.minValue * 1000)
        const baseValue = column.baseValue < column.minValue ? moment() : moment(column.baseValue * 1000)

        return (
          <TimePicker
            maxTime={maxValue}
            minTime={minValue}
            value={baseValue}
            ampm={false}
            skipDisabled={true}
            disabled={isDisabled}
            timeSteps={{ minutes: 1, seconds: 1 }}
            views={['hours', 'minutes', 'seconds']}
            onChange={(value) => handleFilterChange(column.field, value, column.onChange)}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="section">
      <div className="table-filters-wrapper">
        <div className="table-filters">
          {columnConfigs.map((column) => {
            const filterInput = renderFilterInput(column);
            return filterInput ? (
              <div key={column.field} className="filter">
                <label>{column.headerName}</label> 
                {filterInput}
              </div>
            ) : null;
          })}
        </div>
        <button onClick={resetFilters} className="reset-filters-button greyButton">
          {t('reset-filters')}
        </button>
      </div>
    </div>
  );
};

export default TableFilter;
