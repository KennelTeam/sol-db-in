import { Box, Checkbox, FormControlLabel, FormGroup, InputLabel, MenuItem, Select } from "@mui/material";
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

interface EditUserProps {
  open: boolean;
  name: string;
  closeDialog: () => void;
}

function EditUserDialog({ open, name, closeDialog }: EditUserProps): ReactElement {
  const { t } = useTranslation('translation', { keyPrefix: "users" });
  const [role, setRole] = React.useState('guest');
  return (
    <Dialog open={open} onClose={closeDialog}>
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
        />
        <InputLabel id="role-label" sx={{display: 'inline-block', marginRight: '10px'}}>Role</InputLabel>
        <Select
          labelId="role-label"
          id="demo-simple-select"
          value={role}
          label={t('role')}
          onChange={(event) => {setRole(event.target.value)}}
        >
          <MenuItem value="editor">{t('dialog.editor')}</MenuItem>
          <MenuItem value="intern">{t('dialog.intern')}</MenuItem>
          <MenuItem value="guest">{t('dialog.guest')}</MenuItem>
        </Select>
        <FormGroup>
        <FormControlLabel
          control={<Checkbox name="isBlocked" />}
          label={t('dialog.block-access')}
        />
        </FormGroup>
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
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={closeDialog}>{t('dialog.cancel')}</Button>
        <Button onClick={closeDialog}>{t('dialog.save')}</Button>
      </DialogActions>
    </Dialog>
  );
}

const rows = [
  {role: 'Editor', fullName: 'Andrusov Nikita Andreevich'},
  {role: 'Intern', fullName: 'Ageevn Nikolay Mikhailovich'},
  {role: 'Guest', fullName: 'Nebolsin Alexey Romanovich'},
  {role: 'Guest', fullName: 'Nilov Lev Evgenyevich'},
];

interface BasicRowProps {
  role: string;
  fullName: string;
  openDialog: (fullName: string) => void;
}

function SingleUser({ role, fullName, openDialog }: BasicRowProps) {
  const { t } = useTranslation('translation', { keyPrefix: "users" })

  return (
    <TableRow key={fullName}>
      <TableCell scope="row">
        {role}
      </TableCell>
      <TableCell>{fullName}</TableCell>
      <TableCell><Button onClick={() => { openDialog(fullName) }}>{t('edit')}</Button></TableCell>
    </TableRow>
  );
}


function Users() {
  const { t } = useTranslation();
  const [name, setName] = React.useState('');

  const openDialog = (fullName: string) => {
    console.log('openDialog', fullName);
    setName(fullName);
  };

  const closeDialog = () => {
    setName('');
  };

  return <Box display="flex" flexDirection="column" alignItems="center">
    <h2>{t('title')}</h2>
    <EditUserDialog open={name !== ''} name={name} closeDialog={closeDialog} />
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
          {rows.map((row) => (
            <SingleUser role={row.role} fullName={row.fullName} openDialog={openDialog} />
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  </Box>
}

export default Users;
