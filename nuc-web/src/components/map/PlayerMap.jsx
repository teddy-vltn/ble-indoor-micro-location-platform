import './playermap.css';
import React, { useEffect, useState, useCallback } from 'react';
import MapBasic from './MapBasic';
import { Slider } from '@mui/material';
import { useTranslation } from 'react-i18next';
import Mermaid from '../../Mermaid';

// suppress warnings
/* eslint-disable no-unused-vars */
const EventGanttChart = ({ player, id_device }) => {
    const events = [
        { id: 656, description: 'QRCodeEquipeScanne', start: '13:29:24', end: '13:29:25', equipe_id: 151 },
        { id: 657, description: 'NombresDeJoueurs', start: '13:30:00', end: '13:30:01', equipe_id: 151 },
        { id: 658, description: 'QRCodeEquipeScanne', start: '13:31:00', end: '13:31:01', equipe_id: 152 },
        { id: 659, description: 'NombresDeJoueurs', start: '13:31:37', end: '13:31:38', equipe_id: 152 },
        { id: 660, description: 'QRCodeEquipeScanne', start: '13:32:39', end: '13:32:40', equipe_id: 153 },
        { id: 661, description: 'NombresDeJoueurs', start: '13:32:44', end: '13:32:45', equipe_id: 153 },
        { id: 662, description: 'QRCodeEquipeScanne', start: '13:33:55', end: '13:33:56', equipe_id: 154 },
        { id: 663, description: 'NombresDeJoueurs', start: '13:34:03', end: '13:34:04', equipe_id: 154 },
        { id: 664, description: 'EquipeEnAttentePassword', start: '13:38:28', end: '13:38:29', equipe_id: 151 },
        { id: 665, description: 'EquipeEnAttentePassword', start: '13:40:41', end: '13:40:42', equipe_id: 153 },
        { id: 666, description: 'EquipeEnAttentePassword', start: '13:41:33', end: '13:41:34', equipe_id: 152 },
        { id: 667, description: 'EquipeEnAttentePassword', start: '13:41:38', end: '13:41:39', equipe_id: 154 },
        { id: 668, description: 'QRCodeEspaceScanne', start: '13:42:43', end: '13:42:44', equipe_id: 153 },
        { id: 669, description: 'QRCodeEspaceScanne', start: '13:43:42', end: '13:43:43', equipe_id: 152 },
        { id: 670, description: 'QRCodeEspaceScanne', start: '13:44:52', end: '13:44:53', equipe_id: 154 },
        { id: 671, description: 'QRCodeEspaceScanne', start: '13:45:54', end: '13:45:55', equipe_id: 151 },
        { id: 672, description: 'FinBureauTheodore', start: '13:46:47', end: '13:46:48', equipe_id: 153 },
        { id: 673, description: 'FinBureauTheodore', start: '13:47:37', end: '13:47:38', equipe_id: 152 },
        { id: 674, description: 'FinBureauTheodore', start: '13:47:50', end: '13:47:51', equipe_id: 154 },
        { id: 675, description: 'FinBureauTheodore', start: '13:47:53', end: '13:47:54', equipe_id: 151 },
        { id: 676, description: 'FinBibliotheque', start: '13:48:24', end: '13:48:25', equipe_id: 153 },
        { id: 677, description: 'FinQuizEquipe', start: '13:50:16', end: '13:50:17', equipe_id: 153 },
        { id: 678, description: 'FinBibliotheque', start: '13:51:26', end: '13:51:27', equipe_id: 152 },
        { id: 679, description: 'FinBibliotheque', start: '13:52:24', end: '13:52:25', equipe_id: 151 },
        { id: 680, description: 'FinQuizEquipe', start: '13:54:54', end: '13:54:55', equipe_id: 151 },
        { id: 681, description: 'FinBibliotheque', start: '13:55:08', end: '13:55:09', equipe_id: 154 },
        { id: 682, description: 'FinQuizEquipe', start: '13:56:43', end: '13:56:44', equipe_id: 152 },
        { id: 683, description: 'FinQuizEquipe', start: '13:57:23', end: '13:57:24', equipe_id: 154 },
    ];
    

    const filteredEvents = events.filter(event => event.equipe_id === id_device);

    // regenerate the end date for each event based on the start date of the next event for the same equipe
    for (let i = 0; i < filteredEvents.length - 1; i++) {
        if (filteredEvents[i].description === "NombresDeJoueurs") {
            filteredEvents[i].end = filteredEvents[i].start || filteredEvents[i].end;
            continue
        }


        filteredEvents[i].end = filteredEvents[i + 1].start || filteredEvents[i].end;
    }

    const chart = `
        gantt
            dateFormat  HH:mm:ss
            axisFormat  %H:%M:%S
            title       Event Timeline for Equipe ${id_device}
            section    
            
            ${filteredEvents.map(event => `${event.description} :a${event.id}, ${event.start}, ${event.end}`).join('\n')}
    `;

    return (
        <div>
            {player && (
                <Mermaid chart={chart} />
            )}
        </div>
    );
};

