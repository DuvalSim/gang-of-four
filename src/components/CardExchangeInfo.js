import Card from "./Card";

const CardExchangeInfo = ({ playersInfo, cardExchangeInfo }) => {
    // const theme = useTheme();
    const winner = playersInfo.find(player => player.user_id === cardExchangeInfo.last_winner )
    const looser = playersInfo.find(player => player.user_id === cardExchangeInfo.last_looser )
    return (
        <p>
            Card exchange before round start:  <br/>
            
            {looser.username + ' >> '}
            <Card
                name={cardExchangeInfo.looser_to_winner_card}
                selected={false}
                position="bottom"
                onSelect={null}
            />
            {' >> ' + winner.username}
            
            <br/>
            {winner.username + ' >> '}
            <Card
                name={cardExchangeInfo.winner_to_looser_card}
                selected={false}
                position="bottom"
                onSelect={null}
            />
            {' >> ' + looser.username}
            
        </p>
    );
};

export default CardExchangeInfo;


