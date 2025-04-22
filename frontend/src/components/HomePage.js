import React, { useState } from 'react';
import { TextField, Button, Box, Typography } from '@mui/material';
import Logo from './Logo';
import "../css/home_page.css"

const HomePage = ({ createRoom, joinRoom, setErrorMessage }) => {
    const [usernameInput, setUsernameInput] = useState('');
    const [roomIdInput, setRoomIdInput] = useState('');
    const [inputErrors, setInputErrors ] = useState({username:false, roomId:false});

    const handleJoinRoomClick = () => {

        if ((usernameInput === '') || (roomIdInput === '')){
            setInputErrors({
                username: (usernameInput === ''),
                roomId: (roomIdInput === '')
        });
        } else {
            joinRoom(roomIdInput, usernameInput);
        }
    }

    const handleCreateRoomClick = () => {

        if ((usernameInput === '')){
            setInputErrors({
                username: true,
                roomId: false
            });
        } else {
            createRoom(usernameInput);
        }
    }

    return (

        <div className='HomePage'>       

            <Box 
                display="flex" 
                flexDirection="column" 
                alignItems="center" 
                gap={2} 
                width="100%" 
                maxWidth="300px" 
                mx="auto"
                mt={10}
            >
                <Logo/>
                <TextField
                    value={usernameInput}
                    onChange={(e) => setUsernameInput(e.target.value)}
                    placeholder="Enter username"
                    fullWidth
                    error={inputErrors.username}
                    helperText= {inputErrors.username ? "Username required" : null}
                    required
                />
                
                <Button variant="contained" color="primary" onClick={handleCreateRoomClick} fullWidth>
                    CREATE A GAME
                </Button>
                <Button variant="contained" color="secondary" disabled fullWidth>
                    JOIN A RANDOM GAME (TODO)
                </Button>
                <TextField
                    id = "roomIdInput"
                    value={roomIdInput}
                    onChange={(e) => setRoomIdInput(e.target.value)}
                    placeholder="eg: qjzia5d"
                    fullWidth
                    error={inputErrors.roomId}
                    helperText= {inputErrors.roomId ? "Room code required" : null}
                />
                <Button variant="contained" color="success" onClick={handleJoinRoomClick} fullWidth>
                    JOIN USING CODE
                </Button>
                {/* <Box display="flex" justifyContent="space-between" width="100%" mt={2}>
                    <Button color="error" size="small">How To Play</Button>
                    <Button color="info" size="small">Contact Us</Button>
                    <Button color="inherit" size="small">Changelog</Button>
                    <Button color="inherit" size="small">En</Button>
            </Box> */}
            </Box>
        </div>
    );

};

export default HomePage;