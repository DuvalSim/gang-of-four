import { Grid2, Typography, Button } from "@mui/material";



export default function Scoreboard({ currentUserId, players }) {

  return (
    <div>
      <Typography variant="h2" textAlign="center" fontWeight={600} mb={6}>
        Game Finished!!
      </Typography>
      {Object.entries(players).map(([playerId, info], idx) => (
        <div className={`row ${playerId === currentUserId && "You"}`} key={idx}>
          <p>{info.username} : {info.score}</p>
        </div>
      ))}
      <Grid2 container justifyContent="center" mt={6}>
          <Button onClick={() => {}}>Play Again</Button>
      </Grid2>
    </div>
  );
  
}