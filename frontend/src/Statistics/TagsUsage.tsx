import React, {useEffect} from "react";
import {getRequest} from "../Response/APIRequests";
import {useNavigate} from "react-router-dom";

export interface LinkInfo {
    link: string,
    name: string
}


export default function TagsUsage() {
    const [data, setData] = React.useState<LinkInfo[]>([])
    const navigate = useNavigate()

    useEffect(() => {
        getRequest("tags_usage", {}, navigate)
            .then((response) => {
                setData(response.data.data)
            })
    }, [])

    return <div>
        <h1>Forms not filled with tags: {data.length}</h1>
        {
            data.map(item => <div><a href={item.link}>{item.name}</a><br/></div>)
        }
    </div>
}