import { HelpOutline } from "@mui/icons-material";
import { Box, IconButton, Tooltip } from "@mui/material";

export interface InputInfoInterface {
    title: string | null;
    description: string | null;
}

function InputInfo(inputInfo: InputInfoInterface) {
  const tooltip = (
    <Tooltip title={inputInfo.description}>
      <IconButton>
        <HelpOutline />
      </IconButton>
    </Tooltip>
  );
  const title = <p style={{ display: "inline-block" }}>{inputInfo.title}</p>
  return (
    <Box display="inline-block" sx={{
      verticalAlign: "middle",
      paddingRight: "5px",
      margin: 0,
      whiteSpace: "nowrap"
    }}>
      {inputInfo.title? title : null}
      {inputInfo.description? tooltip : null}
    </Box>
  );
}

export default InputInfo;