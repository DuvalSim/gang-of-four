import React from 'react';
import { useState } from 'react';
import Card from './Card';
import { Chip, Avatar } from '@mui/material';
import styled from 'styled-components'
import SortButton from './SortButton';

const CardsContainer = styled.div`
    display: flex;
    width: 100%;
    justify-content: center;
    filter: ${props => props.$highlighted ? "drop-shadow(0 0 20px white)" : ""};
    padding-top: 20px;
    overflow: hidden;
`

const Player = ({ username, cards, nbCards, score, position, onCardSelected, isTurnToPlay, onSortHand }) => {


    const renderPlayerCards = () => {

        if (cards) {
            return (
                // <div className={`card ${card.selected ? 'selected' : ''}`} key={card.idx}>
                // </div>
            <CardsContainer $highlighted={isTurnToPlay}>
                {cards.map(card => (
                    
                
                <Card
                    name={card.name}
                    selected={card.selected}
                    idx={card.idx}
                    position={position}
                    onSelect={onCardSelected}
                />
                
            ))}
            </CardsContainer>
        );
        }
    };

    return (
        <div className="player">
            
            {((cards && cards.length > 0) || (nbCards && nbCards > 0))  && renderPlayerCards()}  {/* Display cards if available */}
            
            <div className="player-info-container">
                <Chip
                    avatar={<Avatar>{username.charAt(0)}</Avatar>}
                    label={username}
                    variant="outlined"
                    color="primary"
                />

                <SortButton onSortHand={onSortHand}/>
                
                <Chip label={`Score: ${score}`} color='primary' />
            </div>
        </div>
    );
};

export default Player;
