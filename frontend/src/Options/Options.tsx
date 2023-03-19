import { Box } from "@mui/material";
import { useTranslation } from "react-i18next";
import OptionsList, { OptionsListInterface } from "./OptionsList";
import TEST_DATA from "./TEST_DATA";

export interface OptionsInterface {
  data: Array<OptionsListInterface>;
}

export default function Options(): JSX.Element {
  const props = TEST_DATA;
  const { t } = useTranslation('translation', { keyPrefix: 'options' })
  const components = props.data.map((listData) => {return <OptionsList {...listData}/>})
  return (
    <Box>
      <h1>{t('title')}</h1>
      {components}
    </Box>
  );
}