import React, { useState, useEffect, useCallback } from 'react';
import TableInfo from './TableInfo';
import IOSSwitch from '../iosswitch';
import { StatusDot, getStatus } from '../statusDot/StatusDot';
import ConnectionStatus from '../connectionStatus/ConnectionStatus';
import { DeleteForever } from '@mui/icons-material';
import TimeAgo from './TimeAgo';
import TableFilter from './TableFilter';

const TableComposite = (props) => {
  const [rows, setRows] = useState([]);
  const [filteredRows, setFilteredRows] = useState([]);
  const [filters, setFilters] = useState({});

  const handleSelectChange = useCallback(({ row, field, newValue }, onChange) => {
    const updatedRows = rows.map(r =>
      r.id === row.id ? { ...r, [field]: newValue } : r
    );
    setRows(updatedRows);
    setFilteredRows(applyFilters(updatedRows, filters));
    if (onChange) onChange({ row, field, newValue });
  }, [rows, filters]);

  const handleButtonChange = useCallback(({ row, field, newValue }, onClick) => {
    if (onClick) onClick({ row, field, newValue });
  }, []);

  const handleResetRow = useCallback((row, onReset) => {
    const updatedRows = rows.map(r => (r.id === row.id ? row : r));
    setRows(updatedRows);
    setFilteredRows(applyFilters(updatedRows, filters));
    if (onReset) onReset(row);
  }, [rows, filters]);

  const handleSwitchChange = useCallback(({ row, field, newValue }, onBooleanChange) => {
    if (onBooleanChange) onBooleanChange({ row, field, newValue });
  }, []);

  const callbackFilteredRows = useCallback((rows) => {
    if (props.onTransformedRows) {
      props.onTransformedRows(rows);
    }
  }, [props]);

  const applyFilters = useCallback((rows, filters) => {
    const parseFilterValue = (filterValue) => {
      const complexPattern = /^(.*?)%((?:\d+|\d+-\d+)(?:,(?:\d+|\d+-\d+))*)%$/;
      const textPattern = /^%(.*?)(?:,(.*?))?%$/;
      const complexMatch = filterValue.match(complexPattern);
      const textMatch = filterValue.match(textPattern);
  
      if (complexMatch) {
        const prefix = complexMatch[1];
        const ranges = complexMatch[2].split(',').map(part => {
          if (part.includes('-')) {
            const [start, end] = part.split('-').map(Number);
            return { type: 'range', start, end };
          }
          return { type: 'single', value: Number(part) };
        });
        return { type: 'complex', prefix, ranges };
      } else if (textMatch) {
        const texts = textMatch.slice(1).filter(Boolean); // Remove empty values and nulls
        return { type: 'textList', texts };
      }
      return { type: 'normal', value: filterValue };
    };
  
    const matchesFilter = (value, filter) => {
      if (filter.type === 'complex') {
        const checkNumberInRange = (num, ranges) => {
          return ranges.some(range => {
            if (range.type === 'range') {
              return num >= range.start && num <= range.end;
            }
            if (range.type === 'single') {
              return num === range.value;
            }
            return false;
          });
        };
  
        if (typeof value === 'string') {
          const numericPart = parseInt(value.replace(filter.prefix, ''), 10);
          if (isNaN(numericPart)) return false;
          return checkNumberInRange(numericPart, filter.ranges);
        }
  
        if (typeof value === 'number') {
          return checkNumberInRange(value, filter.ranges);
        }
        return false;
      }
  
      if (filter.type === 'textList') {
        if (typeof value === 'string') {
          return filter.texts.some(text => value.toLowerCase().includes(text.toLowerCase()));
        }
        return false;
      }
  
      if (filter.type === 'normal') {
        if (typeof value === 'number') {
          return value.toString().includes(filter.value);
        }
        if (typeof value === 'string') {
          return value.toLowerCase().includes(filter.value.toLowerCase());
        }
      }
  
      if (value && value.props && value.props.defaultChecked !== undefined) {
        return value.props.defaultChecked.toString() === filter.value;
      }
      if (value && value.type) {
        if (value.type.name === "StatusDot") {
          const rowStatus = getStatus(value.props.status);
          const filterStatus = getStatus(filter.value);
          return rowStatus === filterStatus;
        }
        if (value.type.name === "ConnectionStatus") {
          return value.props.statuses.some(status => getStatus(status) === getStatus(filter.value));
        }
      }
      return true;
    };
  
    const filteredRows = rows.filter(row => {
      if (!Object.keys(filters).length) return true;
      return Object.keys(filters).every(field => {
        const filterValue = filters[field];
        if (!filterValue) return true;

        if (typeof filterValue === 'boolean') {
          return row[field] === filterValue;
        }

        const parsedFilter = parseFilterValue(filterValue);

        return matchesFilter(row[field], parsedFilter);
      });
    });
  
    callbackFilteredRows(filteredRows);
    return filteredRows;
  
  }, []);  
  
  const transformRows = useCallback((rows) => {
    const { columnConfigs } = props;
    if (!rows) return [];

    return Object.values(rows).map(row => {
      const transformedRow = { ...row };

      columnConfigs.forEach(config => {
        const value = getFieldValue(row, config.field);

        switch (config.type) {
          case 'list':
            transformedRow[config.field] = value.join(', ');
            break;
          case 'select':
            transformedRow[config.field] = (
              <div className="lineButton">
                <select
                  value={value}
                  onChange={event => handleSelectChange({ row, field: config.field, newValue: event.target.value }, config.onChange)}
                >
                  {config.options.map(option => (
                    <option key={option.name} value={option.name}>{option.name}</option>
                  ))}
                  <option value={value}>{value}</option>
                </select>
                {value && (
                  <button onClick={() => handleResetRow(row, config.onReset)} className="resetButton">
                    <DeleteForever />
                  </button>
                )}
              </div>
            );
            break;
          case 'bool':
            transformedRow[config.field] = (
              <IOSSwitch
                checked={value}
                defaultChecked={value}
                onChange={event => handleSwitchChange({ row, field: config.field, newValue: event.target.checked }, config.onBooleanChange)}
                color="primary"
              />
            );
            break;
          case 'bool.button':
            transformedRow[config.field] = !value && (
              <button onClick={() => handleButtonChange({ row, field: config.field, newValue: true }, config.onClick)}>
                {config.text}
              </button>
            );
            break;
          case 'number':
            transformedRow[config.field] = formatNumber(value);
            break;
          case 'dot.bool':
          case 'dot':
            if (typeof value === 'boolean') {
              transformedRow[config.field] = <StatusDot status={value} />;
            } else {
              transformedRow[config.field] = <StatusDot status="unknown" />;
            }
            break;
          case 'dot.list':
            transformedRow[config.field] = <ConnectionStatus statuses={value} />;
            break;
          case 'date.utc':
            transformedRow[config.field] = new Date(value * 1000).toLocaleString();
            break;
          case 'date.wasago':
            transformedRow[config.field] = <TimeAgo timestamp={value} />;
            break;
          default:
            transformedRow[config.field] = config.render ? config.render(value, row) : value;
            break;
        }
      });

      return transformedRow;
    });
  }, [handleSelectChange, handleResetRow, handleSwitchChange, handleButtonChange, props]);

  const getFieldValue = (row, field) => {
    return field.split('.').reduce((acc, part) => acc?.[part] ?? '', row);
  };

  useEffect(() => {
    const transformedRows = transformRows(props.rows);

    setRows(transformedRows);
    setFilteredRows(applyFilters(transformedRows, filters));
  

  }, [props.rows, props.rows.length, props.rows[0], filters]);

  const formatNumber = (value) => new Intl.NumberFormat().format(value);

  const { columnConfigs, actions } = props;

  return (
    <div>
      <TableFilter filters={filters} setFilters={setFilters} columnConfigs={columnConfigs} />
      <TableInfo
        rows={filteredRows}
        columns={columnConfigs}
        actions={actions}
      />
    </div>
  );
};

export default TableComposite;
