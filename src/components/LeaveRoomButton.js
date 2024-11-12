// src/components/RoomInfo.js
import { Button, useTheme } from '@mui/material';
import React from 'react';
import styled from 'styled-components';
import socket from '../socket';

const Root = styled.div`
    position: absolute;
    top: 0;
    right: 0;
    margin: 1em;`

const LeaveRoomButton = ({ onClick }) => {
    // const theme = useTheme();
    
    return (
            <Root>
                <Button 
                    onClick={onClick}
                    variant="contained"
                >Leave Room</Button>
            </Root>
    );
};

export default LeaveRoomButton;
