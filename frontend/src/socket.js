import { io } from 'socket.io-client';

// Create a singleton socket instance and export it
const socketAddress =
  process.env.REACT_APP_ENV === 'production'
    ? 'https://gangoffourbackend.onrender.com' // Replace with your production backend URL
    : 'http://localhost:8000'; // Local backend URL
    
const socket = io(socketAddress);

// Handle connection events
// socket.on('connect', () => {
//     console.log('Connected with socket ID:', socket.id);
// });

socket.on('disconnect', () => {
    console.log('Disconnected from server.');
});

export const timeoutCallback = (onSuccess, onTimeout, timeout) => {
    let called = false;
  
    const timer = setTimeout(() => {
      if (called) return;
      called = true;
      onTimeout();
    }, timeout);
  
    return (...args) => {
      if (called) return;
      called = true;
      clearTimeout(timer);
      onSuccess.apply(this, args);
    }
}

    
export default socket;
