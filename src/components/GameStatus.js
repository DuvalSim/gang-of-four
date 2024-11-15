import React from 'react';

const GameStatus = ({ gameStatus, currentPlayer }) => {
    const { player_to_play, players_info, current_round } = gameStatus;

    return (
        <div>
            <h2>Game Status</h2>
            <p>Player to play: {player_to_play === currentPlayer ? 'You' : player_to_play}</p>
            <p>Current round: {current_round}</p>
            <ul>
                {Object.entries(players_info).map(([playerId, info]) => (
                    <li key={playerId}>
                        Player {playerId}: {info.nb_cards} cards, Score: {info.score}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default GameStatus;
