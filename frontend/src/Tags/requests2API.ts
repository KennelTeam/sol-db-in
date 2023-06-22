import axios from "axios";
import { TagData } from "./Tags"
import { handleError } from "../FiltersTablePage/requests2API";
import { SERVER_ADDRESS } from "../types/global";

interface ResponseTagData {
    id: number,
    text: string
    parent_id?: number
}

export async function getTags() : Promise<TagData[]> {
    return await axios.get(SERVER_ADDRESS + "/all_tags",
    { withCredentials: true })
    .then((response) => {
        console.log("/all_tags response:", response.data)
        return (response.data.data as ResponseTagData[]).map((data: ResponseTagData) => {
            return {
                id: data.id,
                text: data.text,
                parent_id: data.parent_id
            } as TagData
        })
    })
    .catch((error) => {
        console.log("Error while requesting /all_tags:", error)
        return []
    })
}

export async function changeTag(tag: TagData) {
    axios.post(SERVER_ADDRESS + "/tags", {
        id: tag.id,
        name: {
            en: tag.text
        },
        parent_id: tag.parent_id,
        type_id: 0
    },
    { withCredentials: true })
    .then((response) => {
        console.log("Changed tag successfully")
    })
    .catch((error) => {
        console.log("Changing tag failed")
    })
}

export async function newTag(parent_id?: number) : Promise<number> {
    return axios.post(SERVER_ADDRESS + "/tags", {
        name: {
            en: "NEW TAG"
        },
        parent_id: parent_id,
        type_id: 0
    },
    { withCredentials: true })
    .then((response) => {
        console.log("Added tag successfully:", response.data)
        return response.data as number
    })
    .catch((error) => {
        console.log("Changing tag failed")
        return -1
    })
}