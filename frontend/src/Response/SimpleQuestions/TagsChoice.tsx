import React from 'react'
import TreeView from '@mui/lab/TreeView';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import { alpha, styled } from '@mui/material/styles';
import TreeItem, {
  TreeItemProps,
  useTreeItem,
  TreeItemContentProps,
  treeItemClasses
} from '@mui/lab/TreeItem';
import clsx from 'clsx';
import Typography from '@mui/material/Typography';
import { DialogTitle, Paper } from '@material-ui/core';
import { Box, Button, Checkbox, DialogActions, DialogContent, IconButton, Stack } from '@mui/material';
import { useTranslation } from 'react-i18next';
import axios from 'axios';
import { SERVER_ADDRESS } from '../../types/global';
import { APITag } from '../APIObjects';

const CustomContent = React.forwardRef(function CustomContent(
  props: TreeItemContentProps,
  ref,
) {
  const {
    classes,
    className,
    label,
    nodeId,
    icon: iconProp,
    expansionIcon,
    displayIcon,
  } = props;

  const {
    disabled,
    expanded,
    selected,
    focused,
    handleExpansion,
    handleSelection,
    preventSelection,
  } = useTreeItem(nodeId);

  const icon = iconProp || expansionIcon || displayIcon;

  const handleMouseDown = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
    preventSelection(event);
  };

  const handleExpansionClick = (
    event: React.MouseEvent<HTMLDivElement, MouseEvent>,
  ) => {
    handleExpansion(event);
  };

  const handleSelectionClick = (
    event: React.MouseEvent<HTMLDivElement, MouseEvent>,
  ) => {
    handleSelection(event);
  };

  return (
    // eslint-disable-next-line jsx-a11y/no-static-element-interactions
    <div
      className={clsx(className, classes.root, {
        [classes.expanded]: expanded,
        [classes.selected]: selected,
        [classes.focused]: focused,
        [classes.disabled]: disabled,
      })}
      onMouseDown={handleMouseDown}
      ref={ref as React.Ref<HTMLDivElement>}
    >
      {/* eslint-disable-next-line jsx-a11y/click-events-have-key-events,jsx-a11y/no-static-element-interactions */}
      <div onClick={handleExpansionClick} className={classes.iconContainer}>
        {icon}
      </div>
      <Typography
        onClick={handleSelectionClick}
        component="div"
        className={classes.label}
      >
        {label}
      </Typography>
    </div>
  );
});

function CustomTreeItem(props: TreeItemProps) {
    return <TreeItem ContentComponent={CustomContent} {...props} />;
}

const StyledTreeItem = styled((props: TreeItemProps) => (
    <CustomTreeItem {...props} />
  ))(({ theme }) => ({
    [`& .${treeItemClasses.iconContainer}`]: {
      '& .close': {
        opacity: 0.3,
      },
    },
    [`& .${treeItemClasses.group}`]: {
      marginLeft: 15,
      paddingLeft: 18,
      borderLeft: `1px dashed ${alpha(theme.palette.text.primary, 0.4)}`,
    },
}));

type TagProps = TreeItemProps & {
    tagId: number,
    name: string,
    chosen: boolean
}

export interface TagData {
    id: number,
    text: string,
    parent_id?: number,
    type_id: number
    chosen: boolean
}

interface ResponseTagData {
    id: number,
    text: string
    parent_id?: number,
    type_id: number,
    deleted?: boolean
}

async function getTags() : Promise<TagData[]> {
    return await axios.get(SERVER_ADDRESS + "/all_tags",
    { withCredentials: true })
    .then((response) => {
        console.log("/all_tags response:", response.data)
        return (response.data.data as ResponseTagData[])
            .filter((data: ResponseTagData) => (!data.deleted))
            .map((data: ResponseTagData) => {
                return {
                    id: data.id,
                    text: data.text,
                    parent_id: data.parent_id,
                    type_id: data.type_id
                } as TagData
            })
    })
    .catch((error) => {
        console.log("Error while requesting /all_tags:", error)
        return []
    })
}

export interface TagsChoiceProps {
    chosenTags: number[],
    onCancel: () => void,
    onSubmit: (newTags: APITag[]) => void
}

export default function TagsChoice(props: TagsChoiceProps) {

    const [tagsData, setTagsData] = React.useState<{ [id: number]: TagData }>([])

    const {t} = useTranslation("translation", { keyPrefix: "response"})

    React.useEffect(() => {
        getTags().then((tags) => {
            const newTagsData : { [id: number]: TagData } = {}
            tags.map((value) => {
                newTagsData[value.id] = {
                    ...value,
                    chosen: false
            }})
            console.log(props.chosenTags)
            console.log(newTagsData)
            props.chosenTags.map((tagId) => {
                if (newTagsData[tagId]) {
                    newTagsData[tagId].chosen = true
                }
            })
            setTagsData(newTagsData)
        })
    }, [])

    const Tag = (props: TagProps) => {
        const { tagId, name, chosen, ...other } = props
        
        return <StyledTreeItem label={
            <Stack direction='row' justifyContent='flex-start' alignItems='center'>
                <Checkbox checked={chosen} onChange={() => {
                    const newTagsData = {...tagsData}
                    newTagsData[tagId].chosen = !tagsData[tagId].chosen
                    setTagsData(newTagsData)
                }}/>
                <Typography variant='body1'>{name}</Typography>
            </Stack>
        } {...other}/>
    }

    function makeTags(root: TagData) : JSX.Element{
        const childrenData = Object.values(tagsData).filter(
            (value) => (value.parent_id && value.parent_id === root.id))
        const children = childrenData.map((value) => makeTags(value))
        return <Tag
                    tagId={root.id}
                    name={tagsData[root.id].text}
                    nodeId={root.id.toString()}
                    chosen={tagsData[root.id].chosen}
                    children={children}/>
    }

    const categories = Object.values(tagsData).filter((value) => (!value.parent_id))
            .map((value) => makeTags(value))

    return (
    <div>
        <DialogTitle>{t('tags-dialog-title')}</DialogTitle>
    <DialogContent>
        <TreeView
            aria-label="file system navigator"
            defaultCollapseIcon={<ExpandMoreIcon />}
            defaultExpandIcon={<ChevronRightIcon />}
            sx={{ minHeight: 300, minWidth: 400, flexGrow: 1, overflowY: 'auto' }}
        >
            {categories}
        </TreeView>
    </DialogContent>
    <DialogActions>
        <Button onClick={props.onCancel}>{t("cancel")}</Button>
        <Button color='secondary' onClick={() => {
            props.onSubmit(Object.values(tagsData).filter((tag) => (tag.chosen))
                .map((tag) => ({
                    id: tag.id,
                    name: {
                        en: tag.text,
                        ru: tag.text
                    },
                    parent_id: tag.parent_id,
                    type_id: tag.type_id,
                    deleted: false
                } as APITag)))
        }}>{t("submit")}</Button>
    </DialogActions>
    </div>
    )
}
