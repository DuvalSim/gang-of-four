import React, {useState, useEffect} from 'react';
import Card from './Card';


const GameBoard = ({ lastHand, interRoundInfo, cardExchangeInfo, playersInfo }) => {

    return (
        <div>
            {interRoundInfo ? (
                <p>
                    Round ended. Winner: {playersInfo[interRoundInfo.last_winner].username} <br/>
                    Looser: {playersInfo[interRoundInfo.last_looser].username}.
                    Looser gave {interRoundInfo.looser_to_winner_card} to the winner.<br/>
                    Scores: 
                    <ul>
                    {Object.keys(playersInfo).map(playerId => (<li>{playersInfo[playerId].username}: {playersInfo[playerId].score}</li>))}
                    </ul>
                </p>
            ) : cardExchangeInfo ? (
                <p>
                    Card exchange before round start:  <br/>
                    
                    {playersInfo[cardExchangeInfo.last_looser].username + ' >> '}
                    <Card
                        name={cardExchangeInfo.looser_to_winner_card}
                        selected={false}
                        position="bottom"
                        onSelect={null}
                    />
                    {' >> ' + playersInfo[cardExchangeInfo.last_winner].username}
                    
                    <br/>
                    {playersInfo[cardExchangeInfo.last_winner].username + ' >> '}
                    <Card
                        name={cardExchangeInfo.winner_to_looser_card}
                        selected={false}
                        position="bottom"
                        onSelect={null}
                    />
                    {' >> ' + playersInfo[cardExchangeInfo.last_looser].username}
                    
                </p>
            ) : lastHand ? (
                <div className="hand">
                {lastHand.map((card, index) => (
                    <img
                    idx={index+"board"}
                    src={require(`../images/cards/${card}.png`)}  // Show face-up cards for current user
                    alt={card}
                    className={`card-img bottom-card`}
                />
                ))}
            </div>
            ) : (
                <p>New cycle -- play any combination</p>
            )}
        </div>
    );
};

export default GameBoard;
