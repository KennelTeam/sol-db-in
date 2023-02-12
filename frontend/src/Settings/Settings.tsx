import { Box, Button, TextField } from "@mui/material";
import { useTranslation } from "react-i18next";
import "./Settings.css";

function Settings() {
    const { t } = useTranslation('translation',  {keyPrefix: 'settings'});
    return (
        <Box display="flex" flexDirection="column" alignItems="center">
            <h2>{t('title')}</h2>
            <Box component="form" alignItems="center">
                <Box display="flex" flexDirection="row" justifyContent="space-between" className="form-label">
                    <p className="label-wrapper">{t('leaders-per-page')}</p>
                    <TextField type="number"/>
                </Box>
                <Box display="flex" flexDirection="row" justifyContent="space-between" className="form-label">
                    <p className="label-wrapper">{t('projects-per-page')}</p>
                    <TextField type="number"/>
                </Box>
                <Box display="flex" flexDirection="row" justifyContent="space-between" className="form-label">
                    <p className="label-wrapper">{t('leader-comment-max-length')}</p>
                    <TextField type="number"/>
                </Box>
                <Button variant="contained">{t('save')}</Button>
            </Box>
        </Box>  
    );
}

export default Settings;