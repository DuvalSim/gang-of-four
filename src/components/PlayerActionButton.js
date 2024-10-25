// src/components/RoomInfo.js
import { Button } from '@mui/material';
import React from 'react';


const PlayerActionButton = ({ text, onClick, disabled }) => {
    return (
        <div className="player-action-button">
            <Button onClick={onClick}
            variant="contained"
            disabled = {disabled}>{text}</Button>
        </div>
    );
};

export default PlayerActionButton;
