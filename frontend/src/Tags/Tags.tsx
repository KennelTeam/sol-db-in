import * as React from 'react';
import TreeView from '@mui/lab/TreeView';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import TreeItem, { TreeItemProps, treeItemClasses } from '@mui/lab/TreeItem';
import { Box, Container, IconButton, Stack, TextField, Typography } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import AddIcon from '@mui/icons-material/Add';
import CheckIcon from '@mui/icons-material/Check';
import SubdirectoryArrowRightRoundedIcon from '@mui/icons-material/SubdirectoryArrowRightRounded';
import { getTags, changeTag, newTag } from "./requests2API"

export interface TagData {
    id: number,
    text: string,
    parent_id?: number
}

const data : TagData[] = [
    {
        id: 1,
        text: "Category 1"
    },
    {
        id: 2,
        text: "Subcategory 1.1",
        parent_id: 1
    },
    {
        id: 3,
        text: "Subcategory 1.2",
        parent_id: 1
    },
    {
        id: 4,
        text: "Tag 1.1.1",
        parent_id: 2
    },
    {
        id: 5,
        text: "Tag 1.1.2",
        parent_id: 2
    },
    {
        id: 6,
        text: "Tag 1.2.1",
        parent_id: 3
    },
    {
        id: 7,
        text: "Subcategory 1.2.1 lalala",
        parent_id: 2
    },
    {
        id: 8,
        text: "Tag 1.2.1.1",
        parent_id: 7
    }
]

type TagProps = TreeItemProps & {
    tagId: number,
    name: string
  }

function Tags() {

    const startNames : { [id: number]: TagData } = {}
    data.map((value) => {
        startNames[value.id] = value
    })
    const [names, setNames] = React.useState<{ [id: number]: TagData }>(startNames)

    // getTags().then((tags) => {
    //     const newNames : { [id: number]: TagData } = {}
    //     data.map((value) => {
    //         newNames[value.id] = value
    //     })
    //     console.log("Changed names!")
    //     setNames(newNames)
    // })
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

    // {
    //     '1': 'Category 1',
    //     '2': 'Subcategory 1',
    //     '4': 'Tag 1',
    //     '5': 'Tag 2',
    //     '3': 'Subcategory 2',
    //     '6': 'Tag 4',
    //     '7': 'Subsubcategory 3',
    //     '8': 'Tag 8'
    // })

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

        return <TreeItem label={
            <Container sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
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
                <Box>
                    <IconButton onClick={endEditing}>
                        <EditIcon fontSize='small'/>
                    </IconButton>
                    { !tagProps.children || Object.keys(tagProps.children).length === 0 ?
                        <IconButton onClick={() => {
                            addTag(tagId)
                        }}>
                            <SubdirectoryArrowRightRoundedIcon
                                htmlColor='green' fontSize='small'/>
                        </IconButton> : null }
                </Box>
            </Container>
        } {...other}/>
    }

    function makeTags(root: TagData) : JSX.Element{
        const childrenData = Object.values(names).filter(
            (value) => (value.parent_id && value.parent_id === root.id))
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

    const categories = Object.values(names).filter((value) => (!value.parent_id))
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