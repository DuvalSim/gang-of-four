// src/components/RoomInfo.js
import { Button, useTheme } from '@mui/material';
import React from 'react';


const PlayerActionButton = ({ text, onClick, disabled, isClicked }) => {
    const theme = useTheme();
    return (
        <div className="player-action-button">
            <Button 

            color={isClicked ? "secondary" : "primary" }
            // sx={{
            //     '&:hover': {
            //     backgroundColor: isClicked 
            //         ? theme.palette.secondary.dark 
            //         : theme.palette.primary.dark,
            //     },
            // }}
            onClick={onClick}
            variant="contained"
            disabled = {disabled}
            fullWidth
            className='player-action-button'>{text}</Button>
        </div>
    );
};

export default PlayerActionButton;
