import React, { useEffect, useState } from 'react';
import Player from './Player';
import Opponent from './Opponent'
import GameBoard from './GameBoard';
import { Snackbar, Alert } from '@mui/material';
import PlayerActionButton from './PlayerActionButton';

import Scoreboard from './ScoreBoard';

import "../css/game_room.css"
import gameBoardImg from "../images/gameBoard.png";
import styled from 'styled-components';
import PlayDirection from './PlayDirection';
import socket from '../socket';
import { timeoutCallback } from '../socket';

const UserContainer = styled.div`
        position: absolute;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        ${props => (["top", "bottom"].includes(props.$position)) ? "width: 100vw;" : "height: 100vh;"}
        ${props => ("bottom" !== props.$position) ? props.$position + ": 0.5em;" : "bottom:0;"}
`

const playerIdxPositionMap = {
    0: "bottom",
    1: "left",
    2: "top",
    3: "right"
  };



// Need to retrieve nbCards
const GameRoom = ({ currentUserId, roomInfo, gameStatus, userCards, setUserCards, playCards, passTurn, exchangeCard}) => {

    const [openPlayerAlert, setOpenPlayerAlert] = React.useState(false);
    const [alertText, setAlertText] = React.useState("");
    const [alertSeverity, setAlertSeverity] = React.useState("warning");


    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
        return;
        }

        setOpenPlayerAlert(false);
    };

    const displayError = (error) => {
        setAlertText(error);
        setOpenPlayerAlert(true);
    };

    const onSortHand = (sortMethod) => {
        const sortData = {
            user_id : currentUserId,
            sort_method: sortMethod
        }

        socket.emit("card:sort", sortData, timeoutCallback((response) => {
            console.log("Got card:sort:", response);
            if(response.error){
                setAlertSeverity("warning")
                displayError(response.error);
            } else {

                const newCards = response.sort_order.map(index => userCards[index]);
                setUserCards(newCards);
            }
          }, () => {
            setAlertSeverity("error")
            displayError("No response from server");
          }, 2000));
            
    }

    const {roomId, players, roomLeader} = roomInfo;

    console.log("Creating gameRoom", roomInfo, gameStatus)
    
    useEffect(() => {
        document.body.style.overflow = "hidden"
        return () =>     document.body.style.overflow = "auto"
      }, [])

    const selectCard = (index) => {
        console.log("Card selected:", index)
        setUserCards(userCards.map((card) => {
            if (card.idx === index) {
                return { ...card, selected: !card.selected };
            } else {
              return card;
            }
          }));
    }

    const isPlayerTurn = (userId) => {
        return gameStatus.player_to_play === userId;
    }

    

    const buildPlayerDict = (gameStatus, players) => {
        let playerInfoDict = {};
        players.forEach(player => {
            playerInfoDict[player.user_id] = {
                username : player.username,
                nbCards : gameStatus.players_info[player.user_id].nb_cards,
                score: gameStatus.players_info[player.user_id].score,
            }
        });

        return playerInfoDict;
    }

    const userPlayerIdx = players.findIndex(player => player.user_id === currentUserId);


    const renderOpponents = () => {

        if(playersGameInfo.length < 2){
            return null;
        }
        
        return playersGameInfo.map((player, index) => {

            // perform modulo on negative numbers
            const playerPosition = playerIdxPositionMap[(((index - userPlayerIdx) % 4) + 4) % 4]
            
            if(playerPosition !== "bottom"){
                return (
                    <UserContainer $position={playerPosition}>
                        <Opponent 
                            isCurrentPlayerTurn={isPlayerTurn(player.user_id)}
                            username={player.username} 
                            nbCards={player.nbCards} 
                            score={player.score}
                            position={playerPosition} />
                    </UserContainer>)
            } else {
                return null;
            }            

        });
    
    }

    const playersGameInfo =  players.map(player => ({ ...player, 'nbCards': gameStatus.players_info[player.user_id].nb_cards, 'score':gameStatus.players_info[player.user_id].score }))    
    
    const otherPlayers = playersGameInfo.filter(player => player.user_id !== currentUserId);  // Filter out the current user
    const currentPlayer = playersGameInfo.find(player => player.user_id === currentUserId);

    const interRoundInfo = gameStatus.inter_round_info ? gameStatus.inter_round_info : null;
    const cardExchangeInfo = gameStatus.card_exchange_info ? gameStatus.card_exchange_info : null;

    const [showCardExchange, setShowCardExchange] = useState(false);
    const [showGameResults, setShowGameResults] = useState(false);
    const [showInterRoundInfo, setShowInterRoundInfo] = useState(false);



    // Only display card exchange for limited amount of time
    useEffect(() => {
        if (cardExchangeInfo) {
            setShowCardExchange(true);
            setTimeout(() => {
                setShowCardExchange(false);
          }, 6000);
        }
    }, [cardExchangeInfo]);

    // Delay inter round info display to show last hand
    useEffect(() => {
        if (interRoundInfo) {
            setTimeout(() => {
                setShowInterRoundInfo(true);
          }, 2000);
        } else {
            setShowInterRoundInfo(false);
        }
    }, [interRoundInfo]);

    // Show scores at the end of the game
    useEffect(() => {
        if (!gameStatus.game_is_on) {
            
            setTimeout(() => {
                setShowGameResults(true);
          }, 2000);
        }
    }, [gameStatus]);


    console.log("Creating GameRoom:", gameStatus)

    return (

        <div className="game-room">
                        
            <div className="game-board-container">
                    <img src={gameBoardImg} alt="game board" className='game-board-img'/>

                        <GameBoard 
                            showGameResults={showGameResults}
                            lastHand={gameStatus.previous_hand}
                            interRoundInfo={showInterRoundInfo ? interRoundInfo : null}
                            cardExchangeInfo={showCardExchange ? cardExchangeInfo : null}
                            playersInfo={buildPlayerDict(gameStatus, players)}
                            currentUserId={currentUserId}
                        />                  
        
            </div>

            {renderOpponents()}

            {/* Current user at the bottom */}
            <UserContainer $position="bottom">
                <Player 
                    username={currentPlayer.username} 
                    cards={userCards} 
                    score={currentPlayer.score} 
                    position="bottom"
                    onCardSelected={selectCard}
                    isTurnToPlay={gameStatus.player_to_play === currentPlayer.user_id}
                    onSortHand={onSortHand}
                />
                <div className="player-buttons-container">
                { interRoundInfo && interRoundInfo.last_winner === currentUserId ?
                    <PlayerActionButton text="Exchange Card" onClick={() => exchangeCard()}/>
                
                    :
                    <React.Fragment>
                        <PlayerActionButton text="Play" onClick={() => playCards()} 
                                        disabled={showCardExchange  || (!isPlayerTurn(currentUserId)) }/>
                        <PlayerActionButton text="Pass" onClick={() => passTurn()}
                                        disabled={showCardExchange || (!isPlayerTurn(currentUserId))}/>
                    </React.Fragment>
                }
                </div>
            
                <PlayDirection direction={gameStatus.play_direction}/>
            </UserContainer>


            <Snackbar
                anchorOrigin={{vertical: "bottom", horizontal:"right"}}
                open={openPlayerAlert}
                autoHideDuration={2000}
                onClose={handleClose}>
                    <Alert severity={alertSeverity} variant="filled">{alertText}</Alert>
            </Snackbar>

            
        </div>
    );
};

export default GameRoom;
