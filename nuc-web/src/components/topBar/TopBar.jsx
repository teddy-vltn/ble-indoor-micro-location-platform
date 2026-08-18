import React, { useState, useContext, useEffect } from "react";
import "./topbar.css";
import { Settings, PlayArrow, Stop } from "@mui/icons-material";
import ProfileManager from "../profileManager/ProfileManager";
import { StatusContext } from "../../provider/StatusProvider";
import MakeModal from "../makeModal/MakeModal";
import { useTranslation } from "react-i18next";

const TopBar = () => {
  const { t } = useTranslation();
  const {
    allProfiles,
    activeProfile,
    changeProfile,
    startNewSessionForProfile,
    stopSessionForProfile,
    getActiveSession
  } = useContext(StatusContext);

  const [isSessionCreationOpen, setIsSessionCreationOpen] = useState(false);
  const [isSessionStopOpen, setIsSessionStopOpen] = useState(false);
  const [isProfileManagerOpen, setIsProfileManagerOpen] = useState(false);
  const [selectedProfileId, setSelectedProfileId] = useState(activeProfile._id);
  const [activeSession, setActiveSession] = useState(null);
  const [sessionName, setSessionName] = useState('');

  useEffect(() => {
    setSelectedProfileId(activeProfile._id);
  }, [activeProfile]);

  useEffect(() => {
    const fetchActiveSession = async () => {
      const session = await getActiveSession();
      setActiveSession(session);
    };

    fetchActiveSession();
  }, [getActiveSession]);

  const handleSettingsClick = () => {
    setIsProfileManagerOpen(true);
  };

  const handleProfileManagerClose = () => {
    setIsProfileManagerOpen(false);
  };

  const handleProfileChange = (e) => {
    const profileId = e.target.value;
    setSelectedProfileId(profileId);
    changeProfile({ _id: profileId });
  };

  const handleSessionButtonClick = () => {
    /*if (activeSession) {
      stopSessionForProfile();
      setActiveSession(null); // Manually update the state to reflect session stop
    } else {
      startNewSessionForProfile({ name: 'new session' });
      setActiveSession(getActiveSession()); // Manually update the state to reflect session start
    }*/

    if (activeSession) {
        setIsSessionStopOpen(true);
    } else {
        setIsSessionCreationOpen(true);
    }
  };

  const handleStartSession = () => {
    startNewSessionForProfile({ name: sessionName });
    setActiveSession(getActiveSession());
    setIsSessionCreationOpen(false);
  }

  const handleStopSession = () => {
    stopSessionForProfile();
    setActiveSession(null);
    setIsSessionStopOpen(false);
  }

  const handleCloseModal = () => {
    setIsSessionCreationOpen(false);
    setIsSessionStopOpen(false);
  }

  const actionsStart = [
    { text: t('start'), onClick: handleStartSession, className: 'greenButton' },
    { text: t('cancel'), onClick: handleCloseModal, className: 'redButton' }
  ];

  const actionsStop = [
    { text: t('stop'), onClick: handleStopSession, className: 'greenButton' },
    { text: t('cancel'), onClick: handleCloseModal, className: 'redButton' }
  ];

  return (
    <div className="topBar">
      <div className="topBarLeft">
        <span className="topTitle">{t('profil')}</span>
        <select
          className="profileSelect"
          value={selectedProfileId}
          onChange={handleProfileChange}
          disabled={!!activeSession}
        >
          {allProfiles.map((profile) => (
            <option key={profile._id} value={profile._id}>
              {profile.name}
            </option>
          ))}
        </select>
        {!activeSession && (
          <Settings className="settingsIcon" onClick={handleSettingsClick} />
        )}
      </div>
      <div className="topBarRight">
        <button
          className={`topButton ${activeSession ? "redButton" : ""}`}
          onClick={handleSessionButtonClick}
        >
          {activeSession ? <Stop /> : <PlayArrow />}
          <span className="topButtonText">
            {activeSession ? t('stop-session') : t('start-session')}
          </span>
        </button>
        {activeSession && (
          <span className="sessionText">
            {t('session-active', {0: activeSession.name, 1:new Date(activeSession.started_at * 1000).toLocaleString()})}
          </span>
        )} 
        {!activeSession && (
          <span className="sessionText">
            {t('no-active-session')}
          </span>
        )}
      </div>

      <MakeModal
        open={isSessionCreationOpen}
        onClose={handleCloseModal}
        title={t('start-session')}
        actions={actionsStart}
     >
        <input
          type="text"
          name="name"
          placeholder={t('session-name')}
          value={sessionName} onChange={(e) => setSessionName(e.target.value)}
        />
      </MakeModal>

        <MakeModal
        open={isSessionStopOpen}
        onClose={handleCloseModal}
        title={t('stop-session')}
        actions={actionsStop}
        >
        <p>{t('are-you-sure-stop-session')}</p>
        
        </MakeModal>

      <ProfileManager
        isOpen={isProfileManagerOpen}
        onClose={handleProfileManagerClose}
      />
    </div>
  );
};

export default TopBar;
