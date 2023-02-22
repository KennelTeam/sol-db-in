import { Box, Button, MenuItem, Select, TextField } from "@mui/material";
import { i18n as I18nType } from "i18next";
import { useState } from "react";
import { useTranslation } from "react-i18next";
import { SupportedLanguages, SUPPORTED_LANGUAGES } from "../i18n";
import "./Settings.css";

interface SettingsData {
    leadersPerPage: number;
    projectsPerPage: number;
    commentMaxLength: number;
    language: SupportedLanguages;
}

function applySettings(i18n: I18nType, settings: SettingsData) {
    i18n.changeLanguage(settings.language);
}

function Settings() {
    const { t, i18n } = useTranslation('translation', { keyPrefix: 'settings' });
    const [langCode, setLangCode] = useState(i18n.language);
    return (
        <Box display="flex" flexDirection="column" alignItems="center">
            <h2>{t('title')}</h2>
            <Box component="form" alignItems="center">
                <Box display="flex" flexDirection="row" justifyContent="space-between" className="form-label">
                    <p className="label-wrapper">{t('leaders-per-page')}</p>
                    <TextField type="number" />
                </Box>
                <Box display="flex" flexDirection="row" justifyContent="space-between" className="form-label">
                    <p className="label-wrapper">{t('projects-per-page')}</p>
                    <TextField type="number" />
                </Box>
                <Box display="flex" flexDirection="row" justifyContent="space-between" className="form-label">
                    <p className="label-wrapper">{t('leader-comment-max-length')}</p>
                    <TextField type="number" />
                </Box>
                <Box display="flex" flexDirection="row" justifyContent="space-between" className="form-label">
                    <p className="label-wrapper">{t('change-language')}</p>
                    <Select sx={{width: "300px"}} value={langCode} onChange={(e) => setLangCode(e.target.value)}>
                        {SUPPORTED_LANGUAGES.map((langCode) => <MenuItem value={langCode}>{new Intl.DisplayNames([langCode], { type: "language" }).of(langCode)}</MenuItem>)}
                    </Select>
                </Box>
                <Button
                    variant="contained"
                    onClick={() => applySettings(i18n, {
                        language: langCode as SupportedLanguages,
                        leadersPerPage: 10,
                        projectsPerPage: 20,
                        commentMaxLength: 130,
                    })}
                >
                    {t('save')}
                </Button>
            </Box>
        </Box>
    );
}

export default Settings;