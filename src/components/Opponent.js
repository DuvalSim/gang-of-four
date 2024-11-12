import React from 'react';
import { useState } from 'react';
import Card from './Card';
import { Chip, Avatar, colors } from '@mui/material';
// import '../images/cards/*'
import styled from 'styled-components'

const CardContainer = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;

    ${props => props.$vertical ? (
        "height: 100%;"
    )
     :  "width: 100%;"}

    filter: ${props => props.$highlighted ? "drop-shadow(0 0 20px white)" 
                                        : props.$blocked ? "grayscale(100) drop-shadow(0px 0px 10px red)"
                                        : "brightness(0.6)"};

`



const NbCardInfo = styled.div`
    position: absolute;
    align-items: center;
`


const Opponent = ({ player, position, isCurrentPlayerTurn }) => {

    const {username, score,nbCards, isBlocked} = player;
    const [showNbCards, setShowNbCards] = useState(false);

    const handleMouseEnter = () => {
        setShowNbCards(true);
    };

    const handleMouseLeave = () => {
        setShowNbCards(false);
    };

    const renderOpponentCards = () => {
        
        return Array.from({length: nbCards}).map((_, index) => (
            <div className={`opponent-card`} key={index}>
                <Card
                    name='1-M'
                    selected={false}
                    idx={index}
                    position={position}
                    key={index}
                />
            </div>
        ));
    
    };

    return (
        <div className={`player-${position}`}>
            {/* <div> */}

            <CardContainer $vertical={position !== "top"} 
            $highlighted={isCurrentPlayerTurn} 
            $blocked={isBlocked} 
            onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
            

                <div className={`player-cards-${position}`}>
                {(nbCards && nbCards > 0)  && renderOpponentCards()}  {/* Display cards if available */}
                </div>
                {showNbCards && (<NbCardInfo><Chip label={`${nbCards} card${nbCards > 1 ? "s" : ""} left`} color="primary"/></NbCardInfo>)}
            </CardContainer>
                
            {/* </div> */}
                
            
            <div className={`player-info-container-${position}`}>
                <Chip
                    avatar={<Avatar>{username.charAt(0)}</Avatar>}
                    label={username}
                    variant="outlined"
                    color="primary"
                />
                <Chip label={`Score: ${score}`} color='primary' />
            </div>
        </div>
    );
};

export default Opponent;
