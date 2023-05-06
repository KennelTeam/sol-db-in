import { Backdrop, Box, Checkbox, CircularProgress, Fab, FormControlLabel, FormGroup, InputLabel, MenuItem, Select } from "@mui/material";
import * as React from 'react';
import { ReactElement } from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { useTranslation } from "react-i18next";
import { SERVER_ADDRESS, UserType } from "../types/global";
import axios from "axios";
import { Add as AddIcon } from "@mui/icons-material";
import { handleError } from "../FiltersTablePage/requests2API";
import { useNavigate } from "react-router-dom";


interface SingleUserData {
  role: UserType;
  comment: string;
  id: number;
  login: string;
  name: string;
  password: string | null;
}

interface CoreUserDialogData {
  userData: SingleUserData;
  message: string | null;
}

interface UserDialogProps extends CoreUserDialogData {
  cancelDialog: () => void;
  saveDialog: (userData: SingleUserData) => void;
}

function deserializeApiRole(role: string): UserType {
  role = role.toLowerCase();
  role = role.charAt(0).toUpperCase() + role.slice(1);  // Capitalize first letter
  return UserType[role as "Admin" | "Editor" | "Intern" | "Guest"];
}

function AddEditUserDialog({ userData, message, cancelDialog, saveDialog }: UserDialogProps): ReactElement {
  const { t } = useTranslation('translation', { keyPrefix: "users" });
  const [newPassword, setNewPassword] = React.useState<string>("");
  const [name, setName] = React.useState<string>(userData.name);
  const [comment, setComment] = React.useState<string>(userData.comment);
  const [role, setRole] = React.useState<UserType>(userData.role);
  const [login, setLogin] = React.useState<string>(userData.login);
  const isNewUser = userData.id === -1;
  return (
    <Dialog open={true}>
      <DialogTitle>{t('dialog.title')}</DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          margin="dense"
          id="username"
          label="Username"
          type="text"
          fullWidth
          variant="standard"
          placeholder="Username"
          value={login}
          onChange={(event) => { setLogin(event.target.value) }}
          disabled={!isNewUser}
        />
        <InputLabel id="role-label" sx={{ display: 'inline-block', marginRight: '10px' }}>{t('role')}</InputLabel>
        <Select
          labelId="role-label"
          id="demo-simple-select"
          value={role}
          label={t('role')}
          onChange={(event) => setRole(event.target.value as UserType)}
        >
          <MenuItem value={UserType.Admin}>{t('dialog.admin')}</MenuItem>
          <MenuItem value={UserType.Editor}>{t('dialog.editor')}</MenuItem>
          <MenuItem value={UserType.Intern}>{t('dialog.intern')}</MenuItem>
          <MenuItem value={UserType.Guest}>{t('dialog.guest')}</MenuItem>
        </Select>
        <TextField
          autoFocus
          margin="dense"
          id="fullName"
          label={t('full-name')}
          type="text"
          fullWidth
          variant="standard"
          value={name}
          placeholder={t('full-name')!!}
          onChange={(event) => setName(event.target.value)}
        />
        <TextField
          autoFocus
          margin="dense"
          id="password"
          label={t('dialog.new-password')}
          type="password"
          fullWidth
          variant="standard"
          placeholder={t('dialog.new-password')!!}
          value={newPassword}
          onChange={(event) => setNewPassword(event.target.value)}
        />
        <TextField
          autoFocus
          margin="dense"
          id="comment"
          label={t('dialog.comment')}
          type="text"
          fullWidth
          variant="standard"
          placeholder={t('dialog.comment')!!}
          multiline
          minRows={2}
          value={comment}
          onChange={(event) => setComment(event.target.value)}
        />
        <Box component="p" sx={{ color: "red" }}>{message}</Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => cancelDialog()}>{t('dialog.cancel')}</Button>
        <Button onClick={() => saveDialog({
          role: role,
          comment: comment,
          id: userData.id,
          login: login,
          name: name,
          password: newPassword
        })}>{t('dialog.save')}</Button>
      </DialogActions>
    </Dialog>
  );
}


interface BasicRowProps {
  userData: SingleUserData;
  openEditDialog: (user: SingleUserData) => void;
  editingDisabled: boolean;
}

function SingleUser({ userData, openEditDialog, editingDisabled }: BasicRowProps) {
  const { t } = useTranslation('translation', { keyPrefix: "users" })

  return (
    <TableRow key={userData.name}>
      <TableCell scope="row">
        {UserType[userData.role]}
      </TableCell>
      <TableCell>{userData.name}</TableCell>
      <TableCell>
        <Button
          onClick={() => { openEditDialog(userData) }}
          disabled={editingDisabled}
        >{
            t('edit')}
        </Button>
      </TableCell>
    </TableRow>
  );
}


