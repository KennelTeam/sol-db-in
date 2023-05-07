import { Box, InputLabel, MenuItem, Select, Table, TableCell, TableContainer, TableHead, TableRow, TableBody } from "@mui/material";
import axios from "axios";
import React from "react";
import { useEffect } from "react";
import { useTranslation } from "react-i18next";
import { SERVER_ADDRESS } from "../types/global";

interface FullnessStatisticsEntryInterface {
    name: string;
    count: number;
}

interface FullnessStatisticsInterface {
    max_count: number;
    entries: FullnessStatisticsEntryInterface[];
}


function FullnessStatistics() {
    const [t] = useTranslation('translation', { keyPrefix: "statistics-fullness" });
    const [formType, setFormType] = React.useState('LEADER');
    const [groupBy, setGroupBy] = React.useState('BY_FORM');
    const [statsData, setStatsData] = React.useState<FullnessStatisticsInterface>({ max_count: 0, entries: [] });
    useEffect(() => {
        axios.get(SERVER_ADDRESS + '/fullness_statistics', {
            params: {
                form_type: formType,
                report_type: groupBy,
            },
            withCredentials: true
        }).then((response) => {
            if (response.status !== 200) {
                console.log("Error while fetching fullness statistics", response.status, response.data);
                return;
            }
            const max_count = response.data.max_count;
            const entries: FullnessStatisticsEntryInterface[] = [];
            for (const entry of response.data.statistics) {
                entries.push({ name: entry.name, count: entry.count });
            }
            setStatsData({ max_count: max_count, entries: entries });
        })
    }, [formType, groupBy]);
    return <Box>
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'row',
                justifyContent: 'space-around',
                alignItems: 'center',
            }}
        >
            <Box>
                <InputLabel
                    id="form-type-selector-label"
                    sx={{ display: 'inline-block', marginRight: '10px' }}
                >
                    {t('form-type-selector')}
                </InputLabel>
                <Select
                    labelId='form-type-selector-label'
                    value={formType}
                    onChange={(event) => { setFormType(event.target.value) }}
                >
                    <MenuItem value="LEADER">{t('form-type-leader')}</MenuItem>
                    <MenuItem value="PROJECT">{t('form-type-project')}</MenuItem>
                </Select>
            </Box>
            <Box>
                <InputLabel
                    id="group-by-selector-label"
                    sx={{ display: 'inline-block', marginRight: '10px' }}
                >
                    {t('group-by-selector')}
                </InputLabel>
                <Select
                    labelId='group-by-selector-label'
                    value={groupBy}
                    onChange={(event) => { setGroupBy(event.target.value) }}
                >
                    <MenuItem value="BY_FORM">{t('group-by-form')}</MenuItem>
                    <MenuItem value="BY_QUESTION">{t('group-by-question')}</MenuItem>
                </Select>
            </Box>
        </Box>
        <TableContainer>
            <Table>
                <colgroup>
                    <col style={{ width: '80%' }} />
                    <col style={{ width: '20%' }} />
                </colgroup>
                <TableHead>
                    <TableRow>
                        <TableCell>{t('table-name-column-name')}</TableCell>
                        <TableCell>{t('table-data-column-name')}</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {
                        statsData.entries.map((entry) =>
                            <TableRow>
                                <TableCell>{entry.name}</TableCell>
                                <TableCell>
                                    {Math.round(entry.count / statsData.max_count * 100)}%
                                    ({entry.count} / {statsData.max_count})</TableCell>
                            </TableRow>
                        )}
                </TableBody>
            </Table>
        </TableContainer>
    </Box>
}

export default FullnessStatistics;