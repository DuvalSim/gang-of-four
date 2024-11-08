import React from 'react';

import Card from './Card';

import styled from 'styled-components'
import Divider from '@mui/material/Divider';

import colorImg from "../images/colors.png"
import rankImg1 from "../images/rank-1.png"
import rankImg2 from "../images/rank-2.png"
import rankImg3 from "../images/rank-3.png"

import {Box} from '@mui/material';
import socket from '../socket';
const boxStyles = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'background-color 0.3s',
    flexGrow: 1,
    cursor: 'pointer',
    '&:hover': {
      bgcolor: 'primary.dark',
    },
  };


const SortButton = ({ onSortHand }) => {

return(
    <Box
        sx={{
            display: 'flex',
            alignItems: 'stretch',
            bgcolor: 'primary.main',
            borderRadius: 1,
            overflow: 'hidden',
        }}
        >
        <Box
            sx={{
                ...boxStyles
              }}
              onClick={() => onSortHand("color")}
        >
            <img alt="colors" src={colorImg} height="30em" width="60em" />
        </Box>

        <Box
            sx={{
            display: 'flex',
            alignItems: 'center',
            }}
        >
            <Divider 
            orientation="vertical" 
            sx={{ 
                bgcolor: 'secondary.main',
                height: '60%', // Adjust this value to control the divider's height
                borderRightWidth: 1.5
            }} 
            />
        </Box>

        <Box 
            sx={{
                ...boxStyles,
                gap: '.3em',
                paddingLeft: ".3em",
                paddingRight: ".3em",
                
            }}
            onClick={() => onSortHand("rank")}
        >
            <img alt="rank" src={rankImg1} height="19em" width="7em" />
            <img alt="rank" src={rankImg2} height="19em" width="12em" />
            <img alt="rank" src={rankImg3} height="19em" width="12em" />
        </Box>
    </Box>
);}

export default SortButton;