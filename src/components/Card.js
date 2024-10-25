import React from 'react';

const Card = ({ name, selected, idx, position, onSelect}) => {
    
    const renderCard = () => {

        if (onSelect !== null) {
            return (
                <img
                    // idx={idx}
                    src={require(`../images/cards/${name}.png`)}  // Show face-up cards for current user
                    alt={name}
                    className={`card-img ${position}-card ${selected ? 'selected' : ''}`}
                    onClick={() => onSelect(idx)}  // Click handler to toggle selection
                />
            )
        } else {
            return (
                <img
                    // idx={idx}
                    src={require(`../images/cards/${name}.png`)}  // Show face-up cards for current user
                    alt={name}
                    className={`card-img ${position}-card ${selected ? 'selected' : ''}`}
                />
            )
        }
    };
    
    return renderCard();
};

export default Card;
