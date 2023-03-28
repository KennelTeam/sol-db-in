import { Visibility, VisibilityOff } from '@mui/icons-material';
import { Box, Button, IconButton, InputAdornment, TextField } from '@mui/material';
import { SyntheticEvent, useState} from 'react';
import { useTranslation } from 'react-i18next';
import { Navigate, useNavigate } from 'react-router-dom'
import { SERVER_ADDRESS } from '../types/global'
import axios, {AxiosResponse} from "axios";
import i18n from "../i18n";
import { UserType } from '../types/global';
import { handleError } from '../FiltersTablePage/requests2API'


enum Status {
    Nothing,
    PasswordMismatch,
    LoginMismatch,
    UnknownError,
    SuccessfulLogIn
}

function Login({ changeUser } : { changeUser: (userType: UserType) => void }) {
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [status, setStatus] = useState(Status.Nothing);
  const {t} = useTranslation('translation', { keyPrefix: 'login' });

  const navigate = useNavigate()

  function processResponse(res: AxiosResponse) {
      switch (res.status) {
          case 200: {
              setStatus(Status.SuccessfulLogIn)
              changeUser(UserType.Admin) // later must be set by response
              break;
          }
          case 400: {
              setStatus(Status.UnknownError)
              break;
          }
          case 403: {
              setStatus(Status.PasswordMismatch)
              break;
          }
          case 404: {
              setStatus(Status.LoginMismatch)
              break;
          }
          default: {
              setStatus(Status.UnknownError)
          }
      }
  }

  function onSubmit(e: SyntheticEvent) {
      e.preventDefault();
      const target = e.target as typeof e.target & {
          login: { value: string },
          password: { value: string }
      }
      const request = {
          login: target.login.value,
          password: target.password.value,
          language: i18n.language
      }

      const config = {
          withCredentials: true,
          validateStatus: function (status: number) {
              return status < 500
          }
      }

      axios.post(SERVER_ADDRESS + "/login", request, config).then(processResponse)
        .catch((error) => {
          console.log(error)
          handleError(navigate, error)
          return error
        })
  }

  function errorBox(text: string, statusCode: Status) {
      return <Box component="p" sx={{'color': 'red', 'display': status == statusCode ? 'block' : 'none'}}>{text}</Box>
  }

  if (status == Status.SuccessfulLogIn) {
      return <Navigate to="/leaders"/>
  }

  return (
      <Box display="flex" flexDirection="column" alignItems="center" onSubmit={onSubmit}>
        <h2>{t('title')}</h2>
        <Box component="form" display="flex" flexDirection="column" alignItems="center">
          <TextField label={t('login')} name="login" sx={{width: "350px", marginBottom: "20px"}}/>
          <TextField
            label={t('password')}
            type={passwordVisible? "text": "password"}
            sx={{width: "350px", marginBottom: status != Status.Nothing? "5px" : "20px"}}
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
          <Box component="p" sx={{'color': 'red', 'display': status == Status.PasswordMismatch ? 'block' : 'none'}}>{t('incorrect-credentials')}</Box>
          <Box component="p" sx={{'color': 'red', 'display': status == Status.UnknownError ? 'block' : 'none'}}>{t('unknown-error')}</Box>
          <Box component="p" sx={{'color': 'red', 'display': status == Status.LoginMismatch ? 'block' : 'none'}}>{t('incorrect-login')}</Box>
          <Button type="submit" variant="contained">Submit</Button>
        </Box>
      </Box>
    )
}

export default Login;