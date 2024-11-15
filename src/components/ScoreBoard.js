import { Grid2, Typography, Button } from "@mui/material";
import React from "react";
import {TableContainer, Table, TableHead, TableRow, TableCell, TableBody} from "@mui/material";
// import Paper from "@mui/material";

export default function Scoreboard({ players, currentRound, scoreHistory }) {

  console.log("Creating Scoreboard", scoreHistory)

  return (
    <div>
      <TableContainer>
      <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
        <TableHead>
          <TableRow>
            <TableCell>Player</TableCell>
            
            {[...Array(currentRound)].map((_, roundIdx) => (
              <TableCell key={roundIdx} align="right">
                Round {roundIdx + 1}
              </TableCell>))
            }
            <TableCell align="right">Total</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {players.sort((player, other) => player.score - other.score).map((player, idx) => (
            <TableRow
              key={idx}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {player.username}
              </TableCell>
              {[...Array(currentRound)].map((_, roundIdx) => (
              <TableCell key={roundIdx} align="right">
                {scoreHistory[player.user_id][roundIdx + 1]}
              </TableCell>))
            }
            <TableCell align="right">{player.score}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
    </div>
  );
  
}