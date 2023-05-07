import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { useTranslation } from 'react-i18next';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AnswerVariant } from './TypedFilters';
import { getObjectsList } from './requests2API';
import { TextField, Autocomplete, Typography, Button } from '@mui/material';
import React from 'react'
import { Link } from 'react-router-dom';

interface AddObjectPopupProps {
    formType: 'LEADER' | 'PROJECT'
    onSubmit: (name: string) => void
    onCancel: () => void
}

export default function AddObjectPopup(props : AddObjectPopupProps) {
    const [variants, setVariants] = useState<AnswerVariant[]>([])
    const [value, setValue] = useState<AnswerVariant>({name: "", id: -1})
    const [inputValue, setInputValue] = useState<string>("")
    const [exists, setExists] = useState<boolean>(false)

    const navigate = useNavigate()

    const handleChange = (event: React.SyntheticEvent, newValue: string | AnswerVariant | null) => {
        setValue(newValue as AnswerVariant)
        setExists(true)
    }

    const handleInputChange = (event: React.SyntheticEvent, newInputValue: string | null) => {
        if (newInputValue !== null) {
            setInputValue(newInputValue as string)
            if (variants.filter((v) => (v.name === newInputValue)).length === 0) {
                setExists(false)
            }
        }
    }

    useEffect(() => {
        getObjectsList(props.formType, navigate).then((response) => {
            setVariants(response)
        })
    }, [])
    const {t} = useTranslation("translation", { keyPrefix: "filters." + 
                ( props.formType === 'LEADER' ? 'add_leader_dialog' : 'add_project_dialog' )})


    const isExists = (name: string) => (
            variants.filter((v) => (v.name.trim() === name.trim())).length > 0
        )
    
    return (
        <div>
            <DialogTitle>{t('title')}</DialogTitle>
            <DialogContent>
                <DialogContentText>{t('body')}</DialogContentText>
                <Autocomplete
                    sx={{ width: 350, margin: 5 }}
                    options={variants}
                    disableCloseOnSelect
                    getOptionLabel={(option) => (typeof option === 'string' ?
                        option : option.name)}
                    value={value}
                    inputValue={inputValue}
                    onChange={handleChange}
                    onInputChange={handleInputChange}
                    isOptionEqualToValue={(option, value) => (option.name.trim() === value.name.trim())}
                    freeSolo
                    renderInput={(params) => (
                        <TextField
                            {...params}
                            size="small"
                            sx={{ input: {
                                color: isExists(inputValue) ? 'red' : 'green'
                            } }}
                            label={t("input_label")}
                            inputProps={{
                                ...params.inputProps,
                                autoComplete: 'new-password',
                            }}
                            >
                        </TextField>
                    )}
                />
                {isExists(inputValue) ?
                    <div>
                        <Typography color="red">{t("exists")}</Typography>
                        <Link to={(props.formType === 'LEADER' ? '/leader/' : '/project/')
                                + value.id}>{t("follow_page")}</Link>
                    </div>  : null}
            </DialogContent>
            <DialogActions>
                <Button onClick={props.onCancel}>{t("cancel")}</Button>
                <Button disabled={isExists(inputValue) || inputValue.trim() === ""}
                onClick={() => {
                    props.onSubmit(inputValue)
                }}>{t("create")}</Button>
            </DialogActions>
        </div>
    )
}
