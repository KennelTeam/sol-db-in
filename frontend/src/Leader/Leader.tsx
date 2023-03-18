import Response from "../Response/Response";
import TEST_DATA from "./TEST_DATA";
import {GetFormInfo} from '../Response/API2Front'
import {useState} from "react";
import {ResponseDataInterface} from "../Response/ResponseData";
import {Navigate, useParams} from "react-router-dom";

function Leader(): JSX.Element {
    const [loaded, setLoaded] = useState(false);
    const [data, setData] = useState(TEST_DATA);
    const params = useParams();

    if (!loaded) {
        let id = params.id
        if (id === undefined) {
            return <Navigate to="/login"/>
        }
        GetFormInfo(+id as number).then((responseData) => {
            setLoaded(true);
            setData(responseData);
        })
        return <div>Loading... Please wait...</div>
    } else {
        return <Response {...data as ResponseDataInterface}/>
    }
}

export default Leader;