import React, { useEffect, useState } from 'react';
import Player from './Player';
import Opponent from './Opponent'
import GameBoard from './GameBoard';
import { Snackbar, Alert } from '@mui/material';
import PlayerActionButton from './PlayerActionButton';

import "../css/game_room.css"
import gameBoardImg from "../images/gameBoard.png";
import styled from 'styled-components';
import PlayDirection from './PlayDirection';
import socket from '../socket';
import { timeoutCallback } from '../socket';
import LeaveRoomButton from './LeaveRoomButton';

const UserContainer = styled.div`
        position: absolute;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        ${props => (["top", "bottom"].includes(props.$position)) ? "width: 100vw;" : "height: 100vh;"}
        ${props => ("bottom" !== props.$position) ? props.$position + ": 0.5em;" : "bottom:0;"}
        ${props => props.$inactive ? "filter: grayscale(1);" : ""}
`

const playerIdxPositionMap = {
    0: "bottom",
    1: "left",
    2: "top",
    3: "right"
  };


// Need to retrieve nbCards
const GameRoom = ({ currentUserId, roomInfo, gameStatus, userCards, setUserCards, playCards, passTurn, exchangeCard, leaveGame}) => {

    const [openPlayerAlert, setOpenPlayerAlert] = React.useState(false);
    const [alertText, setAlertText] = React.useState("");
    const [alertSeverity, setAlertSeverity] = React.useState("warning");

    const [lastCardCallDone, setLastCardCallDone ] = useState(false);

    const {roomId, players, roomLeader} = roomInfo;

    const playersGameInfo =  players.map(player => ({ ...player, 
                                                nbCards : gameStatus.players_info[player.user_id].nb_cards,
                                                score :gameStatus.players_info[player.user_id].score,
                                                isSafe:gameStatus.players_info[player.user_id].safe,
                                                isBlocked:gameStatus.players_info[player.user_id].blocked}))    
    
    const currentPlayer = playersGameInfo.find(player => player.user_id === currentUserId);
    const counterPossible = (playersGameInfo.filter(player => (player.user_id !== currentUserId) 
                                                && (player.nbCards === 1)
                                                && !(player.isBlocked || player.isSafe) ).length > 0);

    const interRoundInfo = gameStatus.inter_round_info ? gameStatus.inter_round_info : null;
    const cardExchangeInfo = gameStatus.card_exchange_info ? gameStatus.card_exchange_info : null;

    const [showCardExchange, setShowCardExchange] = useState(false);
    const [showGameResults, setShowGameResults] = useState(false);
    const [showInterRoundInfo, setShowInterRoundInfo] = useState(false);


    const nbCardsUnselected = userCards.filter(card => !card.selected).length
    // TODO
    const lastCardCallAvailable = (((nbCardsUnselected === 1) || (lastCardCallDone)) && !(currentPlayer.isSafe || currentPlayer.isBlocked));

    // SOCKET HANDLERS:

    useEffect(() => {
        
        function onCallLastCard(data) {
            if (data.error) {
                displayError(data.error, "warning");            
            } else {
                const lastCardUser = data.user_id;
                // Afficher animation
                console.log("USER IS SAFE:", lastCardUser);
            }
        }

        function onCallCounter(data) {
            console.log("Got counter_last_card:", data)
            if (data.error) {
                displayError(data.error, "warning");            
            } else {
                const blockedUsers = data.blocked_players;
                // Afficher animation
                console.log("USER HAS BEEN BLOCKED:", blockedUsers);
            }
        }
    
        socket.on('game:call_last_card', onCallLastCard);
        
        socket.on('game:counter_last_card', onCallCounter);

        return () => {
            socket.off('game:call_last_card', onCallLastCard);
            socket.off('game:counter_last_card', onCallCounter);
        };

    },[])


    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
        return;
        }

        setOpenPlayerAlert(false);
    };

    const displayError = (error, severity="warning") => {
        setAlertSeverity(severity)
        setAlertText(error);
        setOpenPlayerAlert(true);
    };

    const sendCallLastCard = () => {
        console.log("Sending call last card")
        socket.emit("game:call_last_card", {"user_id": currentUserId}, timeoutCallback((response) => {
            console.log("Got call_last_card response:", response);
            if(response.error){
                displayError(response.error, "warning");
            } 
            }, () => {
            displayError("No response from server", "error");
            }, 2000));
    }

    const onPlayCards = () => {
        
        playCards()
        if(lastCardCallDone){
            sendCallLastCard();
            setLastCardCallDone(false);
        }
    }

    const onSortHand = (sortMethod) => {
        const sortData = {
            user_id : currentUserId,
            sort_method: sortMethod, 
            cards: userCards.map(card => card.name)
        }

        socket.emit("card:sort", sortData, timeoutCallback((response) => {
            console.log("Got card:sort:", response);
            if(response.error){
                displayError(response.error, "warning");
            } else {

                const newCards = response.sort_order.map(index => userCards[index]);
                setUserCards(newCards);
            }
          }, () => {
            displayError("No response from server", "error");
          }, 2000));
            
    }
    
    // LAST CARDS FUNCTIONS
    const onCallLastCardClicked = () => {
        console.log("Called last card:", lastCardCallDone, lastCardCallAvailable)
        if(lastCardCallDone){
            setLastCardCallDone(false);
            return
        }

        if(userCards.length === 1){
            // Player already with only 1 card left, send the message right away
            sendCallLastCard();
        } else {
            // Player is about to play and calls before
            setLastCardCallDone(true);
        }

    }

    const onCallCounterClicked = () => {
        console.log("Called counter!!!!")
        if(lastCardCallAvailable){
            displayError("You should better call your last card!!!", "info")
            return
        }
        socket.emit("game:counter_last_card", {"user_id": currentUserId}, timeoutCallback((response) => {
            console.log("Got call_last_card response:", response);
            if(response.error){
                displayError(response.error, "warning");
            } 
            }, () => {
            displayError("No response from server", "error");
            }, 2000));

    }

    console.log("Creating gameRoom", roomInfo, gameStatus)
    
    useEffect(() => {
        document.body.style.overflow = "hidden"
        return () =>     document.body.style.overflow = "auto"
      }, [])

    const selectCard = (index) => {
        console.log("selected")
        setUserCards(userCards.map((card) => {
            if (card.idx === index) {
                return { ...card, selected: !card.selected };
            } else {
              return card;
            }
          }));
        // If a card is selected, reset
        setLastCardCallDone(false);
    }

    const isPlayerTurn = (userId) => {
        return gameStatus.player_to_play === userId;
    }   


    const renderOpponents = () => {

        if(playersGameInfo.length < 2){
            return null;
        }
        
        const userPlayerIdx = players.findIndex(player => player.user_id === currentUserId);
        
        return playersGameInfo.map((player, index) => {

            // perform modulo on negative numbers
            const playerPosition = playerIdxPositionMap[(((index - userPlayerIdx) % 4) + 4) % 4]
            
            if(playerPosition !== "bottom"){
                return (
                    <UserContainer $position={playerPosition} $inactive={!player.active}>
                        <Opponent 
                            isCurrentPlayerTurn={isPlayerTurn(player.user_id)}
                            player={player}
                            position={playerPosition} />
                            
                    </UserContainer>)
            } else {
                return null;
            }            

        });
    
    }
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
                            scoreHistory={gameStatus.score_history}
                            playersInfo={playersGameInfo}
                            currentUserId={currentUserId}

                            // currentRound={gameStatus.current_round}
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
                    setUserCards={setUserCards}
                />
                <div className="player-buttons-container">
                { interRoundInfo && interRoundInfo.last_winner === currentUserId ?
                    <PlayerActionButton text="Exchange Card" onClick={() => exchangeCard()}/>
                
                    :
                    <React.Fragment>
                        <PlayerActionButton text="Play" onClick={() => onPlayCards()} 
                                        disabled={showCardExchange  || (!isPlayerTurn(currentUserId))}/>
                        <PlayerActionButton text="Pass" onClick={() => passTurn()}
                                        disabled={showCardExchange || (!isPlayerTurn(currentUserId))}/>
                        <PlayerActionButton text="Last Card!" onClick={() => onCallLastCardClicked()}
                                        disabled={!(lastCardCallAvailable)} isClicked={lastCardCallDone}/>
                        <PlayerActionButton text="TAPADICARTE!" onClick={() => onCallCounterClicked()}
                                        disabled={!(counterPossible)} isClicked={true}/>
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

            <LeaveRoomButton
            onClick={leaveGame}/>

            
        </div>
    );
};

export default GameRoom;
