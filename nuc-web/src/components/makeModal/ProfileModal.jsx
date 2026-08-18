import React, { useState, useEffect } from 'react';
import MakeModal from './MakeModal';
import './profilemodal.css';
import { useTranslation } from 'react-i18next';
import SVGCache from '../../svgCache';


const ProfileModal = ({ modalOpen, title, submitText, profileToEdit, handleClose, onSubmit, method }) => {
    const { t } = useTranslation();
    const [newProfile, setNewProfile] = useState({ name: '', graph_svg: SVGCache.getSVGFileNames()[0] });
    const [, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        if (profileToEdit && modalOpen) {
            setNewProfile(profileToEdit);
        }
    }, [profileToEdit, modalOpen]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewProfile(prevState => ({ ...prevState, [name]: value }));
    };

    const handleCloseModal = () => {
        setNewProfile({ name: '', graph_svg: SVGCache.getSVGFileNames()[0] });
        setError('');
        handleClose();
    };

    const handleSubmit = async () => {
        setIsLoading(true);
        try {
            await onSubmit({ newProfile, profileToEdit });
            handleCloseModal();
        } catch (error) {
            setError(error.message);
        } finally {
            setIsLoading(false);
        }
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
                        value={newProfile.name}
                        onChange={handleInputChange}
                    />
                    <select
                        name="graph_svg"
                        value={newProfile.graph_svg}
                        onChange={handleInputChange}
                    >
                        {SVGCache.getSVGFileNames().map((svgFileName) => (
                            <option key={svgFileName} value={svgFileName}>{svgFileName}</option>
                        ))}
                    </select>
                    <img src={SVGCache.getSVGContent(newProfile.graph_svg)} alt="graph" />
                </div>
            )}
            {method === 'delete' && (
                <div>
                    <p>{t('are-you-sure-delete-profile', { profile: profileToEdit.name })}</p>
                </div>
            )}
        </MakeModal>
    );
};

export { ProfileModal };
