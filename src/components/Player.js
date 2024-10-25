import React from 'react';
import { useState } from 'react';
import Card from './Card';
// import '../images/cards/*'

const Player = ({ username, cards, nbCards, score, position, onCardSelected }) => {

    const renderPlayerCards = () => {

        console.log("rendering cards", cards);

        if (cards) {
            return cards.map(card => (
                <Card
                    name={card.name}
                    selected={card.selected}
                    idx={card.idx}
                    position={position}
                    onSelect={onCardSelected}
                />
            ));
        }
    };

    return (
        <div className="player">
            <div className={`player-cards ${position}-cards`}>
                {((cards && cards.length > 0) || (nbCards && nbCards > 0))  && renderPlayerCards()}  {/* Display cards if available */}
            </div>
            <p>{username} {score !== undefined ? (`- Score ${score}`) : null} </p>
            
        </div>
    );
};

export default Player;
