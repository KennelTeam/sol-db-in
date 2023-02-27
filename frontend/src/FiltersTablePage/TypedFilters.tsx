import { Stack } from "@mui/system"
import { MenuItem, Select, SelectChangeEvent, TextField, Typography, FormControlLabel } from "@mui/material";
import React, { ReactNode, useState} from "react";
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker';
import dayjs, { Dayjs } from "dayjs"
import { FormControl, Checkbox, ListItemText, Autocomplete } from "@mui/material";

interface ListChoiceInterface {
    options: string[],
    defaultIdx: number,
    returnValue?: React.Dispatch<string>
}

export function ListChoice({options, defaultIdx, returnValue} : ListChoiceInterface) {
    // makes Select element (drop-down list) with default value options[defaultIdx]
    const [curValue, setValue] = useState(options[defaultIdx])

    const handleChange = (event: SelectChangeEvent<string>, child: ReactNode) : void => {
        setValue(event.target.value)
        if (returnValue !== undefined) {
            returnValue(event.target.value)
        }
    }

    return (
    <Select value={curValue} onChange={handleChange} size="small">
        {options.map((option: string, i: number) => (
            <MenuItem value={option}>{option}</MenuItem>
        ))}
    </Select>
    )
}

export function NumberFilter() {
    return (
        <Stack direction="row" spacing={1}>
            <ListChoice options={['<', '⩽', '=', '⩾', '>', '≠']} defaultIdx={2}/>
            <TextField
                size="small"
                label="Filter value"
                type="number"
                InputLabelProps={{
                    shrink: true,
                }}
            />
        </Stack>
    )
}

export function TextFilter() {
    return (
        <Stack direction="row" spacing={1}>
            <ListChoice options={['equals', 'contains', 'contained in']} defaultIdx={0}/>
            <TextField
                size="small"
                label="Filter value"
                InputLabelProps={{
                    shrink: true,
                }}
            />
        </Stack>
    )
}

export function DateFilter() {

    const [dateFrom, setDateFrom] = React.useState<Dayjs | null>(dayjs)

    const handleChangeFrom = (newDateFrom: Dayjs | null) => {
        setDateFrom(newDateFrom)
      }
    
    const [dateTo, setDateTo] = React.useState<Dayjs | null>(dayjs)

    const handleChangeTo = (newDateTo: Dayjs | null) => {
        setDateTo(newDateTo)
    }

    return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
            <Stack direction="row" spacing={1} alignItems="center" justifyContent="flex-start">
                <Typography variant="overline">FROM:</Typography>
                <DesktopDatePicker
                    label="from"
                    inputFormat="DD.MM.YYYY"
                    value={dateFrom}
                    onChange={handleChangeFrom}
                    renderInput={(params) => <TextField size="small" {...params} />}
                    />
                <Typography variant="overline">TO:</Typography>
                <DesktopDatePicker
                    label="to"
                    inputFormat="DD.MM.YYYY"
                    value={dateTo}
                    onChange={handleChangeTo}
                    renderInput={(params) => <TextField size="small" {...params} />}
                    />
            </Stack>
        </LocalizationProvider>
    )
}

export function ChoiceFilter({variants} : {variants: string[]}) {
    const [checked, setChecked] = React.useState<string[]>([]);

    const handleChange = (event: SelectChangeEvent<string[]>) => {
        setChecked(event.target.value as string[]);
    }

    const MenuProps = {
        PaperProps: {
          style: {
            maxHeight: 250,
            width: 200,
          },
        },
      }

  return (
    <Stack direction="row" spacing={1} alignItems="center" justifyContent="flex-start">
        <Typography variant="overline">HAS CHECKED ONE OF:</Typography>
            <FormControl sx={{ m: 1, minWidth: 120, maxWidth: 300 }}>
                {/* <InputLabel id="demo-mutiple-checkbox-label">Variants</InputLabel> */}
                <Select
                    aria-label="Variants"
                    id="demo-mutiple-checkbox"
                    size="small"
                    multiple
                    value={checked}
                    onChange={handleChange}
                    renderValue={(selected) => selected.join(', ')}
                    MenuProps={MenuProps}
                >
                    {variants.map((name: string) => (
                        <MenuItem key={name} value={name}>
                            <Checkbox checked={checked.indexOf(name) > -1} />
                            <ListItemText primary={name} />
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
    </Stack>
  )
}

export function AutocompleteChoiceFilter({variants} : {variants: string[]}) : JSX.Element {

    return (
        <Stack direction="row" spacing={1} alignItems="center" justifyContent="flex-start">
            <Typography variant="overline">HAS CHECKED ONE OF:</Typography>
                <Autocomplete
                    sx={{ width: 300 }}
                    options={variants}
                    disableCloseOnSelect
                    multiple
                    renderInput={(params) => (
                        <TextField
                            {...params}
                            size="small"
                            inputProps={{
                                ...params.inputProps,
                                autoComplete: 'new-password', // disable autocomplete and autofill
                            }}
                            >
                        </TextField>
                    )}
                />
        </Stack>
    )
}

export function CheckboxFilter() {
    const [checked, setChecked] = useState(true)

    const handleCheck = () => {
        setChecked(!checked)
    }

    return (
        <FormControlLabel control={<Checkbox defaultChecked/>} onClick={handleCheck} label={checked ? "Checked" : "Unchecked"}/>
    )
}
