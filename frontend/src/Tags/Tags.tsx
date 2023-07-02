import * as React from 'react'
import TreeView from '@mui/lab/TreeView';
import { alpha, styled } from '@mui/material/styles';
import TreeItem, {
  TreeItemProps,
  useTreeItem,
  TreeItemContentProps,
  treeItemClasses
} from '@mui/lab/TreeItem';
import clsx from 'clsx';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import { Box, Container, IconButton, Stack, TextField, Typography } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import AddIcon from '@mui/icons-material/Add';
import CheckIcon from '@mui/icons-material/Check';
import SubdirectoryArrowRightRoundedIcon from '@mui/icons-material/SubdirectoryArrowRightRounded';
import { getTags, changeTag, newTag } from "./requests2API"
import DeleteIcon from '@mui/icons-material/Delete';

export interface TagData {
    id: number,
    text: string,
    parent_id?: number,
    deleted?: boolean
}

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
    name: string
}

function Tags() {

    const [names, setNames] = React.useState<{ [id: number]: TagData }>([])

    React.useEffect(() => {
        getTags().then((tags) => {
            const newNames : { [id: number]: TagData } = {}
            tags.map((value) => {
                newNames[value.id] = value
            })
            console.log("Changed names!", newNames)
            setNames(newNames)
            console.log("Names:", Object.values(names))
        })
    }, [])

    function addTag(parentId?: number) {
        newTag(parentId).then((newId) => {
            const newNames = {...names}
            newNames[newId] = {
                id: newId,
                text: "",
                parent_id: parentId
            }
            setNames(newNames)
        })
    }

    const Tag = (tagProps: TagProps) => {
        const {tagId, name, ...other} = tagProps

        console.log("init")
        const [tagName, setName] = React.useState(name)
        const [edit, setEdit] = React.useState(tagName === "")

        const endEditing = () => {
            setEdit(!edit)
            if (edit) {
                const newNames = {...names}
                newNames[tagId].text = tagName
                setNames(newNames)
                changeTag({
                    id: tagId,
                    text: tagName
                })
            }
        }

        const deleteTag = () => {
            setEdit(false)
            const newNames = {...names}
            newNames[tagId].deleted = true
            setNames(newNames)
            changeTag({
                id: tagId,
                text: tagName,
                deleted: true
            })
        }

        const hasntChildren = !tagProps.children || Object.keys(tagProps.children).length === 0

        return <StyledTreeItem label={
            <Container sx={{ display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'space-between'}}>
                {edit ? 
                    <Container maxWidth={false} disableGutters>
                        <TextField value={tagName} variant='standard' fullWidth={true}
                            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                                setName(event.target.value)
                            }} onKeyDown={(e: React.KeyboardEvent<HTMLDivElement>) => {
                                if (e.key === 'Enter') {
                                    endEditing()
                                }
                            }}/>
                        <IconButton onClick={endEditing}>
                            <CheckIcon fontSize='small' htmlColor='green'/>
                        </IconButton>
                    </Container> :
                    <span onDoubleClick={endEditing}>
                        <Typography variant='body1' sx={{flexGrow: 1}}>{tagName}</Typography>
                    </span>}
                <Stack direction='row' justifyContent='flex-end'>
                    <IconButton onClick={endEditing}>
                        <EditIcon fontSize='small'/>
                    </IconButton>
                    { hasntChildren ?
                        <IconButton onClick={() => {
                            addTag(tagId)
                        }}>
                            <SubdirectoryArrowRightRoundedIcon
                                htmlColor='green' fontSize='small'/>
                        </IconButton> : null }
                    { hasntChildren ?
                        <IconButton onClick={deleteTag}>
                            <DeleteIcon htmlColor='red'/>
                        </IconButton> : null }
                </Stack>
            </Container>
        } {...other}/>
    }

    function makeTags(root: TagData) : JSX.Element{
        const childrenData = Object.values(names).filter(
            (value) => (value.parent_id && value.parent_id === root.id && !value.deleted))
        const children = childrenData.map((value) => makeTags(value))
        if (children.length > 0) {
            children.push(
                <IconButton onClick={() => {
                    addTag(root.id)
                }}>
                    <AddIcon htmlColor='green'/>
                </IconButton>
            )
        }
        return <Tag
                    tagId={root.id}
                    name={names[root.id].text}
                    nodeId={root.id.toString()}
                    children={children}/>
    }

    const categories = Object.values(names).filter((value) => (!value.parent_id && !value.deleted))
            .map((value) => makeTags(value))

    return <TreeView
        aria-label="file system navigator"
        defaultCollapseIcon={<ExpandMoreIcon />}
        defaultExpandIcon={<ChevronRightIcon />}
        sx={{ minHeight: 1500, flexGrow: 1, overflowY: 'auto' }}
    >
        {categories}
        <IconButton onClick={() => {
            addTag()
        }}>
            <AddIcon htmlColor='green'/>
        </IconButton>
    </TreeView>
}

export default Tags;