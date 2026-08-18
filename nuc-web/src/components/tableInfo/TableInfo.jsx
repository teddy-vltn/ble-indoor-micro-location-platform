import React, { useEffect, useState } from 'react';
import './tableinfo.css';
import { useTranslation } from 'react-i18next';

/**
 * TableInfo component displays a table with data and optional actions.
 *
 * @param {Object} props - The properties object.
 * @param {Array} props.rows - The data rows to display.
 * @param {Array} props.columns - The table columns.
 * @param {Array} props.actions - The actions to display for each row.
 * @returns {JSX.Element} - The rendered table.
 */
export default function TableInfo({ rows, columns, actions }) {
    // Translation hook
    const { t } = useTranslation();
    // State for table rows
    const [tableRows, setTableRows] = useState([]);
    // State for table sorting configuration
    const [sortConfig, setSortConfig] = useState({ key: '', direction: '' });

    /**
     * Updates table rows based on the data and sorting configuration.
     */
    useEffect(() => {
        setTableRows(transformRows(rows, actions, sortConfig));
    }, [rows, sortConfig]);

    /**
     * Transforms the rows data to include actions and sorts them if necessary.
     *
     * @param {Array} items - The data rows.
     * @param {Array} actions - The actions to display for each row.
     * @param {Object} sortConfig - The sorting configuration.
     * @returns {Array} - The transformed rows.
     */
    const transformRows = (items, actions, sortConfig) => {
        let updatedRows = items;
        if (actions) {
            updatedRows = items.map(row => ({
                ...row,
                actions: actions.map((action, index) => ({
                    icon: action.icon,
                    onClick: () => action.action(row),
                    key: index
                }))
            }));
        }

        if (sortConfig.key) {
            updatedRows = sortRows(updatedRows, sortConfig);
        }

        return updatedRows;
    };

    /**
     * Sorts the rows based on the specified column and direction.
     *
     * @param {Array} rows - The rows to sort.
     * @param {Object} sortConfig - The sorting configuration.
     * @returns {Array} - The sorted rows.
     */
    const sortRows = (rows, sortConfig) => {
        return [...rows].sort((a, b) => {
            const aValue = a[sortConfig.key];
            const bValue = b[sortConfig.key];

            // Parse the value into parts for sorting
            const parseValue = (value) => {
                return value
                    .toString()
                    .split(/(\d+)/)
                    .map((part) => (isNaN(part) ? part : Number(part)));
            };

            const aParts = parseValue(aValue);
            const bParts = parseValue(bValue);

            // Compare the parts until a difference is found
            for (let i = 0; i < Math.max(aParts.length, bParts.length); i++) {
                if (aParts[i] < bParts[i]) {
                    return sortConfig.direction === 'ascending' ? -1 : 1;
                }
                if (aParts[i] > bParts[i]) {
                    return sortConfig.direction === 'ascending' ? 1 : -1;
                }
            }

            return 0;
        });
    };

    /**
     * Handles the sorting of the table by setting the new sorting configuration.
     *
     * @param {string} key - The column to sort by.
     */
    const handleSort = (key) => {
        let direction = 'ascending';
        if (sortConfig.key === key && sortConfig.direction === 'ascending') {
            direction = 'descending';
        }
        setSortConfig({ key, direction });
    };

    // Render the table
    return (
        <div className="tableInfo">
            <table className="table">
                <thead>
                    <tr>
                        {/* Render table columns */}
                        {columns.filter(column => column.field !== '_id').map((column) => (
                            <th key={column.field} onClick={() => handleSort(column.field)}>
                                {column.headerName}
                                {/* Show sorting arrow if column is sorted */}
                                {sortConfig.key === column.field && (
                                    sortConfig.direction === 'ascending' ? ' ▲' : ' ▼'
                                )}
                            </th>
                        ))}
                        {/* Render actions column if actions provided */}
                        {actions && <th>{t('actions')}</th>}
                    </tr>
                </thead>
                <tbody>
                    {/* Render table rows */}
                    {tableRows.map((row, rowIndex) => (
                        <tr key={rowIndex}>
                            {columns.filter(column => column.field !== '_id').map((column) => (
                                <td key={`${column.field}-${rowIndex}`}>{row[column.field]}</td>
                            ))}
                            {/* Render actions for each row */}
                            {row.actions && (
                                <td>
                                    {row.actions.map(action => (
                                        <button key={action.key} onClick={action.onClick} className="actionButton">
                                            {action.icon}
                                        </button>
                                    ))}
                                </td>
                            )}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
