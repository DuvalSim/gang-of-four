import React from 'react';
import { Snackbar, Alert } from '@mui/material';

const ErrorDisplay = ({ errorMessage }) => {


    return (
        <Snackbar
                anchorOrigin={{vertical: "top", horizontal:"center"}}
                open={errorMessage !== ''}
                autoHideDuration={2000}
                >
                    <Alert severity={"warning"} variant="filled">{errorMessage}</Alert>
            </Snackbar>
    )
    
    // errorMessage ? <div className="error">{errorMessage}</div> : null;
};

export default ErrorDisplay;
