import {Autocomplete, Box, Button, Checkbox, FormControlLabel, makeStyles, Paper, TextField} from "@mui/material";
import Block from "./Block";
import { ResponseDataInterface } from "./ResponseData";
import {SyntheticEvent, useState} from "react";
import {SimpleQuestionTypesList} from "./SimpleQuestions/SimpleQuestion";
import {postRequest} from "./APIRequests";
import {APIFormState} from "./APIObjects";

interface IndexedData {
    [key: number]: SimpleQuestionTypesList
}


function Response(responseData: ResponseDataInterface): JSX.Element {
    const [name, setName] = useState(responseData.title)
    const [state, setState] = useState(responseData.state.toString())
    const [deleted, setDeleted] = useState(false)

    const onItemChanged = (changedAnswer: SimpleQuestionTypesList) => {
        console.log("ONITEMCHANGED")
        console.log(changedAnswer)
        if (changedAnswer.initialValue !== false && changedAnswer.deleted === true) {
            if (resultData[changedAnswer.uid] !== undefined) {
                delete resultData[changedAnswer.uid]
            }
        } else {
            resultData[changedAnswer.uid] = changedAnswer
        }
    }

    const blocksComponents = responseData.blocks.map(
        (blockData) => {return <Block onChange={onItemChanged} blockData={blockData} />}
    )
    let resultData: IndexedData = []

    const onSubmit = (e: SyntheticEvent) => {
        e.preventDefault()
        console.log("ONSUBMIT")
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
        }).then((response: any) => {
            console.log(response)
        })
    }

    return (<Box>
        <Box>
            <TextField
                size="medium"
                type="text"
                sx={{ display: "block" }}
                label={""}
                value={name}
                onChange={(event) => {
                    setName(event.target.value)
                }}
            />
            <Autocomplete
                disablePortal
                options={[APIFormState.PLANNED.toString(), APIFormState.STARTED.toString(), APIFormState.FINISHED.toString()]}
                value={state.toString()}
                size="small"
                sx={{ display: "block", minWidth: "300px" }}
                renderInput={(params) => <TextField {...params}
                                                    label={"State: "}
                />}
                onChange={(e, val) => {
                    e.preventDefault()
                    setState(val ? val.toString() : "PLANNED")
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