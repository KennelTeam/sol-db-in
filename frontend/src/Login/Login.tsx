import { Visibility, VisibilityOff } from '@mui/icons-material';
import { Box, Button, IconButton, InputAdornment, TextField } from '@mui/material';
import { SyntheticEvent, useState} from 'react';
import { useTranslation } from 'react-i18next';
import axios from "axios";


function Login() {
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [isError, setIsError] = useState(false);
  const {t} = useTranslation('translation', { keyPrefix: 'login' });

  async function on_submit(e: SyntheticEvent) {
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
      const res = await axios.post("http://127.0.0.1:5000/login", request, {withCredentials: true})
      console.log(res)
      const req = {
          form_type: "LEADER"
      }
      /*axios.get("http://127.0.0.1:5000/form", {data: req, withCredentials: true})
          .then((r) => {console.log(r)})*/
      /*const response = await fetch("http://127.0.0.1:5000/form", {
          method: "QUERY", // *GET, POST, PUT, DELETE, etc.
          //mode: "cors", // no-cors, *cors, same-origin
          //cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
          credentials: "include", // include, *same-origin, omit
          headers: {
              "Content-Type": "application/json"

              // 'Content-Type': 'application/x-www-form-urlencoded',
          },
          //redirect: "follow", // manual, *follow, error
          //referrerPolicy: "strict-origin", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
          body: JSON.stringify(req), // body data type must match "Content-Type" header
      });
      console.log(response)*/
      axios.request({
          method: "QUERY",
          url: "http://127.0.0.1:5000/form",
          data: req,
          withCredentials: true
      }).then((r) => {console.log(r)})
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