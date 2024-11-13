// src/components/RoomInfo.js
import { Button, useTheme } from '@mui/material';
import React from 'react';
import styled from 'styled-components';
import socket from '../socket';
import Scoreboard from './ScoreBoard';

const Root = styled.div`
    position: absolute;
    top: 0;
    right: 0;
    margin: 1em;`

const InterRoundInfo = ({ playersInfo, interRoundInfo }) => {
    // const theme = useTheme();
    const winner = playersInfo.find(player => player.user_id === interRoundInfo.last_winner )
    const looser = playersInfo.find(player => player.user_id === interRoundInfo.last_looser )
    return (
        <div>
        {/* Round end!!! */}
        Waiting for {winner.username} to give card to {looser.username}..
    </div>
    );
};

export default InterRoundInfo;


