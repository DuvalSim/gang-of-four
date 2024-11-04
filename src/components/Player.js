import React from 'react';
import { useState } from 'react';
import Card from './Card';
import { Typography } from '@mui/material';
// import '../images/cards/*'

const Player = ({ username, cards, nbCards, score, position, onCardSelected }) => {

    const renderPlayerCards = () => {

        console.log("rendering cards", cards);

        if (cards) {
            return cards.map(card => (
                <div className='card'>
                <Card
                    name={card.name}
                    selected={card.selected}
                    idx={card.idx}
                    position={position}
                    onSelect={onCardSelected}
                />
                </div>
            ));
        }
    };

    return (
        <div className="player">
            <div className={`player-cards-${position}`}>
                {((cards && cards.length > 0) || (nbCards && nbCards > 0))  && renderPlayerCards()}  {/* Display cards if available */}
            </div>
            <div className="player-info">
                <Typography variant='body1'>{username}</Typography>
                <Typography variant='body2'>Score: {score}</Typography>
            </div>
        </div>
    );
};

export default Player;
