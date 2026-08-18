import React, { createContext, useContext, useState, useEffect } from 'react';
import env from 'react-dotenv';
import { apiRequest } from '../apiHelper';
import { StatusContext } from './StatusProvider';

export const GraphsContext = createContext();

/**
 * GraphsProvider component that provides the graph related data and actions
 * to its child components through the GraphsContext.
 *
 * @param {Object} props - The component props.
 * @param {ReactNode} props.children - The child components.
 * @returns {ReactNode} The rendered child components.
 */
const GraphsProvider = ({ children }) => {
    // Destructure the necessary data from the StatusContext
    const { refresh, graph, inventory, activeProfile } = useContext(StatusContext);
    // State hooks to store the transformed graph and unpaired devices
    const [nodeConnections, setNodeConnections] = useState([]);
    const [unpairedDevices, setUnpairedDevices] = useState([]);

    // Effect hook to transform the graph and inventory when they change
    useEffect(() => {
        transformGraphAndInventory(graph, inventory);
    }, [graph, inventory]);

    /**
     * Transforms the graph and inventory data into a format that can be used by the child components.
     *
     * @param {Object} graphData - The graph data.
     * @param {Object} inventoryData - The inventory data.
     */
    const transformGraphAndInventory = (graphData, inventoryData) => {
        const nodesMap = {};
        const unpairedDevices = [];

        // Map the graph nodes to an object for easier access
        graphData.nodes.forEach(node => {
            nodesMap[node.id] = { ...node, device: null, name: "Noeud " + node.id };
        });

        // Loop through the inventory devices and match them with the corresponding nodes
        Object.values(inventoryData).forEach(device => {
            const nodeId = device.node;
            if (nodesMap[nodeId] && !nodesMap[nodeId].device) {
                nodesMap[nodeId].device = device;
            } else {
                unpairedDevices.push(device);
            }
        });

        // Set the transformed data in the state hooks
        setNodeConnections(Object.values(nodesMap));
        setUnpairedDevices(unpairedDevices);
    };

    /**
     * Object containing the graph related actions.
     *
     * @type {Object}
     */
    const graphActions = {
        /**
         * Saves the node settings by updating the device node in the inventory.
         *
         * @param {Object} data - The data containing the nodeId and deviceName.
         */
        saveNode: ({ nodeId, deviceName }) => apiRequest({
            url: `http://${window.location.hostname}:5001/inventory/hosts/${deviceName}`,
            method: 'PUT',
            data: { node: nodeId },
            onSuccess: (response) => {
                refresh();
                transformGraphAndInventory(graph, inventory);
            }
        }),
        /**
         * Saves the graph by updating the graph data in the server.
         *
         * @param {Object} graph - The graph data to be saved.
         */
        saveGraph: (graph) => apiRequest({ url: `http://${window.location.hostname}:5001/graph`, method: 'PUT', data: graph, onSuccess: refresh }),
        /**
         * Downloads the graph data as a YAML file.
         */
        downloadYamlGraph: () => {
            apiRequest({
                url: `http://${window.location.hostname}:5001/graph/download`,
                method: 'GET',
                onSuccess: (response) => {
                    const url = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', 'graph.yaml');
                    document.body.appendChild(link);
                    link.click();
                }
            });
        }
    };

    /**
     * Returns the SVG map of the active profile.
     *
     * @returns {string|null} The SVG map of the active profile or null if no active profile.
     */
    const getActiveProfileSvgMap = () => {
        return activeProfile ? activeProfile.graph_svg : null;
    }

    // Return the GraphsContext provider with the necessary data and actions
    return (
        <GraphsContext.Provider value={{ graph, inventory, nodeConnections, unpairedDevices, ...graphActions, getActiveProfileSvgMap }}>
            {children}
        </GraphsContext.Provider>
    );
};

export default GraphsProvider;
