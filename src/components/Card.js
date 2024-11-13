import React from 'react';
import styled from 'styled-components'

const CardWrapper = styled.div`
  overflow: hidden;
  &:last-child {
    overflow: visible;
  }
`;

const PlayerCardWrapper = styled(CardWrapper)`
    position: relative;
    transition: transform 0.1s ease;
    transform: ${props => props.$selected ? 'translateY(-20px)' : 'none'};
    z-index: ${props => props.$selected ? 2 : 1};
    &:hover {
        overflow: visible;
    }
`;

const Card = ({ name, selected, idx, position, onSelect}) => {
    
    const renderCard = () => {

        if (onSelect) {
            return (
                <PlayerCardWrapper $selected={selected} onClick={() => onSelect(idx)}>
                <img
                    idx={idx}
                    src={require(`../images/cards/${name}.png`)}  // Show face-up cards for current user
                    alt={name}
                    className={`card-img ${position}-card`}
                    onClick={() => onSelect(idx)}  // Click handler to toggle selection
                    
                />
                </PlayerCardWrapper>
            )
        } else {
            return (
                <CardWrapper>
                    <img
                        // idx={idx}
                        src={require(`../images/cards/${name}.png`)}  // Show face-up cards for current user
                        alt={name}
                        className={`card-img ${position}-card`}
                    />
                </CardWrapper>
            )
        }
    };
    
    return renderCard();
};

export default Card;
