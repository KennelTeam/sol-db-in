import { Stack } from "@mui/system"
import { MenuItem, Select, SelectChangeEvent, TextField, Typography, FormControlLabel } from "@mui/material"
import React, { ReactNode, SyntheticEvent, useEffect, useState} from "react"
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker'
import dayjs, { Dayjs } from "dayjs"
import { FormControl, Checkbox, ListItemText, Autocomplete } from "@mui/material"
import { useTranslation } from 'react-i18next'

export interface AnswerVariant {
    id: number,
    name: string
}

interface ListChoiceProps {
    options: string[],
    defaultIdx: number,
    returnValue?: (value: string) => void
}

export interface AnswerFilter {
    question_id: number,
    exact_values?: number[] | string[] | boolean[],
    min_value?: number | string,
    max_value?: number | string,
    substring?: string
}

interface FilterProps {
    setFilter: (newValue: AnswerFilter) => void
}

interface MultipleFilterProps extends FilterProps {
    variants: {
        name: string,
        id: number
    }[]
}

export function ListChoice({ options, defaultIdx, returnValue } : ListChoiceProps) {
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

export function NumberFilter({ setFilter } : FilterProps) {

    const [compare, setCompare] = useState('=')
    const [value, setValue] = useState(0)

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setValue(Number(e.target.value))
    }

    useEffect(() => {
        switch (compare) {
            case '=' : {
                setFilter({
                    question_id: 0,
                    exact_values: [value]
                })
                break
            }
            case '⩽' : {
                setFilter({
                    question_id: 0,
                    max_value: value
                })
                break
            }
            case '⩽' : {
                setFilter({
                    question_id: 0,
                    min_value: value
                })
                break
            }
        }
    })

    const changeCompare = (value: string) => {
        setCompare(value)
    }

    return (
        <Stack direction="row" spacing={1}>
            <ListChoice options={['⩽', '=', '⩾']} defaultIdx={2} returnValue={changeCompare}/>
            <TextField
                size="small"
                label="Filter value"
                type="number"
                value={value}
                onChange={handleChange}
                InputLabelProps={{
                    shrink: true,
                }}
            />
        </Stack>
    )
}

export function TextFilter(props : FilterProps) {
    const { t } = useTranslation('translation', { keyPrefix: "filters" })
    const [compare, setCompare] = useState(t('equals'))
    const [value, setValue] = useState('')

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setValue(e.target.value)
    }
    
    useEffect(() => {
        switch (compare) {
            case t('equals') : {
                props.setFilter({
                    question_id: 0,
                    exact_values: [value]
                })
                break
            }
            case t('contains') : {
                props.setFilter({
                    question_id: 0,
                    substring: value
                })
                break
            }
        }
    })

    const changeCompare = (value: string) => {
        setCompare(value)
    }

    return (
        <Stack direction="row" spacing={1}>
            <ListChoice options={[t('equals'), t('contains')]} defaultIdx={0} returnValue={changeCompare}/>
            <TextField
                size="small"
                label={t('filter_value')}
                value={value}
                onChange={handleChange}
                InputLabelProps={{
                    shrink: true,
                }}
            />
        </Stack>
    )
}

export function DateFilter({ setFilter } : FilterProps) {
    const { t } = useTranslation('translation', { keyPrefix: "filters" })

    const [dateFrom, setDateFrom] = React.useState<Dayjs | null>(dayjs)
    const [dateTo, setDateTo] = React.useState<Dayjs | null>(dayjs)

    useEffect(() => {
        setFilter({
            question_id: 0,
            min_value: dateFrom === null ? undefined : dateFrom.format('DD-MM-YYYY'),
            max_value: dateTo === null ? undefined : dateTo.format('DD-MM-YYYY')
        })
    })

    const handleChangeFrom = (newDateFrom: Dayjs | null) => {
        setDateFrom(newDateFrom)
      }

    const handleChangeTo = (newDateTo: Dayjs | null) => {
        setDateTo(newDateTo)
    }

    return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
            <Stack direction="row" spacing={1} alignItems="center" justifyContent="flex-start">
                <Typography variant="overline">{t("from")}</Typography>
                <DesktopDatePicker
                    label="from"
                    inputFormat="DD.MM.YYYY"
                    value={dateFrom}
                    onChange={handleChangeFrom}
                    renderInput={(params) => <TextField size="small" {...params} />}
                    />
                <Typography variant="overline">{t("to")}</Typography>
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

export function ChoiceFilter({ setFilter, variants } : MultipleFilterProps) {
    const { t } = useTranslation('translation', { keyPrefix: "filters" })

    const [checked, setChecked] = React.useState<string[]>([])

    const handleChange = (event: SelectChangeEvent<string[]>) => {
        setChecked(event.target.value as string[])
    }
    
    useEffect(() => {
        setFilter({
            question_id: 0,
            exact_values: checked.map((name: string) => (
                        variants.filter((v: AnswerVariant) => (name === v.name))[0].id
                    ))
        })
    })

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
            <Typography variant="overline">{t('checked_one_of')}</Typography>
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
                        {variants.map((variant: AnswerVariant) => (
                            <MenuItem key={variant.id} value={variant.name}>
                                <Checkbox checked={checked.filter((v: string) => (v === variant.name)).length > 0} />
                                <ListItemText primary={variant.name} />
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
        </Stack>
    )
}

export function AutocompleteChoiceFilter({ variants, setFilter } : MultipleFilterProps) : JSX.Element {
    const { t } = useTranslation('translation', { keyPrefix: "filters" })

    const [checked, setChecked] = React.useState<AnswerVariant[]>([])

    const handleChange = (event: SyntheticEvent, value?: AnswerVariant[]) => {
        setChecked(value as AnswerVariant[])
    }

    useEffect(() => {
        setFilter({
            question_id: 0,
            exact_values: checked.map((v) => (v.id))
        })
    })

    return (
        <Stack direction="row" spacing={1} alignItems="center" justifyContent="flex-start">
            <Typography variant="overline">{t('checked_one_of')}</Typography>
                <Autocomplete
                    sx={{ width: 300 }}
                    options={variants}
                    disableCloseOnSelect
                    multiple
                    getOptionLabel={(option) => (option.name)}
                    value={checked}
                    onChange={handleChange}
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

export function CheckboxFilter({ setFilter } : FilterProps) {
    const { t } = useTranslation('translation', { keyPrefix: "filters" })

    const [checked, setChecked] = useState(true)

    const handleCheck = () => {
        setChecked(!checked)
    }

    useEffect(() => {
        setFilter({
            question_id: 0,
            exact_values: [checked]
        })
    })

    return (
        <FormControlLabel
            control={<Checkbox defaultChecked/>}
            onClick={handleCheck}
            label={checked ? t("checked") : t("unchecked")}/>
    )
}
