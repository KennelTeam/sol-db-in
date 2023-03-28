import Response from "../Response/Response";
import TEST_DATA from "./TEST_DATA";
import { GetFormInfo} from "../Response/API2Front";
import {useEffect, useState} from "react";
import {ResponseDataInterface} from "../Response/ResponseData";
import {Navigate, useParams, useNavigate} from "react-router-dom";
import {useEffectOnce} from "./useEffectOnce";

function Leader(): JSX.Element {
    const [loaded, setLoaded] = useState(false);
    const [data, setData] = useState(TEST_DATA);
    const params = useParams();

    const navigate = useNavigate()

    console.log("rendering")
    useEffectOnce( () => {
        let id = params.id
        if (id !== undefined) {
            GetFormInfo(+id as number, navigate).then((responseData) => {
                setLoaded(true);
                console.log(responseData)
                setData(responseData);
            })
        }

    });
    if (!loaded) {
        return <div>Loading...</div>
    }
    return <Response {...data as ResponseDataInterface}/>
}

export default Leader;