import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './sidebar.css';
import { Menu } from '@mui/icons-material';
import { Tooltip, IconButton, Menu as MuiMenu, MenuItem } from '@mui/material';
import ProfileManager from '../profileManager/ProfileManager';
import { useTranslation } from 'react-i18next';
import LanguageIcon from '@mui/icons-material/Language';
import FlagIcon from '@mui/icons-material/Flag';

export default function Sidebar({ sidebarItems = [] }) {
  const { t, i18n } = useTranslation();
  const [isOpen, setIsOpen] = useState(true);
  const [anchorEl, setAnchorEl] = useState(null);

  const location = useLocation();
  const currentPath = location.pathname;

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 768) {
        setIsOpen(true);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const toggleSidebar = () => setIsOpen((prev) => !prev);

  const handleMenuClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLanguageChange = (lng) => {
    i18n.changeLanguage(lng);
    handleMenuClose();
  };

  return (
    <div className="container">
      <div className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
        <div className="sidebarContent">
          <div className="sidebarWrapper">
            <h3 className="sidebarTitle">{t('vues')}</h3>
            <ul className="sidebarList">
              {sidebarItems.map((item) => (
                <Link
                  to={item.path}
                  onClick={() => window.innerWidth <= 768 && setIsOpen(false)}
                  className="sidebarLink"
                  key={item.id}
                >
                  <li className={`sidebarListItem ${currentPath === item.path ? 'active' : ''}`}>
                    <Tooltip title={t(item.title)} placement="right">
                      <div className="sidebarIcon">{item.icon}</div>
                    </Tooltip>
                  </li>
                </Link>
              ))}
            </ul>
            <div className="languageToggle">
              <IconButton onClick={handleMenuClick} size="large">
                <LanguageIcon />
              </IconButton>
              <MuiMenu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
              >
                <MenuItem onClick={() => handleLanguageChange('en')}>
                  {t('english')}
                </MenuItem>
                <MenuItem onClick={() => handleLanguageChange('fr')}>
                  {t('french')}
                </MenuItem>
              </MuiMenu>
            </div>
          </div>
        </div>
      </div>
      <ProfileManager />
      <button className="menuButton" onClick={toggleSidebar}>
        <Menu />
      </button>
    </div>
  );
}