/**
 * Renders a player map component with a map, players, and controls.
 *
 * @param {Object} props - The component props.
 * @param {Object[]} props.players - The players data.
 * @param {Object} props.graph - The graph data.
 * @param {Object} props.player - The selected player.
 * @param {string} props.mapImageName - The name of the map image.
 * @param {number} props.startDate - The start date of the time range.
 * @param {number} props.endDate - The end date of the time range.
 * @return {JSX.Element} The player map component.
 */
const PlayerMap = ({ players, graph, player, mapImageName, startDate, endDate }) => {
    const { t } = useTranslation();
    const [activePlayers, setActivePlayers] = useState([]);
    const [playersNodes, setPlayersNodes] = useState([]);
    const [edges, setEdges] = useState([]);
    const [points, setPoints] = useState([]);
    const [allTimes, setAllTimes] = useState([]);
    const [filteredTimes, setFilteredTimes] = useState([]);
    const [step, setStep] = useState(0);
    const [playingState, setPlayingState] = useState(false);
    const [playingSpeed, setPlayingSpeed] = useState(1);

    const [visitedNodes, setVisitedNodes] = useState([]);
    const [missingNodes, setMissingNodes] = useState(new Set());

    useEffect(() => {
        setEdges(graph.edges || []);
        setPoints(graph.nodes || []);
    }, [graph]);

    /**
     * Calculates the position around a circle given the center coordinates, radius, index and total number of positions.
     *
     * @param {number} centerX - The x-coordinate of the circle's center.
     * @param {number} centerY - The y-coordinate of the circle's center.
     * @param {number} radius - The radius of the circle.
     * @param {number} index - The index of the position.
     * @param {number} total - The total number of positions.
     * @return {Object} - The x and y coordinates of the position around the circle.
     */
    const getPositionAroundCircle = useCallback((centerX, centerY, radius, index, total) => {
        const angle = (index / total) * 2 * Math.PI;
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);
        return { x, y };
    }, []);

    /**
     * Transforms the players nodes based on the active players and the current time.
     *
     * @param {Object[]} points - The points of the graph.
     * @param {number} currentTime - The current time.
     * @return {Object[]} The transformed players nodes.
     */
    const transformPlayersNodes = useCallback((points, currentTime) => {
        /**
         * The players nodes.
         * @type {Object[]}
         */
        const playersNodes = [];

        /**
         * The players grouped by node.
         * @type {Object.<string, Object[]>}
         */
        const playersByNode = {};

        // Reset visited nodes
        setVisitedNodes([]);

        // Iterate over the active players
        Object.keys(activePlayers).forEach(playerId => {
            const player = activePlayers[playerId];
            const playerCreatedAt = player.started_at;

            // Get the movement keys sorted by time
            const movementKeys = Object.keys(player.temporal_sequence_visited || {})
                .sort((a, b) => a - b);

            // Find the last key that is greater than or equal to the current time
            const lastKey = movementKeys.find(key => key >= currentTime) ||
                movementKeys[movementKeys.length - 1];

            // Get the last visited node
            const lastVisited = player.temporal_sequence_visited[lastKey]?.to?.slice(-1)[0];

            // If the player has been created before the current time and has visited a node
            if (playerCreatedAt <= parseFloat(currentTime) && lastVisited) {
                // If the node does not have players, create an empty array
                if (!playersByNode[lastVisited]) {
                    playersByNode[lastVisited] = [];
                }

                // Add the player to the array of players for the node
                playersByNode[lastVisited].push(player);
            }
        });

        // Iterate over the players grouped by node
        for (const [nodeId, players] of Object.entries(playersByNode)) {
            // Find the point of the node
            const nodePoint = points.find(point => point.id.toString() === nodeId.toString());

            // If the node point exists
            if (nodePoint) {
                // Calculate the radius for the players' positions
                const radius = 30;

                // Add the node to the visited nodes
                setVisitedNodes(prev => [...prev, nodeId]);

                // Iterate over the players
                players.forEach((player, index) => {
                    // Calculate the position of the player around the node
                    const position = getPositionAroundCircle(nodePoint.x, nodePoint.y, radius, index, players.length);

                    // Add the player node to the players nodes
                    playersNodes.push({
                        id: player.id_minor,
                        x: position.x,
                        y: position.y,
                        has_finished: player.has_finished
                    });
                });
            } else {
                // If the node does not exist, add it to the missing nodes set
                if (nodeId !== "0") setMissingNodes(prev => new Set(prev.add(nodeId)));
            }
        }

        // Return the transformed players nodes
        return playersNodes;
    }, [activePlayers, getPositionAroundCircle]);

    const transformTemporalData = useCallback(() => {
        const times = new Set();

        Object.values(activePlayers).forEach(player => {
            Object.keys(player.temporal_sequence_visited || {}).forEach(time => {
                times.add(time);
            });
        });

        const sortedTimes = Array.from(times).sort((a, b) => a - b);
        setAllTimes(sortedTimes);
        setFilteredTimes(sortedTimes);
        setStep(sortedTimes.length - 1);
    }, [activePlayers]);

    /**
     * Updates the visited nodes based on the player's temporal sequence visited and the current time.
     *
     * @param {Object} player - The player object.
     * @param {number} currentTime - The current time.
     * @return {void} This function does not return anything.
     */
    const updateVisitedNodes = useCallback((player, currentTime) => {
        const visitedNodes = [];
        const movementKeys = Object.keys(player.temporal_sequence_visited || {}).sort((a, b) => a - b);

        movementKeys.forEach(key => {
            if (key <= currentTime) {
                const nodeId = player.temporal_sequence_visited[key]?.to?.slice(-1)[0];
                if (nodeId && !visitedNodes.includes(nodeId)) {
                    visitedNodes.push(nodeId);
                }
            }
        });

        setVisitedNodes(visitedNodes);
    }, []);

    /**
     * Transforms the nodes for a single player based on their temporal sequence visited and the current time.
     *
     * @param {Object} player - The player object.
     * @param {Object[]} points - The points representing the nodes on the map.
     * @param {number} currentTime - The current time.
     * @return {Object[]} An array of objects representing the player's nodes at the current time.
     */
    const transformSinglePlayerNodes = useCallback((player, points, currentTime) => {
        // Get the keys of the player's temporal sequence visited and sort them in ascending order
        const movementKeys = Object.keys(player.temporal_sequence_visited || {}).sort((a, b) => a - b);
        // Find the last key that is less than or equal to the current time, or the last key if none found
        const lastKey = movementKeys.find(key => key <= currentTime) || movementKeys[movementKeys.length - 1];
        // Get the last visited node from the player's temporal sequence visited
        const lastVisited = player.temporal_sequence_visited[lastKey]?.to?.slice(-1)[0];
        // Find the point object representing the last visited node
        const nodePoint = points.find(point => point.id.toString() === lastVisited.toString());

        // If the node point is found, get the position around a circle and return an array with the player's node object
        if (nodePoint) {
            const position = getPositionAroundCircle(nodePoint.x, nodePoint.y, 30, 0, 1);
            return [{ id: player.id_minor, x: position.x, y: position.y }];
        } else {
            // If the last visited node is not "0", add it to the set of missing nodes
            if (lastVisited !== "0") setMissingNodes(prev => new Set(prev.add(lastVisited)));
        }

        // Return an empty array if no node point is found
        return [];
    }, [getPositionAroundCircle]);

    useEffect(() => {
        if (player) {
            setActivePlayers([player]);
        } else {
            const activePlayers = Object.values(players)
            setActivePlayers(activePlayers);
        }
    }, [players, player]);

    useEffect(() => {
        if (activePlayers.length > 0) {
            transformTemporalData();
        }
    }, [activePlayers, transformTemporalData]);

    useEffect(() => {
        const currentTime = filteredTimes[step];
        setPlayersNodes([]); // Force re-render of players nodes to avoid having "ghost" players
        setMissingNodes(new Set()); // Same for missing nodes
        if (currentTime) {
            let newPositions;
            let date = currentTime;
            if (player) {
                newPositions = transformSinglePlayerNodes(player, points, date);
                updateVisitedNodes(player, date);
            } else {
                newPositions = transformPlayersNodes(points, date);
            }
            setPlayersNodes( newPositions );
        }
    }, [step, players, activePlayers, points, filteredTimes, player, transformSinglePlayerNodes, transformPlayersNodes, updateVisitedNodes]);

    useEffect(() => {
        if (startDate && endDate) {
            const getTimeFromTimestamp = (timestamp) => {
                const date = new Date(timestamp * 1000);
                return date.getHours() * 3600 + date.getMinutes() * 60 + date.getSeconds();
            };

            const startTime = getTimeFromTimestamp(startDate);
            const endTime = getTimeFromTimestamp(endDate);

            const newFilteredTimes = allTimes.filter(time => {
                const timeOfDay = getTimeFromTimestamp(time);
                return timeOfDay >= startTime && timeOfDay <= endTime;
            });

            setFilteredTimes(newFilteredTimes);
            setStep(newFilteredTimes.length - 1);
        } else {
            setFilteredTimes(allTimes);
            setStep(allTimes.length - 1);
        }
    }, [startDate, endDate, allTimes]);

    const handleSliderChange = (event, newValue) => {
        setStep(newValue);
    };

    const playerIcon = (
        <svg width="45" height="45" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <circle cx="32" cy="20" r="10" fill="black" /> 
            <rect x="27" y="30" width="10" height="20" fill="black" /> 
            <line x1="27" y="40" x2="20" y2="50" stroke="black" strokeWidth="2" /> 
            <line x1="37" y1="40" x2="44" y2="50" stroke="black" strokeWidth="2" /> 
            <line x1="27" y1="50" x2="20" y2="60" stroke="black" strokeWidth="2" /> 
            <line x1="37" y1="50" x2="44" y2="60" stroke="black" strokeWidth="2" /> 
        </svg>
    );

    const startPlaying = () => {
        if (step === filteredTimes.length - 1)
            setStep(0);
        
        setPlayingState(true);
    };

    const stopPlaying = () => {
        setPlayingState(false);
    };

    useEffect(() => {
        if (playingState) {
            const interval = setInterval(() => {
                setStep(prevStep => {
                    if (prevStep === filteredTimes.length - 1) {
                        stopPlaying();
                        return prevStep;
                    }
                    return prevStep + 1;
                });
            }, 1000 / playingSpeed);
            return () => clearInterval(interval);
        }
    }, [playingState, filteredTimes.length, playingSpeed]);

    useEffect(() => {
        // Cap playing speed to 4x
        if (playingSpeed > 4) {
            setPlayingSpeed(1);
        }
    }, [playingSpeed]);

    return (
        <>
        <div className="map">
  
            <div className="replayer">
            <div>
                <MapBasic edges={edges} edgeThickness={0.5} mapImageName={mapImageName} points={points} handleSvgClick={null} children={
                    <>
                        {playersNodes.map(player => (
                            <g key={player.id} transform={`translate(${player.x - 22}, ${player.y - 22}) scale(1)`}>
                                {playerIcon}
                                <circle cx="22" cy="15" r="10" fill={player.has_finished === true ? "green" : "black"} />
                                <text x="22" y="15" fill="white" textAnchor="middle" alignmentBaseline="middle" fontSize="12">
                                    {player.id}
                                </text>
                            </g>
                        ))}
                        {visitedNodes.map(nodeId => {
                            const node = points.find(point => point.id === nodeId);

                            if (!node) return null;
                            
                            return (
                                <g key={node.id}>
                                    <circle cx={node.x} cy={node.y} r="12" fill="green" />
                                    <text x={node.x} y={node.y} fill="white" textAnchor="middle" alignmentBaseline="middle" fontSize="12">
                                        {node.id}
                                    </text>
                                </g>
                            );
                        })}
                        {missingNodes.size > 0 && (
                            <text x={30} y={30} fill="red" textAnchor="left" alignmentBaseline="left" fontSize="16">
                                {t('missing-node')} {Array.from(missingNodes).join(', ')}
                            </text>
                        )}
                    </>
                } />
            </div>
                {filteredTimes.length > 0 && (
                    <>
                        <div className="control">
                            <div className="controlSlider">
                                <span className='spanDate'>{new Date(filteredTimes[step] * 1000).toLocaleString()}</span>
                                <Slider
                                    value={step}
                                    onChange={handleSliderChange}
                                    min={0}
                                    max={filteredTimes.length - 1}
                                    valueLabelDisplay="auto"
                                    valueLabelFormat={value => new Date(filteredTimes[value] * 1000).toLocaleString()}
                                />

                            </div>

                            <div className="controlButtons">
                                <button className='greyButton' onClick={() => setStep(step - 1)} disabled={step === 0}>{"<"}</button>
                                <button onClick={playingState ? stopPlaying : startPlaying}>{playingState ? t('pause') : t('play')}</button>
                                {/* Speed control */}
                                { playingState && (
                                    <button onClick={() => setPlayingSpeed(playingSpeed * 2)}>{playingSpeed}x</button>
                                )}
                                <button className='greyButton' onClick={() => setStep(step + 1)} disabled={step === filteredTimes.length - 1}>{">"}</button>
                            </div>
                        </div>
                    </>
                )}
                {filteredTimes.length === 0 && (
                    <div className='control controlButtons'>
                        <span >{t('no-data-to-show')}</span>
                    </div>
                )}
            </div>
        </div>
        {/*<EventGanttChart player={player} id_device={player ? player.id_device : null} />*/}
        </>
    );
};

export default PlayerMap;
