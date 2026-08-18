import React, { createContext, useState, useEffect } from 'react';
import io from 'socket.io-client';
import env from 'react-dotenv';

// Create the context
export const TerminalContext = createContext();

const TerminalProvider = ({ children }) => {
    const [terminalOutput, setTerminalOutput] = useState('');
    const socket = io(`http://${window.location.hostname}:5001/bash`, { transports: ['websocket'] });
    const [scripts, setScripts] = useState(['start', 'stop', 'update-rasplog'])

    useEffect(() => {
        // Set up WebSocket connection
        socket.on('connect', () => {
            console.log('Connected to WebSocket server');
        });

        // Receive data and update terminal output
        socket.on('bash_output', data => {
            setTerminalOutput(prev => prev + data.data);
        });

        socket.on('scripts_list', data => {
            setScripts(data.scripts);
        });
    }, []);

    const clearTerminalOutput = () => {
        setTerminalOutput(''); // Clear local output
    };

    const getTerminalOutput = () => {
        return terminalOutput; // Accessor for the terminal output
    };

    const run_script = (script) => {
        socket.emit('start_script', { "script_name": script });
        clearTerminalOutput();
    };

    // Provide the context
    return (
        <TerminalContext.Provider value={{
            scripts,
            terminalOutput,
            clearTerminalOutput,
            getTerminalOutput,
            run_script
        }}>
            {children}
        </TerminalContext.Provider>
    );
};

export default TerminalProvider;
