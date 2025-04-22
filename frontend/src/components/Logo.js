import React from 'react';
import logo from '../images/gof_logo.jpg'

const Logo = () => {
    return (
        <div>
        <img
            src={logo}
            alt="logo"
            style={{ width: '200px', height: 'auto' }} // Set your desired width and height here
        />
        </div>
    )
};

export default Logo;