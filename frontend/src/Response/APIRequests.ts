import axios, {AxiosResponse} from "axios";
import { SERVER_ADDRESS } from '../types/global'


export async function getRequest(endpoint: string, params: Object = {}): Promise<AxiosResponse<any, any>> {
    let query = SERVER_ADDRESS + endpoint + "?"
    let key: keyof typeof params
    for (key in params) {
        query += key + "=" + params[key].toString() + "&"
    }
    return await axios.get(query, {
        withCredentials: true
    })
}

export async function postRequest(endpoint: string, params: Object): Promise<AxiosResponse<any, any>> {
    let query = SERVER_ADDRESS + endpoint
    return await axios.post(query, params, {
        withCredentials: true
    })
}
