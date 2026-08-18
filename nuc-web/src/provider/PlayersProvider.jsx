import React, { createContext, useContext } from 'react';
import env from 'react-dotenv';
import { apiRequest } from '../apiHelper';
import { StatusContext } from './StatusProvider';

export const PlayersContext = createContext();

const PlayersProvider = ({ children }) => {
    const { refresh, activeProfile, graph, activeSession } = useContext(StatusContext);

    const playerActions = {
        setFinishPlayerState: (_id) => apiRequest({ url: `http://${window.location.hostname}:5001/players/${_id}/finish`, method: 'PUT', onSuccess: refresh }),
        deletePlayer: (_id) => apiRequest({ url: `http://${window.location.hostname}:5001/players/${_id}`, method: 'DELETE', onSuccess: refresh }),
        deleteAllPlayers: () => apiRequest({ url: `http://${window.location.hostname}:5001/players/wipe-players`, method: 'DELETE', onSuccess: refresh })
    };

    const getActiveProfileSvgMap = () => {
        return activeProfile ? activeProfile.graph_svg : null;
    }

    return (
        <PlayersContext.Provider value={{ ...playerActions, graph, activeProfile, activeSession, getActiveProfileSvgMap }}>
            {children}
        </PlayersContext.Provider>
    );
};

export default PlayersProvider;
