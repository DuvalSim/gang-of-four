import React, { useState } from 'react';
import Card from './Card';

const Hand = ({ cards, onCardSelect, playCardsBtn, isInterRoundPhase, playCards }) => {
    const [selectedCards, setSelectedCards] = useState([]);

    const handleSelect = (cardId) => {
        if (selectedCards.includes(cardId)) {
            setSelectedCards(selectedCards.filter(id => id !== cardId));
        } else {
            setSelectedCards([...selectedCards, cardId]);
        }
    };

    const handlePlayCards = () => {
        playCards(selectedCards);
        setSelectedCards([]);
    };

    return (
        <div>
            <h2>Your Cards</h2>
            <div className="hand">
                {cards.map((card, index) => (
                    <Card
                        key={index}
                        card={card}
                        cardId={index}
                        onSelect={handleSelect}
                        isSelected={selectedCards.includes(index)}
                    />
                ))}
            </div>
            <button onClick={handlePlayCards}>
                {isInterRoundPhase ? 'Exchange Card' : playCardsBtn}
            </button>
        </div>
    );
};

export default Hand;
