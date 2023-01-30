import { Label, Visibility, VisibilityOff } from '@mui/icons-material';
import { Box, Button, IconButton, InputAdornment, TextField } from '@mui/material';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';


function Login() {
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [isError, setIsError] = useState(false);
  const {t} = useTranslation('translation', { keyPrefix: 'login' });
  return (
      <Box display="flex" flexDirection="column" alignItems="center" onSubmit={(e) => {setIsError(true); e.preventDefault()}}>
        <h2>{t('title')}</h2>
        <Box component="form" display="flex" flexDirection="column" alignItems="center">
          <TextField label={t('login')} sx={{width: "350px", marginBottom: "20px"}}/>
          <TextField
            label={t('password')}
            type={passwordVisible? "text": "password"}
            sx={{width: "350px", marginBottom: isError? "5px" : "20px"}}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={() => {setPasswordVisible(!passwordVisible)}}>
                    {passwordVisible ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              )
            }}
          />
          <Box component="p" sx={{'color': 'red', 'display': isError? 'block' : 'none'}}>{t('incorrect-credentials')}</Box>
          <Button type="submit" variant="contained">Submit</Button>
        </Box>
      </Box>
    )
}

export default Login;