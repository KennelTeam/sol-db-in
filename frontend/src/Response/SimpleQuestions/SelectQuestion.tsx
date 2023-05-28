import {
  Autocomplete,
  Box, Button, Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  IconButton,
  TextField
} from "@mui/material";
import { CommonQuestionProperties } from "./common";
import React, {ReactElement, SyntheticEvent, useEffect, useState} from "react";
import {makeNewAnswerOption, makeNewObject} from "../../FiltersTablePage/requests2API";
import {useNavigate} from "react-router-dom";
import AddIcon from "@material-ui/icons/Add";
import {useTranslation} from "react-i18next";
import {Stack} from "@mui/system";

export interface SingleSelectItemInterface {
  id: number;
  name: string | null;
}

export interface SelectQuestionInterface extends CommonQuestionProperties {
  initialValue: string | null; // value
  dataToChooseFrom: Array<SingleSelectItemInterface>;
  answer_block_id: number
}

function SelectQuestion(props: { questionData: SelectQuestionInterface; onChange: (arg0: SelectQuestionInterface) => void; }): JSX.Element {
  let questionData: SelectQuestionInterface = props.questionData
  const [value, setValue] = useState(questionData)
  const [ans, setAns] = useState(questionData.initialValue)
  const [variants, setVariants] = useState(questionData.dataToChooseFrom)
  const navigate = useNavigate()
  const [open, setOpen] = useState(false)
  const {t} = useTranslation("translation", { keyPrefix: "select_question" })

  const handleAddObject = () => {
    console.log(ans)
    console.log(value)
    console.log("THIS")
      makeNewAnswerOption(navigate, questionData.answer_block_id, ans).then((newId) => {
        setVariants([...variants, {
          id: newId,
          name: ans
        }])
        let data = questionData
        data.initialValue = ans
        data.value = newId
        setValue(data)
        props.onChange(data)
      })
  }

  useEffect(() => {
      setValue(props.questionData)
      setAns(props.questionData.initialValue)
  }, [props.questionData])

  let creationalBlock: ReactElement
  if (questionData.answer_block_id != null) {
    creationalBlock = <div><IconButton onClick={() => { setOpen(true) }} disabled={variants.filter((v) => (v.name === ans)).length > 0}>
      <AddIcon htmlColor={
        variants.filter((v) => (v.name === ans)).length > 0 ? "grey": "green"}
               fontSize="small"/>
    </IconButton>
    <Dialog
        open={open}
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

          handleAddObject()
          setOpen(false)
        }} autoFocus>
          {t("confirm_add_object.confirm")}
        </Button>
      </DialogActions>
    </Dialog></div>
  } else {
    creationalBlock = <div/>
  }

  return <Stack direction="row" spacing={1} alignItems="center" justifyContent="flex-start">
      <Autocomplete
        sx={{ width: 200 }}
        disableCloseOnSelect
        disablePortal
        options={variants.sort((a, b) => {
          if (!a.name) {
            return -1
          }
          if (!b.name) {
            return 1
          }
          return a.name > b.name ? 1 : -1
        }).map((x) => x.name)}
        value={ans}
        inputValue={ans ? ans : ""}
        freeSolo
        size="small"
        renderInput={(params) => <TextField {...params}
          label={questionData.label}
          sx={{ input: {
              color: (variants.filter((v) => (v.name === ans)).length === 0) ? 'red' : 'inherit'
            } }}
        />}
        onChange={(e, val) => {
          console.log("On change")
          e.preventDefault()
          let data = value
          data.initialValue = val
          data.value = data.dataToChooseFrom.find((item) => item.name == val)?.id

          setAns(val)
          setValue(data)
          props.onChange(value)
        }
        }
        onInputChange={(event: SyntheticEvent, newInputValue: string | null) => {
          console.log("on Input change")
          setAns(newInputValue)
          let data = value
          data.initialValue = newInputValue
          if (data.dataToChooseFrom.find((item) => item.name == newInputValue) != null) {
            data.value = data.dataToChooseFrom.find((item) => item.name == newInputValue)?.id
            setValue(data)
            props.onChange(value)
          }
        }
        }
      />

      {creationalBlock}
  </Stack>
}

export default SelectQuestion;