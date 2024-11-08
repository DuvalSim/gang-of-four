import React from 'react';
import { Button, Box, Typography, IconButton, Avatar, Badge, Snackbar, Alert } from '@mui/material';
import { ContentCopy, Star } from '@mui/icons-material';
import Grid from '@mui/material/Grid2';

const WaitingRoom = ({ currentUserId, roomInfo, onStartGame }) => {
    const { roomId, players, roomLeader } = roomInfo;

    const [openSnack, setOpenSnack] = React.useState(false);

    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
        return;
        }

        setOpenSnack(false);
    };

    const copyToClipboard = () => {
        navigator.clipboard.writeText(roomId);
        setOpenSnack(true);
    };

    return (
        <div>
            <Snackbar
                anchorOrigin={{vertical: "top", horizontal:"center"}} 
                open={openSnack}
                autoHideDuration={2000}
                onClose={handleClose}>
                    <Alert severity="success" display="flex">Room Id copied to clipboard</Alert>
            </Snackbar>

        <Box
            sx={{
                mt: 8, // Responsive top margin
                px: 3,
                py: 3,
                maxWidth: 400,
                marginX: 'auto', // Centers the Box horizontally
                textAlign: 'center',
                backgroundColor: '#f9f9f9',
                borderRadius: 2,
                boxShadow: 3,
            }}
        >
            {/* Room Code and Message */}
            <Box sx={{ mb: 2 }}>
                <Typography variant="h5" color="textSecondary">
                    Waiting for other players..
                </Typography>
                
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mt: 1 }}>
                    <Typography variant="body1" color="textSecondary">
                        Room Id:
                    </Typography>
                    <Typography variant="body1" component="span" sx={{ mr: 1, ml:4 }}>{roomId}</Typography>
                    <IconButton onClick={copyToClipboard} size="small">
                        <ContentCopy fontSize="small" />
                    </IconButton>
                </Box>
            </Box>

            {/* Players Grid */}
            <Grid container spacing={2} justifyContent="center" sx={{ mb: 3 }}>
                {players.map((player, index) => (
                    <Grid key={index} size={6} display="flex" flexDirection="column" alignItems="center">
                        <Badge
                        overlap="circular"
                        color= {(player.user_id === roomLeader) ? "primary" : ""}
                        anchorOrigin={{vertical:'top', horizontal:'right'}}
                        badgeContent={(player.user_id === roomLeader) ? "Owner" : ""} //<Star color="#FFFF00" />
                        >
                            <Avatar
                                    src={player.avatar}
                                    sx={{
                                        width: 70,
                                        height: 70,
                                        backgroundColor: player.avatar ? 'transparent' : '#eee',
                                    }}
                                >
                                    {!player.avatar && <Typography variant="h4" color="textSecondary">?</Typography>}
                            </Avatar>
                        </Badge>
                        <Typography variant="body2" sx={{ mt: 1, color: player.name ? 'textPrimary' : 'textSecondary' }}>
                            {player.username}
                        </Typography>
                    </Grid>
                ))}
            </Grid>

            {/* Start Game Button and Player Count */}
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                {(currentUserId === roomLeader) ? (<Button
                    variant="contained"
                    color="primary"
                    onClick={onStartGame}
                    disabled={(players.filter(p => p.username).length < 2)}
                >
                    Start Game
                </Button>
                ) : null }
                <Box sx={{ ml: 2 }}>
                    <Typography variant="body1" color="textSecondary">
                        Current players: {players.filter(p => p.username).length}/4
                    </Typography>
                </Box>
            </Box>
        </Box>
        </div>
    );
};

export default WaitingRoom;
