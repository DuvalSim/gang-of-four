import { io } from 'socket.io-client';

const socket =
  (process.env.REACT_APP_ENV === 'production'
    ? io("https://simonduval.fr", {
      path: "/api/gof"
    })
    : io('http://localhost:5000')); 

// Handle connection events
socket.on('connect', () => {
    console.log('Connected with socket ID:', socket.id);
});

socket.on('disconnect', () => {
    console.log('Disconnected from server.');
});

socket.on('error', () => {
  console.log('Connected with socket ID:');
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
