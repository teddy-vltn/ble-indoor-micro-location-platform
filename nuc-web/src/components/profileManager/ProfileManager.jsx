import React, { useContext, useEffect, useState } from 'react';
import { StatusContext } from '../../provider/StatusProvider';
import { useTranslation } from 'react-i18next';
import { Edit, DeleteForever, CopyAll } from '@mui/icons-material';
import MakeModal from '../makeModal/MakeModal';
import TableComposite from '../tableInfo/TableComposite';
import { ProfileModal } from '../makeModal/ProfileModal';

const ProfileManager = ({ isOpen, onClose }) => {
  const { t } = useTranslation();
  const {
    allProfiles,
    activeProfile,
    createProfile,
    deleteProfile,
    updateProfile,
    duplicateProfile,
  } = useContext(StatusContext);

  const [selectedProfileForEdit, setSelectedProfileForEdit] = useState({});
  const [openCreateProfileModal, setOpenCreateProfileModal] = useState(false);
  const [openEditProfileModal, setOpenEditProfileModal] = useState(false);
  const [openDeleteProfileModal, setOpenDeleteProfileModal] = useState(false);
  const [openDuplicateProfileModal, setOpenDuplicateProfileModal] = useState(false);

  const handleCreateProfile = ({ newProfile }) => createProfile({ new_profile: newProfile.name, graph_svg: newProfile.graph_svg });

  const handleEditProfile = ({ profileToEdit, newProfile }) => {
    updateProfile({ _id: profileToEdit._id, new_profile: newProfile.name, graph_svg: newProfile.graph_svg });
  };

  const handleDeleteProfile = ({ profileToEdit }) => deleteProfile({ _id: profileToEdit._id });

  const handleDuplicateProfile = ({ profileToEdit }) => duplicateProfile({ _id: profileToEdit._id });

  const handleOpenSubModal = (setSubModalState) => {
    setSubModalState(true);
    onClose();
  };

  const handleCloseSubModal = (setSubModalState) => {
    setSubModalState(false);
  };

  return (
    <>
      <MakeModal
        open={isOpen}
        onClose={onClose}
        title={t('experimentation-profiles')}
        children={
          <div>
            <button onClick={() => handleOpenSubModal(setOpenCreateProfileModal)}>{t('add-a-new-profile')}</button>
            <TableComposite
              rows={allProfiles}
              columnConfigs={[
                { field: '_id', type: 'id', headerName: t('id') },
                { field: 'name', type: 'text', headerName: t('name') },
                { field: 'graph_svg', type: 'text', headerName: t('graph-svg') },
                { field: 'updated_at', type: 'date.wasago', headerName: t('updated-at') },
              ]}
              actions={[
                {
                  icon: <Edit />,
                  action: (row) => {
                    setSelectedProfileForEdit(row);
                    handleOpenSubModal(setOpenEditProfileModal);
                  },
                },
                {
                  icon: <DeleteForever />,
                  action: (row) => {
                    setSelectedProfileForEdit(row);
                    handleOpenSubModal(setOpenDeleteProfileModal);
                  },
                },
                {
                  icon: <CopyAll />,
                  action: (row) => {
                    setSelectedProfileForEdit(row);
                    handleOpenSubModal(setOpenDuplicateProfileModal);
                  },
                },
              ]}
            />
          </div>
        }
        actions={[{ text: t('close'), onClick: onClose, className: 'redButton' }]}
      />
      <ProfileModals
        openCreateProfileModal={openCreateProfileModal}
        setOpenCreateProfileModal={setOpenCreateProfileModal}
        openEditProfileModal={openEditProfileModal}
        setOpenEditProfileModal={setOpenEditProfileModal}
        openDeleteProfileModal={openDeleteProfileModal}
        setOpenDeleteProfileModal={setOpenDeleteProfileModal}
        openDuplicateProfileModal={openDuplicateProfileModal}
        setOpenDuplicateProfileModal={setOpenDuplicateProfileModal}
        selectedProfileForEdit={selectedProfileForEdit}
        handleCloseSubModal={handleCloseSubModal}
        handleCreateProfile={handleCreateProfile}
        handleEditProfile={handleEditProfile}
        handleDeleteProfile={handleDeleteProfile}
        handleDuplicateProfile={handleDuplicateProfile}
      />
    </>
  );
};

const ProfileModals = ({
  openCreateProfileModal,
  setOpenCreateProfileModal,
  openEditProfileModal,
  setOpenEditProfileModal,
  openDeleteProfileModal,
  setOpenDeleteProfileModal,
  openDuplicateProfileModal,
  setOpenDuplicateProfileModal,
  selectedProfileForEdit,
  handleCloseSubModal,
  handleCreateProfile,
  handleEditProfile,
  handleDeleteProfile,
  handleDuplicateProfile,
}) => {
  const { t } = useTranslation();

  return (
    <>
      <ProfileModal
        modalOpen={openCreateProfileModal}
        handleClose={() => handleCloseSubModal(setOpenCreateProfileModal)}
        title={t('create-a-new-profile')}
        submitText={t('create')}
        onSubmit={handleCreateProfile}
      />
      <ProfileModal
        modalOpen={openEditProfileModal}
        handleClose={() => handleCloseSubModal(setOpenEditProfileModal)}
        title={t('modify-an-existing-profile')}
        profileToEdit={selectedProfileForEdit}
        submitText={t('modify')}
        onSubmit={handleEditProfile}
      />
      <ProfileModal
        modalOpen={openDeleteProfileModal}
        handleClose={() => handleCloseSubModal(setOpenDeleteProfileModal)}
        title={t('delete-an-existing-profile')}
        profileToEdit={selectedProfileForEdit}
        submitText={t('delete')}
        method="delete"
        onSubmit={handleDeleteProfile}
      />
      <ProfileModal
        modalOpen={openDuplicateProfileModal}
        handleClose={() => handleCloseSubModal(setOpenDuplicateProfileModal)}
        title={t('duplicate-an-existing-profile')}
        profileToEdit={selectedProfileForEdit}
        submitText={t('duplicate')}
        method="duplicate"
        onSubmit={handleDuplicateProfile}
      />
    </>
  );
};

export default ProfileManager;
