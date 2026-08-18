import React, { useState, useEffect, useContext } from 'react';
import MakeModal from './MakeModal';
import './raspberrymodal.css';
import { useTranslation } from 'react-i18next';
import { InventoryContext } from '../../provider/InventoryProvider';

const RaspberryModal = ({ modalOpen, title, submitText, raspberryToEdit, handleClose, onSubmit, method }) => {
    const { t } = useTranslation();
    const [newRaspberry, setNewRaspberry] = useState({ name: '' });
    const [, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const { hostsNames } = useContext(InventoryContext);

    useEffect(() => {
        if (raspberryToEdit && modalOpen) {
            setNewRaspberry(raspberryToEdit);
        }
    }, [raspberryToEdit, modalOpen]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewRaspberry(prevState => ({ ...prevState, [name]: value }));
    };

    const handleCloseModal = () => {
        setNewRaspberry({ name: '' });
        setError('');
        handleClose();
    };

    const handleSubmit = () => {
        setIsLoading(true);
        onSubmit({ newRaspberry, raspberryToEdit })
            .then(() => {
                setIsLoading(false);
                handleCloseModal();
            })
            .catch((error) => {
                setIsLoading(false);
                setError(error.message);
            });
    };

    const actions = [
        { text: submitText, onClick: handleSubmit, className: 'greenButton' },
        { text: t('cancel'), onClick: handleCloseModal, className: 'redButton' }
    ];

    return (
        <MakeModal
            open={modalOpen}
            onClose={handleCloseModal}
            title={title}
            actions={actions}
        >
            {error && <p className="error">{error}</p>}
            {method !== 'delete' && (
                <div className="columnInputModal">
                    <input
                        type="text"
                        name="name"
                        placeholder={t('name')}
                        value={newRaspberry.name}
                        onChange={handleInputChange}
                        list="hostnames"
                    />
                    <datalist id="hostnames">
                        {hostsNames?.map((hostname, index) => (
                            <option key={index} value={hostname} />
                        )) || []}
                    </datalist>
                </div>
            )}
            {method === 'delete' && (
                <div>
                    <p>{t('are-you-sure-delete-raspberry', { raspberry: raspberryToEdit.name })}</p>
                </div>
            )}
        </MakeModal>
    );
};

export { RaspberryModal };
