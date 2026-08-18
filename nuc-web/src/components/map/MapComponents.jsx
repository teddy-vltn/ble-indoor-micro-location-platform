import React from 'react';
import { Tooltip, Button } from '@mui/material';
import { Edit, ControlCamera, Circle, Save, SwapCalls, Cancel } from '@mui/icons-material';
import { useTranslation } from 'react-i18next';

const Node = ({ point, selectedPoint, draggedNode, isDragging, handlePointClick, handleMouseDown, colorOnline, colorServices, getName }) => {
    return (
        <>
            <g onClick={(e) => handlePointClick(e, point)} onMouseDown={(e) => handleMouseDown(e, point)} style={{ cursor: 'pointer' }}>
                {selectedPoint && selectedPoint.id === point.id && (
                <circle cx={point.x} cy={point.y} r="15" fill="blue" opacity="0.2" />
                )}
                {isDragging && draggedNode && draggedNode.id === point.id && (
                <circle cx={point.x} cy={point.y} r="15" fill="blue" opacity="0.2" />
                )}
                <circle cx={point.x} cy={point.y} r="12" fill={colorOnline(point.id)} />
                <circle cx={point.x} cy={point.y} r="9" fill={colorServices(point.id)} />
                <text className='skipEvent' x={point.x} y={point.y} textAnchor="middle" dy=".3em" fill="white" fontSize={"12px"}>{point.id}</text>
            </g>
            <text x={point.x} y={point.y} textAnchor="middle" dy="-2.5em" stroke="white" strokeWidth={"2px"} fontSize={"6px"}>{getName(point.id)}</text>
            <text x={point.x} y={point.y} textAnchor="middle" dy="-2.5em" fill="black" fontSize={"6px"}>{getName(point.id)}</text>
        </>
    );
};
    
const Edge = ({ edge, points, thickness}) => {
    const startPoint = points.find(p => p.id === edge.from);
    const endPoint = points.find(p => p.id === edge.to);

    return (
        <line x1={startPoint.x} y1={startPoint.y} x2={endPoint.x} y2={endPoint.y} stroke="rgb(170, 170, 170)" strokeWidth={3 * thickness} />
    );
};
  
const Toolbar = ({ editMode, setEditMode, setMode, saveGraph }) => {
    const { t } = useTranslation();
    return (
        <>
            <Tooltip title={editMode ? t('exit-edition-mode') : t('enter-edition-mode')} placement="bottom">
                <Button onClick={() => setEditMode(!editMode)}>
                {editMode ? <Cancel /> : <Edit />}
                </Button>
            </Tooltip>
            {editMode && (
                <> 
                    <Tooltip title={t('move-a-node')} placement="bottom">
                        <Button onClick={() => setMode('move')}>
                        <ControlCamera />
                        </Button>
                    </Tooltip>
                    <Tooltip title={t('add-or-modify-node')} placement="bottom">
                        <Button onClick={() => setMode('node')}>
                        <Circle />
                        </Button>
                    </Tooltip>
                    <Tooltip title={t('add-edge')} placement="bottom">
                        <Button onClick={() => setMode('edge')}>
                        <SwapCalls />
                        </Button>
                    </Tooltip>
                    <Tooltip title={t('save')} placement="bottom">
                        <Button onClick={saveGraph}>
                        <Save />
                        </Button>
                    </Tooltip>
                </>
            )}
        </>
    );
};
  
export { Node, Edge, Toolbar };
  
  
  
  