import React, { createContext, useContext, useState } from 'react';
import { apiRequest } from '../apiHelper';
import { StatusContext } from './StatusProvider';

export const InventoryContext = createContext();

const InventoryProvider = ({ children }) => {
    const [loading, setLoading] = useState(false);
    const { refresh, inventory, hostsNames } = useContext(StatusContext);

    const inventoryActions = {
        postHost: ({ newRaspberry }) => apiRequest({ url: `http://${window.location.hostname}:5001/inventory/hosts`, method: 'POST', data: newRaspberry, onSuccess: refresh, onFinally: () => setLoading(false) }),
        deleteHost: ({ raspberryToEdit }) => apiRequest({ url: `http://${window.location.hostname}:5001/inventory/hosts/${raspberryToEdit._id}`, method: 'DELETE', onSuccess: refresh, onFinally: () => setLoading(false) }),
        putHost: ({ newRaspberry, raspberryToEdit }) => apiRequest({ url: `http://${window.location.hostname}:5001/inventory/hosts/${raspberryToEdit._id}`, method: 'PUT', data: newRaspberry, onSuccess: refresh, onFinally: () => setLoading(false) })
    };

    return (
        <InventoryContext.Provider value={{ inventory, hostsNames, loading, ...inventoryActions }}>
            {children}
        </InventoryContext.Provider>
    );
};

export default InventoryProvider;
