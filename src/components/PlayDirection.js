import LoopIcon from '@mui/icons-material/Loop';
import styled from 'styled-components';


// eslint-disable-next-line no-mixed-operators
const PlayDirectionDiv = styled.div`

    transform: ${props => props.$clockwise ? "rotateY(180deg) " : ""} rotate(45deg)  scale(5);
    box-sizing: border-box; /*la width va jusqu'à la bordure et inclue le padding*/
    position: absolute;
    bottom: 6em;
    left: 6em;
    justify-content: center;
    display: flex;
    flex-direction: column;
    align-items: center;

    `

export default function PlayDirection({ direction }) {


    

  return (
    <PlayDirectionDiv $clockwise={direction === "clockwise"}>
      <LoopIcon color='success' fontSize='large' />
    </PlayDirectionDiv>
    
  );
  
}