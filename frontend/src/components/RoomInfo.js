// src/components/RoomInfo.js
import { Button } from '@mui/material';
import React from 'react';


const RoomInfo = ({ roomId, players, isRoomManager, onStartGame }) => {
    return (
        <div className="room-info">
            <h2>Room ID: {roomId}</h2>
            <h3>Players in the Room:</h3>
            <ul>
                {players.map(player => (
                    <li key={player.client_id}>
                        {player.username}: {player.client_id}
                    </li>
                ))}
            </ul>
            {isRoomManager ? (<Button onClick={onStartGame} className="start-game-button">Start Game</Button>) : null}
        </div>
    );
};

export default RoomInfo;
