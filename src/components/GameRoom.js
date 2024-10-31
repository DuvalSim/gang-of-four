import React, { useEffect, useState } from 'react';
import Player from './Player';
import GameBoard from './GameBoard';
import GameStatus from './GameStatus';
import PlayerActionButton from './PlayerActionButton';
import socket from '../socket';
import Scoreboard from './ScoreBoard';




// Need to retrieve nbCards
const GameRoom = ({ currentUserId, roomInfo, setErrorMessage, gameStatus, userCards, setUserCards, playCards, passTurn, exchangeCard}) => {

    // const [gameStatus, setGameStatus] = useState({});

    

    const {roomId, players, roomLeader} = roomInfo

    console.log("Creating gameRoom", roomInfo, gameStatus)
    

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

    // useEffect(() => {
    //     if (showGameResults) {
    //       setTimeout(() => {
    //         setShowGameResults(false);
    //       }, 10000);
    //     }
    //   }, [showGameResults]);


    console.log("Creating GameRoom:", players)

    return (
        <div className="game-room">
            {/* Top player 
            {otherPlayers[0] && (
                <div className="player-container top">
                    <Player 
                    username={otherPlayers[0].username} 
                    nbCards={otherPlayers[0].nbCards} 
                    score={otherPlayers[0].score}
                    position="top" />
                </div>
            )}

            {/* Right player}
            {otherPlayers[1] && (
                <div className="player-container right">
                    <Player 
                    username={otherPlayers[1].username}
                    nbCards={otherPlayers[1].nbCards}
                    score={otherPlayers[1].score}
                    position="right" />
                </div>
            )}

            {/* Left player */}
            {/* {otherPlayers[2] && (
                <div className="player-container left">
                    <Player
                    username={otherPlayers[2].username}
                    nbCards={otherPlayers[2].nbCards}
                    score={otherPlayers[2].score}
                    position="left" />
                </div>
            )} */}

            <div className="game-board-container">
                    {showGameResults ?
                        (<Scoreboard currentUserId={currentUserId}
                            players={buildPlayerDict(gameStatus, players)}
                            />) :
                        (<GameBoard 
                            lastHand={gameStatus.previous_hand}
                            interRoundInfo={showInterRoundInfo ? interRoundInfo : null}
                            cardExchangeInfo={showCardExchange ? cardExchangeInfo : null}
                            playersInfo={buildPlayerDict(gameStatus, players)}
                             />
                        )
                        
                    }
                    
                    
            </div>

            {/* Current user at the bottom */}
            <div className="player-container bottom">
                <Player 
                    username={currentPlayer.username} 
                    cards={userCards} 
                    score={currentPlayer.score} 
                    position="bottom"
                    onCardSelected={selectCard}
                />
            </div>            
            <div className="player-buttons">
                { interRoundInfo && interRoundInfo.last_winner === currentUserId ?
                    <PlayerActionButton text="Exchange Card" onClick={() => exchangeCard()}/>
                
                    :
                    <React.Fragment>
                        <PlayerActionButton text="Play" onClick={() => playCards()} disabled={showCardExchange}/>
                        <PlayerActionButton text="Pass" onClick={() => passTurn()} disabled={showCardExchange}/>
                    </React.Fragment>
                }
            </div>
        </div>
    );
};

export default GameRoom;
