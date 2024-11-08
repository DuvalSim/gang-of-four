import { Grid2, Typography, Button } from "@mui/material";
import React from "react";
import {TableContainer, Table, TableHead, TableRow, TableCell, TableBody} from "@mui/material";
// import Paper from "@mui/material";

export default function Scoreboard({ currentUserId, players }) {

  return (
    <div>
      <Typography variant="h2" textAlign="center" fontWeight={600} mb={6}>
        Game Finished!!
      </Typography>

      <TableContainer>
      <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
        <TableHead>
          <TableRow>
            <TableCell>Player</TableCell>
            <TableCell align="right">Final Score</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {Object.entries(players).map(([playerId, info], idx) => (
            <TableRow
              key={idx}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {info.username}
              </TableCell>
              <TableCell align="right">{info.score}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>

      <Grid2 container justifyContent="center" mt={6}>
          <Button variant="contained" onClick={() => {}}>Play Again</Button>
      </Grid2>
    </div>
  );
  
}