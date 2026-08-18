import React, { useState, useEffect } from 'react';
import './map.css';
import { Toolbar } from './MapComponents';
import MapBasic from './MapBasic';
import ToastManager from '../toasts/ToastManager';
import { useTranslation } from 'react-i18next';

/**
 * Renders a NodeMap component.
 *
 * @param {Object} props - The properties of the component.
 * @param {Object} props.graph - The graph object.
 * @param {Object} props.inventory - The inventory object.
 * @param {Function} props.save - The save function.
 * @param {string} props.mapImageName - The name of the map image.
 * @param {Object} props.unplacedRaspberryPis - The unplaced Raspberry Pis.
 * @param {Function} props.onNodeAssignRaspberry - The function to assign a Raspberry Pi to a node.
 * @return {JSX.Element} The rendered NodeMap component.
 */
export default function NodeMap({ graph, inventory, save, mapImageName, unplacedRaspberryPis, onNodeAssignRaspberry }) {
  const { t } = useTranslation();
  const [transformedInventory, setTransformedInventory] = useState({});
  const [points, setPoints] = useState([]);
  const [edges, setEdges] = useState([]);
  const [selectedPoint, setSelectedPoint] = useState(null);
  const [mode, setMode] = useState('node');
  const [tempPoint, setTempPoint] = useState(null);
  const [eventClick, setEventClick] = useState(null);
  const [idInput, setIdInput] = useState('');
  const [editMode, setEditMode] = useState(false);
  const [isAddingNode, setIsAddingNode] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [draggedNode, setDraggedNode] = useState(null);

  useEffect(() => {
    if (inventory) {
      const newTransformedInventory = Object.entries(inventory).reduce(
        (acc, [key, value]) => {
          acc[value.node] = { ...value, name: key };
          return acc;
        },
        {}
      );
      setTransformedInventory(newTransformedInventory);
    }
  }, [inventory]);

  useEffect(() => {
    if (!editMode) {
      setPoints(graph.nodes || []);
      setEdges(graph.edges || []);
      setMode('');
    }
  }, [graph, editMode]);

  useEffect(() => {
    setSelectedPoint(null);
    setTempPoint(null);
    setIsAddingNode(false);
    setIdInput('');
  }, [editMode, mode]);

  const isOnline = (node) => {
    try {
      const lastPings = transformedInventory[node]?.last_pings;
      return lastPings?.[lastPings.length - 1] ?? null;
    } catch {
      return null;
    }
  };

  const getName = (node) => transformedInventory[node]?.name ?? t('node', { id: node });

  const colorOnline = (node) => {
    const status = isOnline(node);
    if (status === null) return 'grey';
    return status ? 'green' : 'red';
  };

  const colorServices = (node) => {
    try {
      const services = transformedInventory[node]?.services;
      if (!services) return 'grey';

      const serviceStatuses = Object.values(services);
      if (!serviceStatuses.length) return 'grey';

      return serviceStatuses.every((status) => status === true) ? 'green' : 'red';
    } catch {
      return 'grey';
    }
  };

  const computeTransform = (x, y) => {
    return {
      x: x,
      y: y 
    };
  };

  const handleMouseDown = (event, point) => {
    if (mode === 'move') {
      setDraggedNode(point);
      setIsDragging(true);
      event.stopPropagation();
    }
  };

  const handleMouseMove = (event) => {
    if (isDragging && draggedNode) {
      const svg = document.querySelector('.mapContainer .mapSvg svg');
      const rect = svg.getBoundingClientRect();
      const transform = svg.getScreenCTM().inverse();

      const x = (event.clientX - rect.left) * transform.a;
      const y = (event.clientY - rect.top) * transform.d;


      setPoints((points) =>
        points.map((p) => (p.id === draggedNode.id ? { ...p, x, y } : p))
      );
    }
  };

  const handleMouseUp = () => {
    if (mode === 'move' && isDragging) {
      setIsDragging(false);
      setDraggedNode(null);
    }
  };

  const handleSvgClick = (event) => {
    if (mode === 'node' && editMode) {
      const svg = document.querySelector('.mapContainer .mapSvg svg');
      const rect = svg.getBoundingClientRect();
      const transform = svg.getScreenCTM().inverse();
  
      const x = (event.clientX - rect.left) * transform.a 
      const y = (event.clientY - rect.top) * transform.d
  
      setTempPoint({ x, y });
      // Get the x and y coordinates of the click event for the mapContainer
      const mapContainer = document.querySelector('.mapContainer');
      setEventClick({ clientX: event.clientX - mapContainer.offsetLeft, clientY: event.clientY - mapContainer.offsetTop });
      setSelectedPoint(null);
      setIsAddingNode(true);
    }
  };  

  const handlePointClick = (event, point) => {
    event.stopPropagation();
    if (mode === 'edge' && selectedPoint && selectedPoint.id !== point.id) {
      if (
        !edges.some(
          (e) =>
            (e.from === selectedPoint.id && e.to === point.id) ||
            (e.from === point.id && e.to === selectedPoint.id)
        )
      ) {
        setEdges((prevEdges) => [...prevEdges, { from: selectedPoint.id, to: point.id }]);
        setSelectedPoint(null);
      }
    } else if (mode === 'edge') {
      setSelectedPoint(point);
    } else if (mode === 'node') {
      setSelectedPoint(point);
      const svg = document.querySelector('.mapContainer .mapSvg svg');
      const rect = svg.getBoundingClientRect();
      const transform = svg.getScreenCTM().inverse();

      const x = (event.clientX - rect.left) * transform.a;
      const y = (event.clientY - rect.top) * transform.d;

      setTempPoint({ x, y });
      setIdInput(point.id);
      setIsAddingNode(false);
    }
  };

  const addNode = () => {
    if (tempPoint && idInput && !points.some((p) => p.id === idInput)) {
      const newNode = { ...computeTransform(tempPoint.x, tempPoint.y), id: idInput, name: t('node', { id: idInput }) };
      setPoints((prevPoints) => [...prevPoints, newNode]);
      setIsAddingNode(false);
      setTempPoint(null);
      setIdInput('');
    } else {
      ToastManager.warning(t('id-already-exists-or-invalid-input'));
    }
  };

  const updateNode = () => {
    if (selectedPoint && idInput && !points.some((p) => p.id === idInput && p !== selectedPoint)) {
      const updatedPoints = points.map((p) => (p === selectedPoint ? { ...p, id: idInput, name: t('node', { id: idInput }) } : p));
      const updatedEdges = edges.map((e) => ({
        from: e.from === selectedPoint.id ? idInput : e.from,
        to: e.to === selectedPoint.id ? idInput : e.to,
      }));
      setPoints(updatedPoints);
      setEdges(updatedEdges);
      setSelectedPoint(null);
      setIdInput('');
    } else {
      ToastManager.warning(t('id-already-exists-or-invalid-input'));
    }
  };

  const deleteNode = () => {
    if (selectedPoint) {
      setPoints((points) => points.filter((p) => p !== selectedPoint));
      setEdges((edges) => edges.filter((e) => e.from !== selectedPoint.id && e.to !== selectedPoint.id));
      resetInput();
    }
  };

  const resetEdges = () => {
    if (selectedPoint) {
      setEdges((edges) => edges.filter((e) => e.from !== selectedPoint.id && e.to !== selectedPoint.id));
      resetInput();
    }
  };

  const resetInput = () => {
    setTempPoint(null);
    setIdInput('');
    setSelectedPoint(null);
  };

  const generateIdInput = () => {
    if (idInput !== '') {
      return idInput;
    }

    const ids = points.map((p) => p.id);
    let id = 1;
    while (ids.includes(id.toString())) {
      id++;
    }
    setIdInput(id.toString());
    return id.toString();
  };

  const saveGraph = async () => {
    if (points.length === 0 || edges.length === 0) {
      ToastManager.warning(t('graph-is-empty'));
      return;
    }

    try {
      await save({ nodes: points, edges });
      setEditMode(false);
    } catch (error) {
      console.error('Error saving graph:', error);
    }
  };

  return (
    <div className="map" onMouseMove={handleMouseMove} onMouseUp={handleMouseUp}>
      <MapBasic
        edges={edges}
        points={points}
        selectedPoint={selectedPoint}
        draggedNode={draggedNode}
        isDragging={isDragging}
        handlePointClick={handlePointClick}
        handleSvgClick={handleSvgClick}
        handleMouseDown={handleMouseDown}
        colorOnline={colorOnline}
        colorServices={colorServices}
        getName={getName}
        mapImageName={mapImageName}
        toolsChildren={
          <Toolbar editMode={editMode} setEditMode={setEditMode} setMode={setMode} saveGraph={saveGraph} />
        }
      >
      </MapBasic>
      {editMode && tempPoint && isAddingNode && (
        <div style={{ position: 'absolute', top: eventClick.clientY, left: eventClick.clientX }}>
          <input type="text" value={generateIdInput()} onChange={(e) => setIdInput(e.target.value)} placeholder="ID" />
          <select onChange={(e) => onNodeAssignRaspberry({ row: { id: generateIdInput() }, newValue: e.target.value })}>
            <option value="">{t('select-raspberry')}</option>
            {Object.values(unplacedRaspberryPis).map((device) => (
              <option key={device._id} value={device.name}>
                {device.name}
              </option>
            ))}
          </select>

          <button onClick={addNode}>{t('add-node')}</button>
        </div>
      )}
      {editMode && mode === 'node' && selectedPoint && !isAddingNode && (
        <div style={{ position: 'absolute', top: eventClick.clientY, left: eventClick.clientX }}>
          <input type="text" value={idInput} onChange={(e) => setIdInput(e.target.value)} placeholder="ID" />
          <button onClick={updateNode}>{t('modify')}</button>
          <button onClick={deleteNode}>{t('delete')}</button>
          <button onClick={resetEdges}>{t('reset-edges')}</button>
        </div>
      )}

    </div>
  );
}
