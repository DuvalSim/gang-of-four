import React, { useEffect } from 'react';
import { Snackbar, Alert } from '@mui/material';

const ErrorDisplay = ({ errorMessage }) => {

    const [alertText, setAlertText] = React.useState("");
    const [displayMessage, setDisplayMessage] = React.useState(false);

    useEffect(() => {
        if(errorMessage !== ''){
            setAlertText(errorMessage);
            setDisplayMessage(true);
        } else {
            setDisplayMessage(false);
        }
    }, [errorMessage]);

    const onCloseMessage = () => {
        setDisplayMessage(false);
    }

    return (
        <Snackbar
                anchorOrigin={{vertical: "top", horizontal:"center"}}
                open={displayMessage}
                autoHideDuration={2000}
                onClose={onCloseMessage}
                >
                    <Alert severity={"warning"} variant="filled">{alertText}</Alert>
        </Snackbar>
    )
    
    // errorMessage ? <div className="error">{errorMessage}</div> : null;
};

export default ErrorDisplay;
