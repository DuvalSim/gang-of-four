import React, { useState, useEffect } from 'react';
import socket from './socket';  // Import the existing socket instance
import ErrorDisplay from './components/ErrorDisplay';
import HomePage from './components/HomePage';
import GameRoom from './components/GameRoom';
import WaitingRoom from './components/WaitingRoom';
import { parseRoomInfo } from './utils/utils';
import { ThemeProvider } from '@emotion/react';
import { testTheme } from './Themes';


const STORAGE_KEYS = {
    CLIENT_ID: 'cardGame_clientId',
    ROOM_ID: 'cardGame_roomId'
};

const App = () => {
    
    const [roomInfo, setRoomInfo] = useState(null);
    const [gameState, setGameState] = useState(null);
 
    const [errorMessage, setErrorMessage] = useState('');

    const [userCards, setUserCards] = useState([]);

    const [clientId, setClientId] = useState(() => localStorage.getItem(STORAGE_KEYS.CLIENT_ID) || null);
    const [roomId, setRoomId] = useState(() => localStorage.getItem(STORAGE_KEYS.ROOM_ID) || null);

    const [showGame, setShowGame] = useState(false);

    const [gameStarted, setGameStarted] = useState(false);

    useEffect(() => {
        if (clientId) localStorage.setItem(STORAGE_KEYS.CLIENT_ID, clientId);
        if (roomId) localStorage.setItem(STORAGE_KEYS.ROOM_ID, roomId);
    }, [clientId, roomId]);

    useEffect(() => {

        function onConnect(){
            if(!clientId || !roomId) {
                console.log('Connected with socket ID:', socket.id);
                setClientId(socket.id);
            } else {
                console.log("Trying to reconnect with id:", clientId, roomId)
                attemptReconnect(clientId, roomId);
            } 
        }

        function onDisconnect(reason) {
            console.log('Disconnected:', reason);
        }

        function onReconnect(data){
            if (data.error) {
                console.log("Could not reconnect:", data)
                // Clear stored data if the room no longer exists
                clearStoredData();
                
            } else {
                setErrorMessage('');
                setRoomInfo(parseRoomInfo(data.room_info));
                setGameState(data.game_state || null);
                if (data.cards) {
                    setUserCards(data.cards.map((card, idx) => ({
                        name: card,
                        idx: idx,
                        selected: false
                    })));
                }
                console.log('Got successful reconnection', data);
            }
        }
        
        socket.on('connect', onConnect);
        socket.on('disconnect', onDisconnect);
        socket.on('room:reconnect', onReconnect);

        return () => {
            socket.off('connect', onConnect);
            socket.off('disconnect', onDisconnect);
            socket.off('room:reconnect', onReconnect);
          };

    },[clientId, roomId])

    useEffect(() => {

        console.log("ça rerender", clientId)

        function onGameStart(data){
            if (data.error) {
                setErrorMessage(`Error in game creation: ${data.error}`);
            } else {
                // La game va commencer
                setGameStarted(true); 
            }
        }

        function onRoomCreate(data){
            if (data.error) {
                setErrorMessage('Room creation failed: ' + data.error);
            } else {
                setErrorMessage('');
                setRoomInfo(parseRoomInfo(data))
                setRoomId(data.room_id)

                console.log('Room created with ID:', data.room_id);
            }
        }

        function onRoomJoin(data){
            if (data.error) {
                setErrorMessage('Room joining failed: ' + data.error);
            } else {
                setErrorMessage('');
                setRoomInfo(parseRoomInfo(data));
                setRoomId(data.room_id);
                console.log('Joined room:', data.room_id);
            }
        }

        function onRoomUpdate(data) {
            if (data.error) {
                setErrorMessage('Room update failed: ' + data.error);
            } else {
                
                setRoomInfo(parseRoomInfo(data));
                setRoomId(data.room_id)
                console.log("Got room info:", data)
            }
        }

        function onGameStatus(data){
            console.log("Got game status:", data)
            if (data.error) {
                setErrorMessage(`Error in game status: ${data.error}`);
            } else {
                setGameState(data);
            }
        }

        function onGameCards(data){
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
        }

        function onPlay(data){
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
        }

        function onCardExchange(data) {
            if (data.error) {

                setErrorMessage('Card exchange failed: ' + data.error);
            }
        }

        socket.on('game:play', onPlay);
        socket.on('game:card_exchange',onCardExchange);
        socket.on('game:cards', onGameCards);
        socket.on('game:status', onGameStatus);
        socket.on('room:update',onRoomUpdate);
        socket.on('room:join', onRoomJoin);
        socket.on('room:create', onRoomCreate);
        socket.on('game:start', onGameStart);


        return () => {
            // Clean up the socket listeners when the component unmounts
            socket.off('game:status', onGameStatus);
            socket.off('game:cards', onGameCards);
            socket.off('room:create', onRoomCreate);
            socket.off('room:join', onRoomJoin);
            socket.off('room:update', onRoomUpdate);
            socket.off('game:start', onGameStart);
            socket.off('game:play', onPlay);
        };
    }, [clientId, userCards]);

    const attemptReconnect = (clientId, roomId) => { 
        if (roomId && clientId) {
            console.log('Attempting to reconnect to room:', roomId);
            socket.emit('room:reconnect', {
                room_id: roomId,
                user_id: clientId
            });
        }
    }

    const createRoom = (username) => {        
        socket.emit('room:create', {user_id: clientId, username: username});
    };

    const joinRoom = (roomId, username) => {
        socket.emit('room:join', { user_id: clientId, room_id: roomId, username: username });
    };

    const startGame = () => {
        socket.emit('game:start', {user_id: clientId})
    }

    const playCards = () => {

        const cardsPlayed = userCards.filter(card => card.selected === true);
                                  
        console.log("Cards played", cardsPlayed)

        const playData = {
            room_id: roomId,
            user_id: clientId,
            action: "play",
            cards_played: cardsPlayed.map(card => card.name)
        }

        console.log("Sending play:", playData);

        socket.emit('game:play', playData);
    }

    const passTurn = () => {

        const playData = {
            room_id: roomId,
            user_id: clientId,
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
            user_id : clientId
        }

        console.log("Sending exchange:", exchangeData);

        socket.emit('game:card_exchange', exchangeData);
    }

    const clearStoredData = () => {
        localStorage.removeItem(STORAGE_KEYS.CLIENT_ID);
        localStorage.removeItem(STORAGE_KEYS.ROOM_ID);
        setClientId(socket.id);
        setRoomId(null);
    };
    

    return (
        <div id="app">
        
        <ThemeProvider theme={testTheme}>
            <ErrorDisplay errorMessage={errorMessage}/>

            {!roomId ? (<HomePage createRoom={createRoom} joinRoom={joinRoom} setErrorMessage={setErrorMessage} />)
                    :  gameState ?  (     
                                    <GameRoom currentUserId={clientId} 
                                    roomInfo={roomInfo}
                                    gameStatus={gameState}
                                    setErrorMessage={setErrorMessage}
                                    userCards={userCards}
                                    setUserCards={setUserCards}
                                    playCards={playCards}
                                    passTurn={passTurn}
                                    exchangeCard={exchangeCard}/>)
                    :   roomInfo ? <WaitingRoom currentUserId={clientId} 
                                                roomInfo={roomInfo}
                                                onStartGame={startGame}/>
                    :   null}
            
        </ThemeProvider>
        </div>
    );
};

export default App;
