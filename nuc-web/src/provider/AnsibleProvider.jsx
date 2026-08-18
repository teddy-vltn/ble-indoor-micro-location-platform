import React, { createContext, useState, useContext } from 'react';
import { apiRequest } from '../apiHelper';
import { StatusContext } from './StatusProvider';

export const AnsibleContext = createContext();

const AnsibleProvider = ({ children }) => {
    const [loading, setLoading] = useState(false);
    const { refresh, ansibleLogs, inventory } = useContext(StatusContext);

    const handleInventoryActivateBoolChange = (deviceId, bool) => {
        setLoading(true);
        apiRequest({
            url: `http://${window.location.hostname}:5001/inventory/hosts/${deviceId}`,
            method: 'PUT',
            data: { active: bool },
            onSuccess: refresh,
            onFinally: () => setLoading(false)
        });
    };

    return (
        <AnsibleContext.Provider value={{ ansibleLogs, inventory, loading, handleInventoryActivateBoolChange }}>
            {children}
        </AnsibleContext.Provider>
    );
};

export default AnsibleProvider;
