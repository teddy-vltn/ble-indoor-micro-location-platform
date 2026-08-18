import React, { useRef, useState, useEffect } from 'react';
import './map.css';
import { Node, Edge } from './MapComponents';
import SVGCache from '../../svgCache';
import {
  TransformWrapper,
  TransformComponent,
  useControls
} from "react-zoom-pan-pinch";
import { Fullscreen, ZoomIn, ZoomOut } from '@mui/icons-material';

/**
 * Renders the controls for zooming, resetting the transform, and resetting the map.
 *
 * @return {JSX.Element} The rendered controls component.
 */
const Controls = () => {
  const { zoomIn, zoomOut, resetTransform } = useControls();

  return (
    <div className="tools">
      <button className="greyButton" onClick={() => zoomIn()}><ZoomIn /></button>
      <button className="greyButton" onClick={() => zoomOut()}><ZoomOut /></button>
      <button className="greyButton" onClick={() => resetTransform()}><Fullscreen /></button>
    </div>
  );
};

/**
+ * MapBasic component renders the map with the given nodes and edges.
+ * It also handles the interaction with the map such as zooming and dragging.
+ *
+ * @param {Object} props - The properties passed to the component.
+ * @param {Array} props.edges - The edges to be rendered on the map.
+ * @param {number} props.edgeThickness - The thickness of the edges.
+ * @param {Array} props.points - The nodes to be rendered on the map.
+ * @param {Object} props.selectedPoint - The currently selected node.
+ * @param {Object} props.draggedNode - The node being dragged.
+ * @param {boolean} props.isDragging - Flag indicating if a node is being dragged.
+ * @param {Function} props.handlePointClick - Function to handle click on a node.
+ * @param {Function} props.handleSvgClick - Function to handle click on the map svg.
+ * @param {Function} props.handleMouseDown - Function to handle mouse down on a node.
+ * @param {Function} props.colorOnline - Function to get the color of the online node.
+ * @param {Function} props.colorServices - Function to get the color of the services node.
+ * @param {Function} props.getName - Function to get the name of a node.
+ * @param {string} props.mapImageName - The name of the map image.
+ * @param {Function} props.onTransform - Function to handle transform changes.
+ * @param {ReactNode} props.children - The children components to be rendered.
+ * @param {ReactNode} props.toolsChildren - The children components for the tools.
+ * @returns {ReactNode} The rendered MapBasic component.
+ */
export default function MapBasic({
  edges,
  edgeThickness = 1,
  points,
  selectedPoint,
  draggedNode,
  isDragging = false,
  handlePointClick = () => {},
  handleSvgClick = () => {},
  handleMouseDown = () => {},
  colorOnline = (node) => node ? "grey" : "green",
  colorServices = (node) => node ? "grey" : "green",
  getName = () => "",
  mapImageName,
  children,
  toolsChildren
}) {
  const transformWrapperRef = useRef(null);
  const [viewBox] = useState("0 0 1128 695.7421875");
  const [mapSvgUrl, setMapSvgUrl] = useState(null);

  useEffect(() => {
    if (mapImageName) {
      const svgUrl = SVGCache.getSVGContent(mapImageName);
      if (svgUrl) {
        setMapSvgUrl(svgUrl);
        console.log("Image loaded from cache:", svgUrl);
      } else {
        const defaultSvgUrl = SVGCache.getSVGContent('no-plan.svg');
        setMapSvgUrl(defaultSvgUrl);
        console.log("Default image loaded from cache:", defaultSvgUrl);
      }
    }
  }, [mapImageName]);

  const renderEdges = () => edges.map((edge, index) => (
    <Edge key={index} edge={edge} points={points} thickness={edgeThickness} />
  ));

  const renderNodes = () => points.map((point, index) => (
    <Node
      key={index}
      point={point}
      selectedPoint={selectedPoint}
      draggedNode={draggedNode}
      isDragging={isDragging}
      handlePointClick={handlePointClick}
      handleMouseDown={handleMouseDown}
      colorOnline={colorOnline}
      colorServices={colorServices}
      getName={getName}
    />
  ));

  const renderMapSvg = () => {
    if (!mapSvgUrl) {
      return null;
    }
    return <img key={mapImageName} src={mapSvgUrl} alt="Map" />;
  };

  return (
    <div className='mapContainer'>
      <div className='mapTransformWrapper'>
        <TransformWrapper
          initialScale={1.3}
          limitToBounds={false}
          centerOnInit={true}
        >
          <div className="mapZoomControl">
            <Controls />
          </div>

          <div className="toolsControl">
              <div className='tools'>
                {toolsChildren}
              </div>
          </div>

          <TransformComponent>
          <div className="mapSvg">
              {renderMapSvg()}
              <div className="svgContainer">
                  <svg
                      onClick={handleSvgClick}
                      viewBox={viewBox}
                  >
                      {renderEdges()}
                      {renderNodes()}
                      {children}
                  </svg>
              </div>
          </div>
          
          </TransformComponent>
        </TransformWrapper>
        
      </div>
    </div>
  );
}
