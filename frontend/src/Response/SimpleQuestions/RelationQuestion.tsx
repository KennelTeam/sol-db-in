import React, {SyntheticEvent, useEffect, useState} from "react"
import { Autocomplete, IconButton, TextField } from '@mui/material'
import { Stack } from "@mui/system"
import { AnswerVariant } from "../../FiltersTablePage/TypedFilters"
import { getObjectsList, makeNewObject } from "../../FiltersTablePage/requests2API"
import { Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Button } from "@mui/material"
import AddIcon from '@material-ui/icons/Add'
import { CommonQuestionProperties } from "./common"
import {APIOption} from "../APIObjects";
import { useTranslation } from "react-i18next"
import { useNavigate } from "react-router-dom"

export interface RelationQuestionProps extends CommonQuestionProperties{
    relType: 'LEADER' | 'PROJECT';
    initialValue: APIOption;
}

export default function RelationQuestion(props: {
        questionData: RelationQuestionProps,
        onChange: (arg0: RelationQuestionProps) => void
    }) {
    const [questionData, setData] = useState(props.questionData)
    const [variants, setVariants] = useState<AnswerVariant[]>([])
    const [value, setValue] = useState<AnswerVariant>(questionData.initialValue as AnswerVariant)
    const [inputValue, setInputValue] = useState<string>(questionData.initialValue ? questionData.initialValue.name : "")
    const [addDialogOpen, setOpen] = useState(false)

    const {t} = useTranslation("translation", { keyPrefix: "dynamic_table" })
    const navigate = useNavigate()

    const handleChange = (event: SyntheticEvent, newValue: string | AnswerVariant | null) => {
        setValue(newValue as AnswerVariant)
        if (newValue && typeof newValue !== 'string') {
            let data = questionData
            data.initialValue = newValue
            data.value = newValue.id
            props.onChange(data)
        }
    }

    const handleInputChange = (event: SyntheticEvent, newInputValue: string | null) => {
        if (newInputValue !== null) {
            setInputValue(newInputValue as string)
        }
    }

    useEffect(() => {
        getObjectsList(questionData.relType, navigate).then((response) => {
            setVariants(response)
        })
    }, [])

    const handleAddObject = () => {
        if (variants.filter((v) => (v.name === inputValue)).length === 0) {
            makeNewObject(navigate, questionData.relType, inputValue).then((newId) => {
                setVariants([...variants, {
                    id: newId,
                    name: inputValue
                }])
                let data = questionData
                data.initialValue = {
                    id: newId,
                    name: inputValue
                }
                data.value = newId
                setData(data)
                props.onChange(data)
                setValue({
                    id: newId,
                    name: inputValue
                })
            })
        }
    }
    let found = variants.filter((v) => (v.name === inputValue)).length > 0
    return (
        <Stack direction="row" spacing={1} alignItems="center" justifyContent="flex-start">
            <Autocomplete
                sx={{ width: 200 }}
                options={variants}
                disableCloseOnSelect
                getOptionLabel={(option) => (typeof option === 'string' ? option : option.name)}
                value={value}
                inputValue={inputValue}
                onChange={handleChange}
                onInputChange={handleInputChange}
                freeSolo
                renderInput={(params) => (
                    <TextField
                        {...params}
                        size="small"
                        sx={{ input: {
                            color: (variants.filter((v) => (v.name === inputValue)).length === 0) ? 'red' : 'inherit'
                        } }}
                        label={questionData.label}
                        inputProps={{
                            ...params.inputProps,
                            autoComplete: 'new-password',
                        }}
                        >
                    </TextField>
                )}
            />
            <IconButton onClick={() => { setOpen(true) }} disabled={variants.filter((v) => (v.name === inputValue)).length > 0}>
                <AddIcon htmlColor={
                    variants.filter((v) => (v.name === inputValue)).length > 0 ? "grey": "green"}
                    fontSize="small"/>
            </IconButton>
            <Dialog
                open={addDialogOpen}
                onClose={() => {
                    setOpen(false)
                }}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
            >
                <DialogTitle id="alert-dialog-title">
                {t("confirm_add_object.title")}
                </DialogTitle>
                <DialogContent>
                <DialogContentText id="alert-dialog-description">
                    {t("confirm_add_object.description")}
                </DialogContentText>
                </DialogContent>
                <DialogActions>
                <Button onClick={() => {
                    setOpen(false)
                }}>{t("confirm_add_object.cancel")}</Button>
                <Button onClick={() => {
                    setOpen(false)
                    handleAddObject()
                }} autoFocus>
                    {t("confirm_add_object.confirm")}
                </Button>
                </DialogActions>
            </Dialog>
        </Stack>
    )
}