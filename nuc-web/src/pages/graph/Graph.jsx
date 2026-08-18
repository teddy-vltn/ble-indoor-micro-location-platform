import NodeMap from '../../components/map/NodeMap';
import './graph.css';
import { GraphsContext } from '../../provider/GraphsProvider';
import { useContext } from 'react';
import TableComposite from '../../components/tableInfo/TableComposite';
import { useTranslation } from 'react-i18next';

const GraphPage = () => {
    const { t } = useTranslation();
    const { 
        graph, getActiveProfileSvgMap,
        inventory, 
        nodeConnections, unpairedDevices, 
        saveGraph, saveNode, downloadYamlGraph
    } = useContext(GraphsContext);

    const saveNodeSettings = (event) => {
        const raspberryName = event.newValue;
        const raspberryId = Object.values(unpairedDevices).find(device => device.name === raspberryName)._id;
        saveNode({ nodeId: event.row.id, deviceName: raspberryId });
    }

    const resetNodeSettings = (event) => {
        const raspberryName = event.device.name
        const raspberryId = Object.values(inventory).find(device => device.name === raspberryName)._id;
        saveNode({ nodeId: null, deviceName: raspberryId });
    }
        
    return (
        <div>

            <div className="section">
                <div className="space-between">
                    <h2>{t('graph')}</h2>
                    <button onClick={downloadYamlGraph}>{t('export-yaml')}</button>
                </div>
            </div>

            <div className="section">
                <NodeMap  
                    graph={graph}
                    inventory={inventory}
                    save={saveGraph}
                    mapImageName={getActiveProfileSvgMap()}
                    unplacedRaspberryPis={unpairedDevices}
                    onNodeAssignRaspberry={saveNodeSettings}
                />
            </div>

            <div className="section">
                <TableComposite
                    rows={nodeConnections}
                    columnConfigs={[
                        { field: '_id', type: '_id', headerName: t('id') },
                        { field: 'name', type: 'text', headerName: t('name') },
                        { field: 'device.name',
                            type: 'select', 
                            options: unpairedDevices,
                            onChange : saveNodeSettings,
                            onReset : resetNodeSettings,
                            headerName: t('device-name'),
                            filter : false
                        }
                    ]}

                />
            </div>

        </div>
    );
}

export default GraphPage;