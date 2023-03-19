import React, {SyntheticEvent, useEffect, useState} from "react"
import { Autocomplete, IconButton, TextField } from '@mui/material'
import { Stack } from "@mui/system"
import { AnswerVariant } from "../../FiltersTablePage/TypedFilters"
import { getObjectsList, makeNewObject } from "../../FiltersTablePage/requests"
import AddIcon from '@material-ui/icons/Add'
import { useTranslation } from "react-i18next"
import { CommonQuestionProperties } from "./common"


export interface RelationQuestionProps extends CommonQuestionProperties{
    relType: 'LEADER' | 'PROJECT'
}

export default function RelationQuestion(props: {
        questionData: RelationQuestionProps,
        onChange: (arg0: number) => void
    }) {
    const questionData : RelationQuestionProps = props.questionData
    const { t } = useTranslation('translation', { keyPrefix: "filters" })
    const [variants, setVariants] = useState<AnswerVariant[]>([])
    const [value, setValue] = useState<AnswerVariant>({ id: -1, name: ""})
    const [inputValue, setInputValue] = useState<string>(value.name)

    const handleChange = (event: SyntheticEvent, newValue: string | AnswerVariant | null) => {
        setValue(newValue as AnswerVariant)
        if (newValue && typeof newValue !== 'string') {
            props.onChange(newValue.id)
        }
    }

    const handleInputChange = (event: SyntheticEvent, newInputValue: string | null) => {
        if (newInputValue !== null) {
            setInputValue(newInputValue as string)
        }
    }

    useEffect(() => {
        getObjectsList(questionData.relType).then((response) => {
            setVariants(response)
        })
    }, [])

    const handleAddObject = () => {
        if (variants.filter((v) => (v.name === inputValue)).length === 0) {
            makeNewObject(questionData.relType).then((newId) => {
                setVariants([...variants, {
                    id: newId,
                    name: inputValue
                }])
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
                            autoComplete: 'new-password', // disable autocomplete and autofill
                        }}
                        >
                    </TextField>
                )}
            />
            <IconButton onClick={handleAddObject}>
                <AddIcon htmlColor="green" fontSize="small"/>
            </IconButton>
        </Stack>
    )
}