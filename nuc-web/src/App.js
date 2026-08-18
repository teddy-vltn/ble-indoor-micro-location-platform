import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from "./components/sidebar/Sidebar";
import './App.css';
import { Person, Inventory, Terminal, Schema } from '@mui/icons-material';

import AnsiblePage from './pages/ansible/Ansible';
import GraphPage from './pages/graph/Graph';
import PlayersPage from './pages/players/Players';
import InventoryPage from './pages/inventory/Inventory';
import ToastContainer from './components/toasts/ToastContainer';

import PlayersProvider from './provider/PlayersProvider';
import GraphsProvider from './provider/GraphsProvider';
import StatusProvider from './provider/StatusProvider';
import TerminalProvider from './provider/TerminalProvider';
import AnsibleProvider from './provider/AnsibleProvider';
import InventoryProvider from './provider/InventoryProvider';

import TopBar from './components/topBar/TopBar';

import './i18n';
import { t } from 'i18next';

import { LocalizationProvider } from '@mui/x-date-pickers-pro';
import { AdapterMoment } from '@mui/x-date-pickers-pro/AdapterMoment'
import SVGCache from './svgCache';

import mermaid from "mermaid";

mermaid.initialize({
  startOnLoad: true
});

SVGCache.preloadSVGs();

class SidebarItem {
  constructor(id, path, title, icon) {
      this.id = id;
      this.path = path;
      this.title = title;
      this.icon = icon;
  }
}

const sidebarItems = [
  new SidebarItem(2, "/inventory", t('inventory'), <Inventory />),
  new SidebarItem(4, "/ansible", t('ansible'), <Terminal />),
  new SidebarItem(5, "/graph", t('graph'), <Schema />),
  new SidebarItem(3, "/players", t('players'), <Person />)
];

const renderSvgLinks = () => {
  return SVGCache.getSVGFileNames().map((svgFileName) => (
      <link key={svgFileName} rel="preload" href={SVGCache.getSVGContent(svgFileName)} as="image" />
  ));
};

function App() {

  return (
      <Router>

        {renderSvgLinks()}
        <div className="App">
        <StatusProvider> 
          <TopBar /> 
            <div className="container">
              <Sidebar sidebarItems={sidebarItems} />
              <div className="content">
                <ToastContainer />
                <Routes>
                  <Route path="/inventory" element={
                    <>
                      <InventoryProvider>
                        <InventoryPage />
                      </InventoryProvider>
                    </>
                  } />
                  <Route path="/graph" element={
                    <>
                      <GraphsProvider>
                        <GraphPage />
                      </GraphsProvider>
                    </>
                  } />
                  <Route path="/players" element={
                    <>
                      <LocalizationProvider dateAdapter={AdapterMoment}>
                        <PlayersProvider>
                          <PlayersPage />
                        </PlayersProvider>
                      </LocalizationProvider>
                    </>
                  } />
                  <Route path="/ansible" element={
                    <>
                      <AnsibleProvider>
                        <TerminalProvider>
                          <AnsiblePage />
                        </TerminalProvider>
                      </AnsibleProvider>
                    </>
                  } />
                </Routes>
              </div>
            </div>
          </StatusProvider>
        </div>
      </Router>
  );
}

export default App;
