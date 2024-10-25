import React from 'react';
import Player from './Player';
import GameBoard from './GameBoard';
import RoomInfo from './RoomInfo';
import GameStatus from './GameStatus';
import PlayerActionButton from './PlayerActionButton';

// Need to retrieve nbCards
const WaitingRoom = ({ currentUserId, roomInfo, onStartGame, isRoomManager }) => {
    const {room_id, players} = roomInfo  
    
    
    const otherPlayers = players.filter(player => player.client_id !== currentUserId);  // Filter out the current user
    const currentPlayer = players.find(player => player.client_id === currentUserId);

    console.log("Creating Waiting Room:", currentUserId, roomInfo, isRoomManager)

    return (
        <div className="game-room">
            {/* Top player */}
            {otherPlayers[0] && (
                <div className="player-container top">
                    <Player 
                    username={otherPlayers[0].username} 
                    position="top" />
                </div>
            )}

            {/* Right player */}
            {otherPlayers[1] && (
                <div className="player-container right">
                    <Player 
                    username={otherPlayers[1].username}
                    position="right" />
                </div>
            )}

            {/* Left player */}
            {otherPlayers[2] && (
                <div className="player-container left">
                    <Player
                    username={otherPlayers[2].username}
                    position="left" />
                </div>
            )}

            {/* Conditionally render RoomInfo or GameStatus */}
            <div className="game-board-container">
                <RoomInfo roomId={room_id} players={players} isRoomManager={isRoomManager} onStartGame={onStartGame} />
           </div>

            {/* Current user at the bottom */}
            <div className="player-container bottom">
                <Player 
                    username={currentPlayer.username} 
                    position="bottom"
                />
            </div>
        </div>
    );
};

export default WaitingRoom;
