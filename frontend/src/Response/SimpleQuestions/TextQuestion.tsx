import { Box, Button, Dialog, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import { CommonQuestionProperties } from "./common";
import {TextareaAutosize} from "@mui/core";
import { SimpleQuestionType } from "./SimpleQuestion";
import { useTranslation } from "react-i18next";
import TagsChoice from "./TagsChoice";
import { APITag } from "../APIObjects";

export interface TextQuestionInterface extends CommonQuestionProperties {
    initialValue: string,
    tags: APITag[]
}

function TextQuestion(props: {
    questionData: TextQuestionInterface,
    onChange: (arg0: TextQuestionInterface) => void,
    questionType: SimpleQuestionType
}): JSX.Element {
    let questionData: TextQuestionInterface = props.questionData
    const [value, setValue] = useState(questionData)
    const [text, setText] = useState(questionData.initialValue)
    const [tagsOpen, setTagsOpen] = useState(false)

    const { t } = useTranslation('translation', { keyPrefix: 'response' })

    useEffect(() => {
        console.log("useEffect", value)
        setValue(props.questionData)
        setText(props.questionData.initialValue)
    }, [props.questionData])

    return (
    <div>
        <Box
            component={TextareaAutosize}
            display="inline-block"
            sx={{width: "100%"}}
            value={text}
            minRows={3}
            onChange={(event) => {
                let data = value
                data.initialValue = event.target.value
                data.value = data.initialValue
                setText(event.target.value)
                setValue(data)
                props.onChange(value)
            }}
        />
        { props.questionType === 'LONG_TEXT' ?
            <Button variant='contained' onClick={() => {
                setTagsOpen(true)
            }}>{t('edit-tags')}</Button> : null
        }
        { props.questionType === 'LONG_TEXT' ?
            <Dialog open={tagsOpen} sx={{ minWidth: 400, minHeight: 200 }}>
                <TagsChoice chosenTags={props.questionData.tags.map((tag) => (tag.id))}
                onCancel={() => {
                    setTagsOpen(false)
                }} onSubmit={(newTags: APITag[]) => {
                    console.log(newTags)
                    setTagsOpen(false)
                    let newValue = {...value}
                    newValue.tags = [...newTags]
                    console.log(newValue)
                    setValue(newValue)
                    console.log(value)
                    props.onChange(newValue)
                    console.log(value)
                }}/>
            </Dialog> : null}
    </div>
    )
}

export default TextQuestion;