import React from 'react';
import { Modal, Box } from '@mui/material';
import './makemodal.css';

/**
 * MakeModal component
 *
 * @component
 * @param {Object} props - The component props
 * @param {boolean} props.open - Whether the modal is open or not
 * @param {function} props.onClose - Function to close the modal
 * @param {string} props.title - The title of the modal
 * @param {ReactNode} props.children - The content of the modal
 * @param {Array<{text: string, onClick: function, className: string}>} props.actions - The actions to display in the modal
 * @return {JSX.Element} The MakeModal component
 */
class MakeModal extends React.Component {
    /**
     * Renders the MakeModal component
     *
     * @return {JSX.Element} The MakeModal component
     */
    render() {
        const { open, onClose, title, children, actions } = this.props;
        return (
            <Modal
                open={open}
                onClose={onClose}
                aria-labelledby="modal-title"
                aria-describedby="modal-description"
            >
                <Box className={`modal`}>
                    <h1 className="topTitle">{title}</h1>
                    <div className="modalContent">
                        {children}
                    </div>
                    <div className="modalActions">
                        {actions.map((action, index) => (
                            <button key={index} className={action.className} onClick={action.onClick}>
                                {action.text}
                            </button>
                        ))}
                    </div>
                </Box>
            </Modal>
        );
    }
}

export default MakeModal;
