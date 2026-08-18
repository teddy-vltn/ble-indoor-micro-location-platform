import React, { createContext, useState, useEffect, useCallback, act } from 'react';
import env from 'react-dotenv';
import { apiRequest } from '../apiHelper';

export const StatusContext = createContext();

const StatusProvider = ({ children }) => {
    const [loading, setLoading] = useState(false);
    const [lastRefresh, setLastRefresh] = useState(new Date().toLocaleTimeString());
    const [activeProfile, setActiveProfile] = useState({});
    const [allProfiles, setAllProfiles] = useState([]);
    const [activeSession, setActiveSession] = useState(null);
    const [inventory, setInventory] = useState({});
    const [ansibleLogs, setAnsibleLogs] = useState({});
    const [graph, setGraph] = useState({ nodes: [], edges: [] });
    const [hostsNames, setHostsNames] = useState([]);

    const refresh = useCallback(() => {
        setLastRefresh(new Date().valueOf());
        fetchStatus();
    }, []);

    const fetchStatus = useCallback(() => {
        setLoading(true);
        console.log("Fetching status..." + `http://${window.location.hostname}:5001/status`);
        apiRequest({
            url: `http://${window.location.hostname}:5001/status`,
            method: 'GET',
            onSuccess: (response) => {
                const data = response.data;
                setActiveProfile(data.active_profile);
                setAllProfiles(data.all_profiles);
                setActiveSession(data.active_session);
                setInventory(data.inventory);
                setAnsibleLogs(data.ansible);
                setGraph(data.graph[0]);
                setHostsNames(data.hosts_names);
            },
            onFinally: () => {
                setLastRefresh(new Date().toLocaleTimeString());
                setLoading(false);
            }
        });
    }, []);

    useEffect(() => {
        fetchStatus();
        const interval = setInterval(fetchStatus, 5000);
        return () => clearInterval(interval);
    }, [fetchStatus]);

    const profileActions = {
        changeProfile: ({ _id }) => apiRequest({ url: `http://${window.location.hostname}:5001/profiles/${_id}`, method: 'PATCH', onSuccess: fetchStatus }),
        createProfile: ({ new_profile, graph_svg }) => apiRequest({ url: `http://${window.location.hostname}:5001/profiles`, method: 'POST', data: { name: new_profile, graph_svg }, onSuccess: fetchStatus }),
        deleteProfile: ({ _id }) => apiRequest({ url: `http://${window.location.hostname}:5001/profiles/${_id}`, method: 'DELETE', onSuccess: fetchStatus }),
        updateProfile: ({ _id, new_profile, graph_svg }) => apiRequest({ url: `http://${window.location.hostname}:5001/profiles/${_id}`, method: 'PUT', data: { new_name: new_profile, graph_svg }, onSuccess: fetchStatus }),
        duplicateProfile: ({ _id }) => apiRequest({ url: `http://${window.location.hostname}:5001/profiles/${_id}/duplicate`, method: 'POST', onSuccess: fetchStatus }),
        startNewSessionForProfile: ({ name = "no-name" }) => {
            const active_profile_id = activeProfile._id;
            apiRequest({ url: `http://${window.location.hostname}:5001/profiles/${active_profile_id}/start-session/${name}`, method: 'POST', onSuccess: fetchStatus });
        },
        stopSessionForProfile: () => apiRequest({ url: `http://${window.location.hostname}:5001/profiles/finish-active-session`, method: 'PUT', onSuccess: fetchStatus })
    };

    const getActiveSession = () => {
        return activeSession ? activeSession : null
    }

    return (
        <StatusContext.Provider value={{
            activeProfile, activeSession, allProfiles, ...profileActions, getActiveSession,
            lastRefresh, refresh, inventory, ansibleLogs, graph, hostsNames
        }}>
            {children}
        </StatusContext.Provider>
    );
};

export default StatusProvider;
