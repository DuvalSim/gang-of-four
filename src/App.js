import React, { useState, useEffect } from 'react';
import socket from './socket';  // Import the existing socket instance
import GameBoard from './components/GameBoard';
import GameStatus from './components/GameStatus';
import Hand from './components/Hand';
import ErrorDisplay from './components/ErrorDisplay';
import HomePage from './components/HomePage';
import GameRoom from './components/GameRoom';
import RoomInfo from './components/RoomInfo';
import WaitingRoom from './components/WaitingRoom';
import Scoreboard from './components/ScoreBoard';

const App = () => {
    const [roomId, setRoomId] = useState(null);
    const [roomInfo, setRoomInfo] = useState(null);
    const [gameStatus, setGameStatus] = useState(null);
 
    const [errorMessage, setErrorMessage] = useState('');

    const [userCards, setUserCards] = useState([]);

    const [isRoomManager, setIsRoomManager] = useState(false);
    const [clientId, setClientId] = useState(null);

    useEffect(() => {

        console.log("ça rerender", clientId)

        socket.on('connect', () => {
            if(!clientId){
                console.log('Connected with socket ID:', socket.id);
                setClientId(socket.id);
            } else {
                console.log("Reconnected, using previous client Id")
            }
            // Otherwise, keep on using previous clientId
            
        });

        socket.on('game:start', (data) => {
            if (data.error) {
                setErrorMessage(`Error in game creation: ${data.error}`);
            }
        });

        socket.on('room:create', (data) => {
            if (data.error) {
                setErrorMessage('Room creation failed: ' + data.error);
            } else {
                setErrorMessage('');
                setRoomInfo(data)
                setRoomId(data.room_id)

                setIsRoomManager(true);
                console.log('Room created with ID:', data.room_id);
            }
        });

        socket.on('room:join', (data) => {
            if (data.error) {
                setErrorMessage('Room joining failed: ' + data.error);
            } else {
                setErrorMessage('');
                setRoomInfo(data);
                setRoomId(data.room_id);

                setIsRoomManager(false);
                console.log('Joined room:', data.room_id);
            }
        });

        socket.on('room:update', (data) => {
            if (data.error) {
                setErrorMessage('Room update failed: ' + data.error);
            } else {
                setRoomInfo(data);
                console.log("Got room info:", data)
            }
        });

        socket.on('game:status', (data) => {
            console.log("Got game status:", data)
            if (data.error) {
                setErrorMessage(`Error in game status: ${data.error}`);
            } else {
                setGameStatus(data);
            }
        });

        // Handle game cards event
        socket.on('game:cards', (data) => {
            console.log("Got game:cards", data)
            if (data.error) {
                setErrorMessage('Error receiving cards: ' + data.error);
            } else {

                setUserCards(data.cards.map((card, idx) => (
                    {
                        name:card,
                        idx: idx,
                        selected: false
                    }))
                );
            }
        });

        socket.on('game:start', (data) => {
            if (data.error) {
                setErrorMessage(`Error in game status: ${data.error}`);
            }
        });

        socket.on('game:play', (data) => {
            console.log("Got game:play:", data);
            if(data.error){
                setErrorMessage('Error while playing:' + data.error)
            } else {
                setErrorMessage('');
                const { player_play, action, cards_played } = data;

                // If it's the current player who played, update their hand
                if (player_play === clientId && action === 'play') {
                    console.log('You played:', cards_played);
                    console.log('current cards:', userCards)
                    const newCards = userCards.filter(card => !card.selected);
                    setUserCards(newCards);
                }
            }            
        });

        socket.on('game:card_exchange', (data) => {
            if (data.error) {

                setErrorMessage('Card exchange failed: ' + data.error);
            }
        });


        return () => {
            // Clean up the socket listeners when the component unmounts
            socket.off('game:status');
            socket.off('game:cards');
            socket.off('room:create');
            socket.off('room:join');
            socket.off('room:update');
            socket.off('game:start');
            socket.off('game:play');
            socket.off('game:card_exchange');
        };
    }, [clientId, userCards]);

    const createRoom = (username) => {        
        socket.emit('room:create', {user_id: socket.id, username: username});
    };

    const joinRoom = (roomId, username) => {
        socket.emit('room:join', { user_id: socket.id, room_id: roomId, username: username });
    };

    const startGame = () => {
        socket.emit('game:start', {room_id: roomId, client_id: clientId})
    }

    const playCards = () => {

        const cardsPlayed = userCards.filter(card => card.selected === true);
                                  
        console.log("Cards played", cardsPlayed)

        const playData = {
            room_id: roomId,
            client_id: clientId,
            action: "play",
            cards_played: cardsPlayed.map(card => card.name)
        }

        console.log("Sending play:", playData);

        socket.emit('game:play', playData);
    }

    const passTurn = () => {

        const playData = {
            room_id: roomId,
            client_id: clientId,
            action: "pass",
            cards_played: []
        }

        console.log("Sending pass:", playData);

        socket.emit('game:play', playData);
    }

    const exchangeCard = () => {

        const cardsPlayed = userCards.filter(card => card.selected === true);

        if(cardsPlayed.length !== 1){
            setErrorMessage("Please select exactly 1 card to exchange")
            return
        }

        const exchangeData = {
            room_id : roomId,
            card_to_give : cardsPlayed[0].name,
            client_id : clientId
        }

        console.log("Sending exchange:", exchangeData);

        socket.emit('game:card_exchange', exchangeData);
    }
    

    return (
        <div className="App">
            <h1>Card Game</h1>
            <ErrorDisplay errorMessage={errorMessage} />

            {!roomId ? (<HomePage createRoom={createRoom} joinRoom={joinRoom} setErrorMessage={setErrorMessage} />)
                    :  gameStatus ?  (     
                                    <GameRoom currentUserId={clientId} 
                                    roomInfo={roomInfo}
                                    gameStatus={gameStatus}
                                    setErrorMessage={setErrorMessage}
                                    userCards={userCards}
                                    setUserCards={setUserCards}
                                    playCards={playCards}
                                    passTurn={passTurn}
                                    exchangeCard={exchangeCard}/>)
                    :   roomInfo ? <WaitingRoom currentUserId={clientId} 
                                                roomInfo={roomInfo}
                                                onStartGame={startGame}
                                                isRoomManager={isRoomManager}/>
                    :   null}
            
        </div>
    );
};

export default App;
