import React from 'react';

const ErrorDisplay = ({ errorMessage }) => {
    return errorMessage ? <div className="error">{errorMessage}</div> : null;
};

export default ErrorDisplay;
