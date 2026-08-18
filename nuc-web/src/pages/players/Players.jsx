import './players.css'
import PlayerMap from '../../components/map/PlayerMap'
import { useContext, useState, useEffect, useCallback, act } from 'react';
import { PlayersContext } from '../../provider/PlayersProvider';
import TableComposite from '../../components/tableInfo/TableComposite';
import { DeleteForever, Flag, Map } from '@mui/icons-material';
import MakeModal from '../../components/makeModal/MakeModal';
import { useTranslation } from 'react-i18next';
import TableFilter from '../../components/tableInfo/TableFilter';
import moment from 'moment';


const PlayerSection = ({ players, graph, getActiveProfileSvgMap, filters, setFilters, columnConfigs }) => {
    if (!players) return null;

    return (
        <div className="section">
            <TableFilter filters={filters} setFilters={setFilters} columnConfigs={columnConfigs} />
            <PlayerMap 
                players={players} 
                graph={graph} 
                mapImageName={getActiveProfileSvgMap()}
                startDate={filters.started_at}
                endDate={filters.finished_at}
            />
        </div>
    );
};

const PlayersPage = () => {
    const { t } = useTranslation();
    const { graph, setFinishPlayerState, deletePlayer, deleteAllPlayers, getActiveProfileSvgMap, activeProfile, activeSession } = useContext(PlayersContext);

    const [players, setPlayers] = useState(activeSession?.players || []);
    const [currentActiveProfile, setCurrentActiveProfile] = useState(null);
    const [filteredPlayers, setFilteredPlayers] = useState([]);
    const [filteredRows, setFilteredRows] = useState([]);
    const [selectedRow, setSelectedRow] = useState({});
    const [selectedSession, setSelectedSession] = useState(activeSession || null);
    const [startDate, setStartDate] = useState(activeSession ? activeSession.started_at : null);
    const [endDate, setEndDate] = useState(activeSession ? activeSession.finished_at : null);
    const [filters, setFilters] = useState({
        session: activeSession?._id || '',
        started_at: '',
        finished_at: ''
    });

    useEffect(() => {
        if (!activeProfile.sessions) return;

        if (currentActiveProfile?._id === activeProfile._id) return;
      
        if (activeProfile.sessions.length === 0) {
          setSelectedSession(null);
          setStartDate(null);
          setEndDate(null);
          setPlayers([]);
          return;
        }
        
        const session = activeProfile.sessions[0];
        setSelectedSession(session);
        setCurrentActiveProfile(activeProfile);
      
    }, [activeProfile]);
      
    useEffect(() => {
        if (activeSession) {
            setSelectedSession(activeSession);
        }
    }, [activeSession]);
      

    useEffect(() => {
        if (!selectedSession) return;

        setStartDate(selectedSession.started_at);
        setEndDate(selectedSession.finished_at);
        setFilters({
            ...filters,
            session: selectedSession._id,
            started_at: selectedSession.started_at,
            finished_at: selectedSession.finished_at
        });
        setPlayers(selectedSession.players);
        setFilteredPlayers(selectedSession.players);
    }, [selectedSession]);

    useEffect(() => {
        // filter players when filteredRows change
        if (filteredRows.length === 0) return;

        const filteredPlayers = selectedSession.players.filter(player => {
            return filteredRows.some(row => row._id === player._id);
        });

        setFilteredPlayers(filteredPlayers);
    }, [filteredRows]);

    const handleSessionChange = useCallback((sessionId) => {
        const session = activeProfile.sessions.find(session => session._id === sessionId);
        setSelectedSession(session);
        setFilters({
            ...filters,
            session: sessionId,
            started_at: startDate,
            finished_at: endDate
        });
    }, [activeProfile.sessions, filters, startDate, endDate]);

    const selectOptions = useCallback(() => {
        if (!activeProfile) return [];
        if (!activeProfile.sessions) return [];

        // sort sessions by started_at
        const sortedSessions = activeProfile.sessions.sort((a, b) => b.started_at - a.started_at);

        return sortedSessions.map(session => {
            return {
                value: session._id,
                label: `${session.name}`
            }
        });
    }, [activeProfile]);

    const handleStartDateChange = useCallback((date) => {
        setFilters({
            ...filters,
            started_at: date.valueOf() / 1000
        });
    }, [filters]);

    const handleEndDateChange = useCallback((date) => {
        setFilters({
            ...filters,
            finished_at: date.valueOf() / 1000
        });
    }, [filters]);

    const columnConfigs = [
        { field: '_id', type: 'id', headerName: t('id') },
        {
            field: 'session',
            type: 'select',
            options: selectOptions(),
            headerName: t('session'),
            onChange: (e) => {
                handleSessionChange(e)
            },
            disabled: !!activeSession
        },
        { field: 'time_range_start', type: 'hour', headerName: t('time-range-start'), baseValue: startDate, minValue: startDate, maxValue: endDate, onChange: handleStartDateChange },
        { field: 'time_range_end', type: 'hour', headerName: t('time-range-end'), baseValue: endDate, minValue: startDate, maxValue: endDate, onChange: handleEndDateChange },
    ];

    const [openMapModal, setOpenMapModal] = useState(false);
    const [openFinishModal, setOpenFinishModal] = useState(false);
    const [openDeleteModal, setOpenDeleteModal] = useState(false);
    const [openDeleteAllModal, setOpenDeleteAllModal] = useState(false);

    const handleMapModalClose = useCallback(() => {
        setOpenMapModal(false);
        setSelectedRow({});
    }, []);

    const handleFinishModalClose = useCallback(() => {
        setOpenFinishModal(false);
        setSelectedRow({});
    }, []);

    const handleDeleteModalClose = useCallback(() => {
        setOpenDeleteModal(false);
        setSelectedRow({});
    }, []);

    const handleDeleteAllModalClose = useCallback(() => {
        setOpenDeleteAllModal(false);
    }, []);

    const handleFinishPlayer = useCallback(() => {
        const event = selectedRow;
        setFinishPlayerState(event._id);
        handleFinishModalClose();
    }, [selectedRow, setFinishPlayerState, handleFinishModalClose]);

    const handleDeletePlayer = useCallback(() => {
        const event = selectedRow;
        deletePlayer(event._id);
        handleDeleteModalClose();
    }, [selectedRow, deletePlayer, handleDeleteModalClose]);

    const handleDeleteAllPlayers = useCallback(() => {
        deleteAllPlayers();
        handleDeleteAllModalClose();
    }, [deleteAllPlayers, handleDeleteAllModalClose]);

    const findPlayer = useCallback(() => {
        return selectedRow._id ? selectedSession.players.find(player => player._id === selectedRow._id) : {};
    }, [selectedRow, selectedSession]);

    const onTransformedRows = useCallback((rows) => {
        setFilteredRows(rows);
    });

    return (
        <div>
            <div className="section">
                <div className="space-between">
                    <h2>{t('movement-tracking')}</h2>
                </div>
            </div>

            <PlayerSection
                players={filteredPlayers}
                graph={graph}
                getActiveProfileSvgMap={getActiveProfileSvgMap}
                selectedSession={selectedSession}
                filters={filters}
                setFilters={setFilters}
                columnConfigs={columnConfigs}
            />

            <div className="section">
                <TableComposite
                    rows={players}
                    columnConfigs={[
                        { field: '_id', type: 'id', headerName: t('id') },
                        { field: 'id_player', type: 'text', headerName: t("id-player") },
                        { field: 'id_minor', type: 'text', headerName: t('minor') },
                        { field: 'devices', type: 'list', headerName: t('interacted-with-device') },
                        { field: 'started_at', type: 'date.wasago', headerName: t('created-was-ago') },
                        { field: 'updated_at', type: 'date.wasago', headerName: t('updated-was-ago') },
                        { field: 'has_finished', type: 'dot.bool', headerName: t('finished') }
                    ]}
                    actions={[
                        { icon: <Map/>, action: (row) => {
                            setSelectedRow(row);
                            setOpenMapModal(true);
                        }},
                        { icon: <Flag/>, action: (row) => {
                            setSelectedRow(row);
                            setOpenFinishModal(true);
                        }},
                        { icon: <DeleteForever/>, action: (row) => {
                            setSelectedRow(row);
                            setOpenDeleteModal(true);
                        }}
                    ]}
                    onTransformedRows={onTransformedRows}
                />
            </div>

            <div className="section">
                <button className="redButton" onClick={() => setOpenDeleteAllModal(true)}>{t('delete-all-existing-players')}</button>
            </div>

            <MakeModal
                open={openMapModal}
                onClose={() => setOpenMapModal(false)}
                title={t('player-map')}
                children={
                    <div>
                        <PlayerMap player={findPlayer()} graph={graph} selectedRow={selectedRow} mapImageName={getActiveProfileSvgMap()} />
                    </div>
                }
                actions={[{ text: t('close'), onClick: handleMapModalClose, className: 'redButton' }]}
            />
            <MakeModal
                open={openFinishModal}
                onClose={() => setOpenFinishModal(false)}
                title={t('mark-player-finish-state')}
                children={
                    <div>
                        <p>{t('are-you-sure-finish-state-player', {player: selectedRow.id_player})}</p>
                    </div>
                }
                actions={[{ text: t('finish'), onClick: handleFinishPlayer, className: 'greenButton' }, { text: t('cancel'), onClick: handleFinishModalClose, className: 'redButton' }]}
            />
            <MakeModal
                open={openDeleteModal}
                onClose={() => setOpenDeleteModal(false)}
                title={t('delete-an-existing-player')}
                children={
                    <div>
                        <p>{t('are-you-sure-delete-player', {player: selectedRow.id_player})}</p>
                    </div>
                }
                actions={[{ text: t('delete'), onClick: handleDeletePlayer, className: 'greenButton' }, { text: t('cancel'), onClick: handleDeleteModalClose, className: 'redButton' }]}
            />
            <MakeModal
                open={openDeleteAllModal}
                onClose={() => setOpenDeleteAllModal(false)}
                title={t('delete-all-existing-players')}
                children={
                    <div>
                        <p>{t('are-you-sure-delete-all-players')}</p>
                    </div>
                }
                actions={[{ text: t('delete'), onClick: handleDeleteAllPlayers, className: 'greenButton' }, { text: t('cancel'), onClick: handleDeleteAllModalClose, className: 'redButton' }]}
            />
        </div>
    );
}

export default PlayersPage;
