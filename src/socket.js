import { io } from 'socket.io-client';

// Create a singleton socket instance and export it
const socket = io('http://localhost:5000');

// Handle connection events
// socket.on('connect', () => {
//     console.log('Connected with socket ID:', socket.id);
// });

socket.on('disconnect', () => {
    console.log('Disconnected from server.');
});

    
export default socket;
