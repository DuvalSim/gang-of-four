import React from 'react';
import Scoreboard from './ScoreBoard';
import InterRoundInfo from './InterRoundInfo';
import CardExchangeInfo from './CardExchangeInfo';


const GameBoard = ({ lastHand, interRoundInfo, cardExchangeInfo, playersInfo, currentUserId, showGameResults, currentRound, scoreHistory }) => {

    return (
        <div className='game-board'>
            { showGameResults ? 
                (<Scoreboard currentUserId={currentUserId}
                players={playersInfo} scoreHistory={scoreHistory}
                />)
        
            :  
                    interRoundInfo ? (
                    <React.Fragment>
                        Round End!!!
                        <Scoreboard players={playersInfo} scoreHistory={scoreHistory} currentRound={currentRound}/>
                        <InterRoundInfo playersInfo={playersInfo} interRoundInfo={interRoundInfo}/>
                        
                    </React.Fragment>
                    ) : cardExchangeInfo ? (
                        <CardExchangeInfo
                        playersInfo={playersInfo}
                        cardExchangeInfo={cardExchangeInfo}
                        />
                    ) : lastHand ? (
                        <div className="player-cards-bottom" style={{gap: 2 + 'em'}}>
                        {lastHand.map((card, index) => (
                            <img
                            key={index+"board"}
                            idx={index+"board"}
                            src={require(`../images/cards/${card}.png`)}  // Show face-up cards for current user
                            alt={card}
                            className={`card-img`}
                        />
                        ))}
                    </div>
                    ) : (
                        <p>New cycle -- All combination can be played</p>
                    )
            }
        </div>
    );
};

export default GameBoard;
