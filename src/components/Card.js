import React from 'react';

const Card = ({ name, selected, idx, position, onSelect}) => {
    
    const renderCard = () => {

        if (onSelect) {
            return (
                <img
                    // idx={idx}
                    src={require(`../images/cards/${name}.png`)}  // Show face-up cards for current user
                    alt={name}
                    className={`card-img ${position}-card`}
                    onClick={() => onSelect(idx)}  // Click handler to toggle selection
                    
                />
            )
        } else {
            return (
                    <img
                        // idx={idx}
                        src={require(`../images/cards/${name}.png`)}  // Show face-up cards for current user
                        alt={name}
                        className={`card-img ${position}-card`}
                    />
            )
        }
    };
    
    return renderCard();
};

export default Card;
