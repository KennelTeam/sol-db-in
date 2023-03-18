import { Accordion, AccordionDetails, AccordionSummary, Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, IconButton, InputLabel, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Paper, TextField } from "@mui/material";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Edit, Remove } from "@mui/icons-material";
import { useTranslation } from "react-i18next";
import { useState } from "react";
import LabeledQuestion from "../Response/SimpleQuestions/LabeledQuestion";
import { SimpleQuestionType } from "../Response/SimpleQuestions/SimpleQuestion";

type Translations = { [language: string]: string };

export interface OptionsListInterface {
    title: Translations;
    options: Array<Translations>;
}

interface EditTranslationsDialogInterface {
    translations: Translations;
    closeDialog: () => void;
    open: boolean;
}

function getTranslation(mapping: Translations, language: string): string {
    var translation = mapping[language];
    if (!translation) {
        translation = mapping['en'];
    }
    return translation;
}

function EditTranslationsDialog(props: EditTranslationsDialogInterface): JSX.Element {
    const { t, i18n } = useTranslation('translation', { keyPrefix: 'options.dialog' })
    const languageNames = new Intl.DisplayNames([i18n.language], { type: "language" });

    var isCurrentLanguageTranslated = false;
    const fields = Object.entries(props.translations).map(([langCode, langTranslation]) => {
        if (langCode == i18n.language) {
            isCurrentLanguageTranslated = true;
        }
        const inputInfo = { title: langCode + ':', description: null }
        const languageFullName = languageNames.of(langCode);
        const questionData = {
            initialValue: langTranslation,
            label: languageFullName ? languageFullName : "En"
        }
        return (
            <Box>
                <LabeledQuestion
                    inputInfo={inputInfo}
                    questionType={SimpleQuestionType.SHORT_TEXT}
                    questionData={questionData}
                />
                <IconButton>
                    <Remove sx={{ color: "red" }} />
                </IconButton>
            </Box>
        )
    });
    const addButton = (
        <Box>
            <Button>{t('add').replace('{}', i18n.language)}</Button>
        </Box>
    );
    return (
        <Dialog open={props.open} onClose={props.closeDialog}>
            <DialogTitle>{t('title')}</DialogTitle>
            <DialogContent>
                {fields}
                {isCurrentLanguageTranslated ? null : addButton}
            </DialogContent>
            <DialogActions>
                <Button onClick={props.closeDialog}>{t('cancel')}</Button>
                <Button onClick={props.closeDialog}>{t('save')}</Button>
            </DialogActions>
        </Dialog>
    );
}

function OptionsList(props: OptionsListInterface) {
    const [translations, setTranslations] = useState<Translations | null>(null);
    const dialog = <EditTranslationsDialog
        open={translations ? true : false}
        translations={translations ? translations : {}}
        closeDialog={() => {setTranslations(null)}}
    />;
    const { i18n } = useTranslation();
    const listItems = props.options.map((option, index) => {
        return <ListItem disablePadding key={index}>
            <ListItemButton onClick={() => { setTranslations(option); }}>
                <ListItemIcon>
                    <Edit />
                </ListItemIcon>
                <ListItemText primary={getTranslation(option, i18n.language)} />
            </ListItemButton>
        </ListItem>
    });
    return (
        <Box>
            {dialog}
            <Accordion>
                <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                >
                    <p>{getTranslation(props.title, i18n.language)}</p>
                </AccordionSummary>
                <AccordionDetails>
                    <Box sx={{ marginBottom: "40px" }}>
                        <ListItemButton
                            sx={{ paddingBottom: 0, paddingTop: 0 }}
                            onClick={() => setTranslations(props.title)}
                        >
                            <Edit sx={{ marginRight: "20px" }} />
                            <Box component="p" display="inline" sx={{ fontSize: 28, verticalAlign: "middle" }}>
                                {getTranslation(props.title, i18n.language)}
                            </Box>
                        </ListItemButton>
                    </Box>
                    <Paper sx={{ marginLeft: "20%", marginRight: "20%" }}>
                        <List sx={{ maxHeight: "500px", overflow: "auto" }}>
                            {listItems}
                        </List>
                    </Paper>
                </AccordionDetails>
            </Accordion>
        </Box>
    )
}

export default OptionsList;