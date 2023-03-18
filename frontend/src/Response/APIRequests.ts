import axios, {AxiosResponse} from "axios";

const API_URL = "http://52.192.211.221:5000/"

export async function getRequest(endpoint: string, params: Object = {}): Promise<AxiosResponse<any, any>> {
    let query = API_URL + endpoint + "?"
    let key: keyof typeof params
    for (key in params) {
        query += key + "=" + params[key].toString() + "&"
    }
    return await axios.get(query, {
        withCredentials: true
    })
}

export async function postRequest(endpoint: string, params: Object): Promise<AxiosResponse<any, any>> {
    let query = API_URL + endpoint
    return await axios.post(query, params, {
        withCredentials: true
    })
}
