import {Box, Button, Dialog} from "@mui/material";
import {useEffect, useState} from "react";
import {CommonQuestionProperties} from "./common";
import {TextareaAutosize} from "@mui/core";
import {SimpleQuestionType} from "./SimpleQuestion";
import {useTranslation} from "react-i18next";
import TagsChoice from "./TagsChoice";
import {APITag} from "../APIObjects";
import {APIRequest, RESTMethod} from "../../API";

export interface TextQuestionInterface extends CommonQuestionProperties {
    initialValue: string,
    tags: number[]
}

function TextQuestion(props: {
    questionData: TextQuestionInterface,
    onChange: (arg0: TextQuestionInterface) => void,
    questionType: SimpleQuestionType
}): JSX.Element {
    let questionData: TextQuestionInterface = props.questionData
    const [value, setValue] = useState(questionData)
    const [text, setText] = useState(questionData.initialValue)
    const [tagsText, setTagsText] = useState("")
    const [tagsOpen, setTagsOpen] = useState(false)

    const { t } = useTranslation('translation', { keyPrefix: 'response' })

    const uploadTags = async () => {
        let current_text = ""
        console.log(value.tags)
        for (const tag of value.tags) {
            let resp = await APIRequest(RESTMethod.GET, "/tags", {id: tag}) as APITag
            console.log(resp)
            current_text = current_text + (current_text.length > 0 ? "; " : "") + (resp.text ? resp.text : "")
            console.log(current_text)
        }
        setTagsText(current_text)
    }

    useEffect(() => {
        console.log("useEffect", value)
        setValue(props.questionData)
        setText(props.questionData.initialValue)
        uploadTags().then(() => {console.log("Tags uploaded")})
    }, [props.questionData])
    console.log(props.questionData.question_id.toString() + ": " + questionData.label)
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
            <div>
                <p>{tagsText}</p><br/>
                <Button variant='contained' onClick={() => {
                setTagsOpen(true)
            }}>{t('edit-tags')}</Button></div> : null
        }
        { props.questionType === 'LONG_TEXT' ?
            <Dialog open={tagsOpen} sx={{ minWidth: 400, minHeight: 200 }}>
                <TagsChoice question_id={props.questionData.question_id} chosenTags={value.tags.map((tag) => (tag))}
                onCancel={() => {
                    setTagsOpen(false)
                }} onSubmit={(newTags: APITag[]) => {
                    console.log(newTags)
                    setTagsOpen(false)
                    let newValue = {...value}
                    newValue.tags = newTags.map(tag => tag.id)
                    console.log(newValue)
                    setValue(newValue)
                    console.log(value)
                    props.onChange(newValue)
                    console.log(value)
                    setTagsText(newTags.map(tag => tag.name.en).join("; "))
                }}/>
            </Dialog> : null}
    </div>
    )
}

export default TextQuestion;