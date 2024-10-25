import React, { useState } from 'react';
import { TextField, Button } from '@mui/material';


const HomePage = ({ createRoom, joinRoom, setErrorMessage }) => {
    const [usernameInput, setUsernameInput] = useState('');
    const [roomIdInput, setRoomIdInput] = useState('');
    // const [errorMessage, setErrorMessage] = useState(null);

    const handleJoinRoomClick = () => {

        if((usernameInput === '') || (roomIdInput === '')){
            setErrorMessage("Missing username or room id")
        } else {
            joinRoom(roomIdInput, usernameInput)
        }
    }

    const handleCreateRoomClick = () => {

        if(usernameInput === ''){
            setErrorMessage("Missing username or room id")
        } else {
            createRoom(usernameInput)
        }
    }

    return (
        <div>
            <Button onClick={handleCreateRoomClick} variant='contained'>Create Room</Button>
            <TextField
            type="text"
            value={usernameInput}
            onChange={(e) => setUsernameInput(e.target.value)}
            placeholder="Enter username"/>

            <TextField
                type="text"
                value={roomIdInput}
                onChange={(e) => setRoomIdInput(e.target.value)}
                placeholder="Enter Room ID to join"
            />
            <Button onClick={handleJoinRoomClick} variant='contained'>Join Room</Button>
            
        </div>
    );

};

export default HomePage;