function Users() {
  const { t } = useTranslation('translation', { keyPrefix: "users" });
  const [dialogData, setDialogData] = React.useState<CoreUserDialogData | null>(null);
  const [allUsers, setAllUsers] = React.useState<SingleUserData[]>([]);
  const [isLoading, setIsLoading] = React.useState<boolean>(true);
  const [fetchUsers, setFetchUsers] = React.useState<boolean>(true);
  const navigate = useNavigate()

  const reloadUsers = () => {
    if (!fetchUsers) {
      return;
    }
    axios.get(SERVER_ADDRESS + '/users', { withCredentials: true }).then((response) => {
      const allUsersApiData: object[] = response.data;
      console.log('users data', allUsersApiData);
      const apiAllUsers = allUsersApiData.map((apiUserData: any) => {
        const user: SingleUserData = {
          role: deserializeApiRole(apiUserData.role),
          comment: apiUserData.comment,
          id: apiUserData.id,
          login: apiUserData.login,
          name: apiUserData.name,
          password: null,
        }
        return user;
      });
      apiAllUsers.sort((a, b) => b.id - a.id);  // Reverse to show new users on top
      setAllUsers(apiAllUsers);
      setFetchUsers(false);
      setIsLoading(false);
    }).catch((error) => {
      handleError(navigate, error);
    });
  }
  React.useEffect(() => { reloadUsers() });

  const openEditDialog = (user: SingleUserData) => {
    setDialogData({ userData: user, message: null });
  };

  const cancelDialog = () => {
    setDialogData(null);
  };

  const saveDialog = (user: SingleUserData) => {
    if (user.id == -1) {  // Creating new user
      if (user.password === null || user.password.length === 0) {
        setDialogData({ userData: user, message: t('dialog.password-required') });
      } else if (user.login === '') {
        setDialogData({ userData: user, message: t('dialog.login-required') });
      } else if (allUsers.map((user) => user.login).includes(user.login)) {
        setDialogData({ userData: user, message: t('dialog.user-exists') });
      } else {
        setDialogData(null);
        setIsLoading(true);
        axios.post(
          SERVER_ADDRESS + '/users',
          {
            login: user.login,
            password: user.password,
            name: user.name,
            role: UserType[user.role].toUpperCase(),
            comment: user.comment,
          },
          { withCredentials: true },
        ).then((response) => {
          user.id = response.data;
          console.log('New user id: ', user.id, typeof user.id)
          allUsers.splice(0, 0, user);
          setAllUsers(allUsers)
          setIsLoading(false);
        }).catch((error) => {
          handleError(navigate, error);
        })
      }
    } else {  // Editing existing user
      setDialogData(null);
      setIsLoading(true);
      axios.post(
        SERVER_ADDRESS + '/users',
        {
          login: user.login,
          password: user.password,
          name: user.name,
          role: UserType[user.role].toUpperCase(),
          comment: user.comment,
        },
        { withCredentials: true },
      ).then(() => {
        setAllUsers(allUsers.map((u) => u.login === user.login ? user : u));
        setIsLoading(false);
      }).catch((error) => {
        handleError(navigate, error);
      })
    }
  }

  const addUser = () => {
    const initialUserData: SingleUserData = {
      comment: '',
      id: -1,
      login: '',
      name: '',
      password: null,
      role: UserType.Guest,
    }
    setDialogData({ userData: initialUserData, message: null });
  };

  return <Box display="flex" flexDirection="column" alignItems="center">
    <h2>{t('title')}</h2>
    <Backdrop open={isLoading}>
      <CircularProgress color="inherit" />
    </Backdrop>
    <Fab
      variant="extended"
      color="primary"
      size="large"
      sx={{
        bottom: "40px",
        right: "40px",
        position: "fixed",
      }}
      onClick={() => addUser()}
      disabled={isLoading}
    >
      <AddIcon sx={{ mr: 1 }} />
      {t('add-user')}
    </Fab>

    {dialogData === null ? '' : <AddEditUserDialog
      userData={dialogData.userData!!}
      message={dialogData.message}
      cancelDialog={cancelDialog}
      saveDialog={saveDialog}
    />}
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell sx={{ 'fontWeight': 'bold' }}>{t('role')}</TableCell>
            <TableCell sx={{ 'fontWeight': 'bold' }}>{t('full-name')}</TableCell>
            <TableCell align="right"></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {allUsers.map((userData) => (
            <SingleUser userData={userData} openEditDialog={openEditDialog} editingDisabled={isLoading} />
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  </Box>
}

export default Users;
