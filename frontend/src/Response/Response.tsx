import {Autocomplete, Box, Button, Checkbox, FormControlLabel, makeStyles, Paper, TextField} from "@mui/material";
import Block from "./Block";
import {ResponseDataInterface} from "./ResponseData";
import {SyntheticEvent, useState} from "react";
import {SimpleQuestionTypesList} from "./SimpleQuestions/SimpleQuestion";
import {postRequest} from "./APIRequests";
import {APIFormState, APIFormType} from "./APIObjects";
import {useTranslation} from "react-i18next";
import { useNavigate } from "react-router-dom";


interface IndexedData {
    [key: string]: SimpleQuestionTypesList
}


function Response(responseData: ResponseDataInterface): JSX.Element {
    const { t } = useTranslation('translation', { keyPrefix: "response" })

    const [name, setName] = useState(responseData.title)
    const [nameParts, setNameParts] = useState([
        name.split(' ')[0],
        name.split(' ')[1],
        name.split(' ').slice(2).join(' ')
    ])
    const [state, setState] = useState(responseData.state.toString())
    const [deleted, setDeleted] = useState(false)

    const navigate = useNavigate()

    const onItemChanged = (changedAnswer: SimpleQuestionTypesList) => {
        console.log("ONITEMCHANGED")
        console.log(changedAnswer)
        let key = changedAnswer.uid.toString() + "/" + changedAnswer.table_row?.toString()
        console.log("onItemChanged: key:", key)
        if (changedAnswer.initialValue !== false && changedAnswer.deleted) {
            if (changedAnswer.deleted === true) {
                if (changedAnswer.id != -1) {
                    resultData[key] = changedAnswer
                } else if (resultData[key] !== undefined) {
                    delete resultData[key]
                }
            }
        } else {
            resultData[key] = {...changedAnswer}
        }
        console.log("onItemChanged: resultData:", resultData)
    }

    const blocksComponents = responseData.blocks.map(
        (blockData) => {return <Block onChange={onItemChanged} blockData={blockData} />}
    )
    let resultData: IndexedData = {}

    const onSubmit = (e: SyntheticEvent) => {
        e.preventDefault()
        console.log("ONSUBMIT")
        console.log(resultData)
        let answers = []
        for (let ans in resultData) {
            console.log(resultData[ans])
            if (resultData[ans].value === undefined) {
                // @ts-ignore
                resultData[ans].value = resultData[ans].initialValue
            }
            if (resultData[ans].initialValue === false) {
                resultData[ans].deleted = true
            } else if (resultData[ans].initialValue === true) {
                resultData[ans].deleted = false
            }
            answers.push(resultData[ans])
        }
        console.log(answers)

        let form_type = responseData.form_type.toString()
        let id = responseData.id

        postRequest("forms", {
            name: name,
            form_type: form_type,
            state: state,
            id: id,
            answers: answers,
            deleted: deleted
        }, navigate).then((response: any) => {
            console.log(response)
        }).then((_) => {
            window.location.reload();
        })
    }

    let nameInput = null
    if (responseData.form_type == APIFormType.LEADER) {
        nameInput = <Box><TextField
            size="medium"
            type="text"
            sx={{ display: "block", m: 2 }}
            label={t('name')}
            value={nameParts[0]}
            onChange={(event) => {
                setNameParts([
                    event.target.value,
                    nameParts[1],
                    nameParts[2]
                ])
                setName(event.target.value + ' ' +
                    nameParts[1] + ' ' +
                    nameParts[2])
            }}
        />
        <TextField
            size="medium"
            type="text"
            sx={{ display: "block", m: 2 }}
            label={t('surname')}
            value={nameParts[1]}
            onChange={(event) => {
                setNameParts([
                    nameParts[0],
                    event.target.value,
                    nameParts[2]
                ])
                setName(nameParts[0] + ' ' +
                    event.target.value + ' ' +
                    nameParts[2])
            }}
        />
        <TextField
            size="medium"
            type="text"
            sx={{ display: "block", m: 2 }}
            label={t('other_name')}
            value={nameParts[2]}
            onChange={(event) => {
                setNameParts([
                    nameParts[0],
                    nameParts[1],
                    event.target.value
                ])
                setName(nameParts[0] + ' ' +
                    nameParts[1] + ' ' +
                    event.target.value)
            }}
        /></Box>
    } else {
        nameInput = <Box><TextField
            size="medium"
            type="text"
            sx={{ display: "block", m: 2 }}
            label={t('name')}
            value={name}
            onChange={(event) => {
                setName(event.target.value)
            }}
        /></Box>
    }

    return (<Box>
        <Box>
            {nameInput}
            <Autocomplete
                disablePortal
                options={[APIFormState.RECOMMENDED.toString(), APIFormState.PLANNED.toString(), APIFormState.FINISHED.toString()]}
                value={state.toString()}
                size="small"
                sx={{ display: "block", minWidth: "300px" }}
                renderInput={(params) => <TextField {...params}
                                                    label={"State: "}
                />}
                onChange={(e, val) => {
                    e.preventDefault()
                    setState(val ? val.toString() : "RECOMMENDED")
                }
                }
            />
            <FormControlLabel
                classes={{

                    label: "width: 100%"
                }
                }
                control={<Checkbox checked={deleted} onChange={(event) => {
                    setDeleted(event.target.checked)
                }} />}
                label={"Deleted "}
                sx={{ whiteSpace: "nowrap" }}
            />
            {blocksComponents}
            <Button variant="contained" onClick={onSubmit}>Submit</Button>
        </Box>
    </Box>)
}

export default Response;