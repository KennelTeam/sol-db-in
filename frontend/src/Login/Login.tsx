import { Visibility, VisibilityOff } from '@mui/icons-material';
import { Box, Button, IconButton, InputAdornment, TextField } from '@mui/material';
import { SyntheticEvent, useState} from 'react';
import { useTranslation } from 'react-i18next';
import axios from "axios";


function Login() {
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [isError, setIsError] = useState(false);
  const {t} = useTranslation('translation', { keyPrefix: 'login' });

  function on_submit(e: SyntheticEvent) {
      setIsError(true);
      e.preventDefault();
      const target = e.target as typeof e.target & {
          login: { value: string },
          password: { value: string }
      }
      const request = {
          login: target.login.value,
          password: target.password.value
      }
      axios.post("http://127.0.0.1:5000/login", request)
          .then((r) => {console.log(r)})
  }

  return (
      <Box display="flex" flexDirection="column" alignItems="center" onSubmit={on_submit}>
        <h2>{t('title')}</h2>
        <Box component="form" display="flex" flexDirection="column" alignItems="center">
          <TextField label={t('login')} name="login" sx={{width: "350px", marginBottom: "20px"}}/>
          <TextField
            label={t('password')}
            type={passwordVisible? "text": "password"}
            sx={{width: "350px", marginBottom: isError? "5px" : "20px"}}
            name="password"
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