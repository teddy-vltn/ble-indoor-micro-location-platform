import { useState, useContext } from 'react';
import { AnsibleContext } from '../../provider/AnsibleProvider';
import { TerminalContext } from '../../provider/TerminalProvider';
import FakeBashInterface from '../../components/fakeBashInterface/FakeBashInterface';
import './ansible.css';
import { History, Inventory } from '@mui/icons-material';
import TableComposite from '../../components/tableInfo/TableComposite';
import MakeModal from '../../components/makeModal/MakeModal';
import { useTranslation } from 'react-i18next';

const AnsiblePage = () => { 
    const { t } = useTranslation();
    const { ansibleLogs, inventory, handleInventoryActivateBoolChange } = useContext(AnsibleContext);
    const { run_script, scripts, getTerminalOutput } = useContext(TerminalContext);
    const [refresh, setRefresh] = useState(false);
    const [currentView, setCurrentView] = useState('inventory');

    const [openHistoryModal, setOpenHistoryModal] = useState(false);
    const [selectedRow, setSelectedRow] = useState({});

    const handleHistoryModalClose = () => {
        setOpenHistoryModal(false);
        setSelectedRow({});
    }
    
    const switchInventoryActive = (event) => {
        handleInventoryActivateBoolChange(event.row._id, !event.row.active);
        setRefresh(!refresh);
    }

    const inventoryView = (
        <div>
            <TableComposite 
                rows={inventory}
                columnConfigs={[
                    { field: '_id', type: 'id', headerName: t('id') },
                    { field: 'active', type: 'bool', onBooleanChange: switchInventoryActive, headerName: t('in-inventory') },
                    { field: 'name', type: 'text', headerName: t('name') },
                    { field: 'services.rasplogs', type: 'dot', headerName: t('data-collection') },
                    { field: 'services.filebeat', type: 'dot', headerName: t('data-forwarding') },
                    { field: 'last_pings', type: 'dot.list', headerName: t('last-pings')},
                    { field: 'timestamp_last_successful_ping', type: 'date.wasago', headerName: t('last-successful-ping')}
                ]}
            />
        </div>
    );

    const logsView = (
        <div>
            <TableComposite 
                rows={ansibleLogs}
                columnConfigs={[
                    { field: '_id', type: 'id', headerName: t('id') },
                    { field: 'script_name', type: 'text', headerName: t('script-name') },
                    { field: 'start_time', type: 'date.utc', headerName: t('started-at') },
                    { field: 'stop_time', type: 'date.utc', headerName: t('finished-at') },
                ]}
                actions={[
                    { icon: <History/>, action: (row) => {
                        setSelectedRow(row);
                        setOpenHistoryModal(true);
                    }}
                ]}
            />
                
        </div>
    );

    return (
        <div>
            <div className="section">
                <div className="space-between">
                    <h2>{t('ansible')}</h2>
                </div>
            </div>
            <div className="section">
                <FakeBashInterface output={getTerminalOutput()} />
            </div>
            <div className="section">
                <div className="runButtonSelect">
                    <select name="scripts" id="scripts"> 
                        {Object.keys(scripts).map((script, index) => (
                            <option key={index} value={script}>{scripts[script].name || 'Nom manquant'} - {scripts[script].description || 'Aucune description'}</option>
                        ))}
                    </select>
                    <button onClick={() => run_script(document.getElementById("scripts").value)}>{t('start-script')}</button>
                </div>
            </div>
            <div className="section">
                <div className='tabLineButton'>
                    <button 
                        className={`greyButton ${currentView === 'inventory' ? 'selected' : ''}`} 
                        onClick={() => setCurrentView('inventory')}
                    >
                        <div className='inventoryItems'>
                            <Inventory />
                            <p>{t('inventory')}</p>
                        </div>
                    </button>
                    <button 
                        className={`greyButton ${currentView === 'logs' ? 'selected' : ''}`} 
                        onClick={() => setCurrentView('logs')}
                    >
                        <div className='inventoryItems'>
                            <History />
                            <p>{t('logs')}</p>
                        </div>
                    </button>
                </div>
                <div>
                    {currentView === 'inventory' ? inventoryView : logsView}
                </div>
            </div>

            <MakeModal
                open={openHistoryModal}
                handleClose={handleHistoryModalClose}
                title={t('history')}
                children={
                    <div>
                        <h3>{t('script')}: {selectedRow.script_name}</h3>
                        <p>{t('started-at')}: {selectedRow.start_time}</p>
                        <p>{t('finished-at')}: {selectedRow.stop_time}</p>
                        <p>{t('hosts')}: {(selectedRow.hosts || []).join(', ')}</p>
                        <FakeBashInterface output={selectedRow.output}/>
                    </div>
                }
                actions={[{ text: t('close'), onClick: handleHistoryModalClose, className: 'redButton' }]}
            />
        </div>
    );
}

export default AnsiblePage;
