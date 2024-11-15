import React from 'react';
import { useState } from 'react';
import Card from './Card';
import { Chip, Avatar } from '@mui/material';
import styled from 'styled-components'
import SortButton from './SortButton';

import { Droppable, DragDropContext, Draggable } from 'react-beautiful-dnd';

const CardWrapper = styled.div`
  overflow: hidden;
  &:last-child {
    overflow: visible;
  }
`;

const PlayerCardWrapper = styled(CardWrapper)`
    position: relative;

    transform: ${props => props.$selected ? 'translateY(-20px)' : 'none'};
    z-index: ${props => props.$selected ? 2 : 1};
    &:hover {
        overflow: visible;
    } 

`;

const CardsContainer = styled.div`
    display: flex;
    width: 100%;
    justify-content: center;
    filter: ${props => props.$highlighted ? "drop-shadow(0 0 20px white)" : ""};
    padding-top: 20px;
    overflow: hidden;
`

const reorder = (list, startIndex, endIndex) => {
  const result = Array.from(list);
  const [removed] = result.splice(startIndex, 1);
  result.splice(endIndex, 0, removed);

  return result;
};


const Player = ({ username, cards, nbCards, score, position, onCardSelected, isTurnToPlay, onSortHand, setUserCards }) => {

    function handleOnDragEnd(result){
      if (!result.destination) {
        return;
      }
  
      if (result.destination.index === result.source.index) {
        return;
      }
  
      const newCards = reorder(
        cards,
        result.source.index,
        result.destination.index
      );

      setUserCards(newCards);
    }

    
    const renderPlayerCards = () => {

        if (cards) {
            return (

                <DragDropContext onDragEnd={handleOnDragEnd}>
                <Droppable droppableId="droppable" direction="horizontal">
                  {(provided, snapshot) => (
                    <CardsContainer
                      ref={provided.innerRef}{...provided.droppableProps}
                      // $highlighted={isTurnToPlay}
                    >
                    
                      {cards.map((card, index) => (
                        <Draggable key={card.idx} draggableId={card.idx.toString()} index={index}>
                          {(provided, snapshot) => (

                            <PlayerCardWrapper
                              ref={provided.innerRef}
                              {...provided.draggableProps}
                              {...provided.dragHandleProps}
                              $selected={card.selected}                                                          
                            >
                              <Card
                                name={card.name}
                                selected={card.selected}
                                idx={card.idx}
                                position={position}
                                onSelect={onCardSelected}
                              />
                            </PlayerCardWrapper>
                          )}
                        </Draggable>
                      ))}
                      {provided.placeholder}
                    </CardsContainer>
                  )}
                </Droppable>
              </DragDropContext>
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
