import React, {SyntheticEvent, useEffect, useState} from "react"
import { Autocomplete, IconButton, TextField } from '@mui/material'
import { Stack } from "@mui/system"
import { AnswerVariant } from "../../FiltersTablePage/TypedFilters"
import { getObjectsList, makeNewObject } from "../../FiltersTablePage/requests2API"
import AddIcon from '@material-ui/icons/Add'
import { CommonQuestionProperties } from "./common"
import {APIOption} from "../APIObjects";
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

    return (
        <Stack direction="row" spacing={1} alignItems="center" justifyContent="flex-start">
            <Autocomplete
                sx={{ width: 300 }}
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
                        label={questionData.label}
                        inputProps={{
                            ...params.inputProps,
                            autoComplete: 'new-password',
                        }}
                        >
                    </TextField>
                )}
            />
            <IconButton onClick={handleAddObject} disabled={variants.filter((v) => (v.name === inputValue)).length > 0}>
                <AddIcon htmlColor="green" fontSize="small"/>
            </IconButton>
        </Stack>
    )
}