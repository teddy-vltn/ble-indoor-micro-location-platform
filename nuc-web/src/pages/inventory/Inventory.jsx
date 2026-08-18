import './inventory.css';
import { InventoryContext } from '../../provider/InventoryProvider';
import { useContext, useEffect, useState } from 'react';
import TableComposite from '../../components/tableInfo/TableComposite';
import { Edit, DeleteForever } from '@mui/icons-material';
import { RaspberryModal } from '../../components/makeModal/RaspberryModal';
import { useTranslation } from 'react-i18next';

const InventoryPage = () => {
    const { t } = useTranslation();
    const { inventory, postHost, putHost, deleteHost } = useContext(InventoryContext);

    const [openCreateModal, setOpenCreateModal] = useState(false);
    const [openEditModal, setOpenEditModal] = useState(false);
    const [openDeleteModal, setOpenDeleteModal] = useState(false);

    const [selectedRow, setSelectedRow] = useState({});

    const handleCreateModalClose = () => {
        setOpenCreateModal(false);
        setSelectedRow({});
    }

    const handleEditModalClose = () => {
        setOpenEditModal(false);
        setSelectedRow({});
    }

    const handleDeleteModalClose = () => {
        setOpenDeleteModal(false);
        setSelectedRow({});
    }

    return (
        <div>
            <div className="section">
                <div className="space-between">
                    <h2>{t('inventory')}</h2>
                    <button onClick={() => setOpenCreateModal(true)}>{t('add-a-new-raspberry')}</button>
                </div>
            </div>

            <div className="section">
                
            </div>

            <div className="section">
                <TableComposite 
                    rows={inventory}
                    columnConfigs={[
                        { field: '_id', type: '_id', headerName: t('id') },
                        { field: 'name', type: 'text', headerName: t('name') },
                        { field: 'services.rasplogs', type: 'dot', headerName: t('data-collection') },
                        { field: 'services.filebeat', type: 'dot', headerName: t('data-forwarding') },
                        { field: 'last_pings', type: 'dot.list', headerName: t('last-pings')},
                        { field: 'timestamp_last_successful_ping', type: 'date.wasago', headerName: t('last-successful-ping')}
                    ]}
                    actions={[
                        { icon: <Edit/>, action: (row) => {
                            setSelectedRow(row);
                            setOpenEditModal(true);
                        }},
                        { icon: <DeleteForever/>, action: (row) => {
                            setSelectedRow(row);
                            setOpenDeleteModal(true);
                        }}
                    ]}
                />
            </div>

            <RaspberryModal 
                modalOpen={openCreateModal} 
                handleClose={handleCreateModalClose} 
                title={t('add-a-new-raspberry')}
                submitText={t('validate')}
                onSubmit={postHost}
            />
            <RaspberryModal 
                modalOpen={openEditModal} 
                handleClose={handleEditModalClose} 
                title={t('modify-an-existing-raspberry')} 
                submitText={t('modify')} 
                raspberryToEdit={selectedRow} 
                onSubmit={putHost}
            />
            <RaspberryModal 
                modalOpen={openDeleteModal} 
                handleClose={handleDeleteModalClose} 
                title={t('delete-an-existing-raspberry')} 
                submitText={t('delete')} 
                method="delete"
                raspberryToEdit={selectedRow} 
                onSubmit={deleteHost}
            />
        </div>
    );
}

export default InventoryPage;