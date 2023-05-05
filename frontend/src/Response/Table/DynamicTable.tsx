import { QuestionInterface } from "../Question";
import InputInfo, { InputInfoInterface } from "../SimpleQuestions/InputInfo";
import { WithInputInfoInterface } from "../SimpleQuestions/LabeledQuestion";
import SimpleQuestion, { SimpleQuestionInterface, SimpleQuestionType } from "../SimpleQuestions/SimpleQuestion";
import BaseTable from "./BaseTable";
import {Box, Button, IconButton, Stack} from "@mui/material";
import { Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from "@mui/material"
import {useEffect, useState} from "react";
import AddIcon from "@material-ui/icons/Add"
import DeleteIcon from "@material-ui/icons/Delete"
import ArrowDropUpIcon from '@mui/icons-material/ArrowDropUp'
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown'
import { useTranslation } from "react-i18next";


export interface DynamicTableInterface {
    inputInfos: InputInfoInterface[];
    questions: SimpleQuestionInterface[][];
    sample: SimpleQuestionInterface[];
}

interface DynamicTableWithInputInfoInterface extends DynamicTableInterface, WithInputInfoInterface { }

function DynamicTable(props: { dynamicTableData: DynamicTableInterface, inputInfo: InputInfoInterface, onChange: (arg0: any) => void; }): JSX.Element {
    const [dynamicTableData, setTable] = useState(props.dynamicTableData as DynamicTableWithInputInfoInterface)
    const [a, setA] = useState(dynamicTableData.questions.length)
    const [deleteDialogOpen, setOpen] = useState(false)

    const {t} = useTranslation("translation", { keyPrefix: "dynamic_table" })

    let inputInfoComponents = [
        <div/>, // empty column for sorting buttons
        ...dynamicTableData.inputInfos.map((inputInfo) => {
            return <InputInfo {...inputInfo} />
        })
    ]

    function swapRows(firstIdx: number) {
      const newData = JSON.parse(JSON.stringify(dynamicTableData)) as DynamicTableWithInputInfoInterface
      const buf = JSON.parse(JSON.stringify(newData.questions[firstIdx]))
      newData.questions[firstIdx] = newData.questions[firstIdx + 1]
      newData.questions[firstIdx + 1] = buf
      for (let i = 0; i < newData.questions[firstIdx].length; i++) {
        if (typeof newData.questions[firstIdx][i].questionData.initialValue !== "string") {
          (newData.questions[firstIdx][i].questionData.initialValue as { table_row: number })
              .table_row = firstIdx
        }
        if (typeof newData.questions[firstIdx + 1][i].questionData.initialValue !== "string") {
          (newData.questions[firstIdx + 1][i].questionData.initialValue as { table_row: number })
              .table_row = firstIdx + 1
        }
      }
      console.log("NEW DATA:", newData)
      setTable(newData)
    }

    const makeQuestionComponents = () => (
      dynamicTableData.questions.map((quetionsDataRow, idx) =>
      [
        <Stack direction="column">
          { idx !== 0 ?
            <IconButton onClick={() => {
              console.log("Move Up:", idx)
              swapRows(idx - 1)
            }}>
              <ArrowDropUpIcon/>
            </IconButton> : null
          }
          { idx !== a - 1 ?
            <IconButton onClick={() => {
              console.log("Move Down:", idx)
              swapRows(idx)
            }}>
              <ArrowDropDownIcon/>
            </IconButton> : null
          }
        </Stack>,
        ...quetionsDataRow.map((question) => <SimpleQuestion questionData={question} onChange={props.onChange} />)
      ]
  ))

    let questionComponents = makeQuestionComponents()

    console.log("REDRAW")

    useEffect(() => {
      questionComponents = makeQuestionComponents()
    })

    const addRow = () => {
        console.log("here")
        let data = dynamicTableData
        data.questions.push(JSON.parse(JSON.stringify(dynamicTableData.sample)))
        for (let i = 0; i < dynamicTableData.sample.length; ++i) {
            data.questions[data.questions.length - 1][i].questionData.table_row = data.questions.length - 1
        }
        setA(a + 1)
        setTable(data)
    }

    const removeRow = () => {
        if (a > 0) {
            for (let question of dynamicTableData.questions[dynamicTableData.questions.length - 1]) {
                question.questionData.deleted = true
                props.onChange(question.questionData)
            }
            let data = dynamicTableData
            data.questions.pop()
            setA(a - 1)
            setTable(data)
        }
    }

    return <Box>
        <BaseTable inputInfo={props.inputInfo} rows={[inputInfoComponents].concat(questionComponents)} />
        <IconButton onClick={addRow}>
            <AddIcon htmlColor="green"/>
        </IconButton>
        <IconButton disabled={questionComponents.length === 0} onClick={() => {
            setOpen(true)
        }}>
            <DeleteIcon htmlColor={questionComponents.length ? "red" : "grey"}/>
        </IconButton>
        <Dialog
        open={deleteDialogOpen}
        onClose={() => {
            setOpen(false)
        }}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          {t("confirm_delete.title")}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            {t("confirm_delete.description")}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {
            setOpen(false)
          }}>{t("confirm_delete.cancel")}</Button>
          <Button onClick={() => {
            setOpen(false)
            removeRow()
          }} autoFocus>
            {t("confirm_delete.confirm")}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
}

export default DynamicTable;