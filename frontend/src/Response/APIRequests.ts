import axios, {AxiosResponse} from "axios";
import { SERVER_ADDRESS } from '../types/global'
import { handleError } from "../FiltersTablePage/requests2API"
import { NavigateFunction } from "react-router-dom";


export async function getRequest(endpoint: string, params: Object = {}, navigate: NavigateFunction): Promise<AxiosResponse<any, any>> {
    let query = SERVER_ADDRESS + "/" + endpoint + "?"
    let key: keyof typeof params
    // for (key in params) {
    //     query += key + "=" + params[key].toString() + "&"
    // }
    return await axios.get(query, {
        withCredentials: true,
        params: params
    })
        .catch((error) => {
            console.log(error)
            handleError(navigate, error)
            return error
        })
}

export async function postRequest(endpoint: string, params: Object, navigate: NavigateFunction): Promise<AxiosResponse<any, any>> {
    let query = SERVER_ADDRESS + "/" + endpoint
    return await axios.post(query, params, {
        withCredentials: true
    })
        .catch((error) => {
            console.log(error)
            handleError(navigate, error)
            return error
        })
}
