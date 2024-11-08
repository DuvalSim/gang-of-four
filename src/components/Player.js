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
`

const Player = ({ username, cards, nbCards, score, position, onCardSelected, isTurnToPlay, onSortHand }) => {


    const renderPlayerCards = () => {

        console.log("rendering cards", cards);

        if (cards) {
            return cards.map(card => (
                <div className={`card ${card.selected ? 'selected' : ''}`} key={card.idx}>
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
            <CardsContainer $highlighted={isTurnToPlay}>
                {((cards && cards.length > 0) || (nbCards && nbCards > 0))  && renderPlayerCards()}  {/* Display cards if available */}
            </CardsContainer>
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
