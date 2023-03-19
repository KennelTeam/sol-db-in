import axios from "axios";
import { SERVER_ADDRESS } from './types/global'

export interface TranslatedText {
    ru: string,
    en: string
}

export enum RESTMethod {
    GET,
    POST,
    PUT
}

export async function APIRequest(method: RESTMethod, endpoint: string, data: Object): Promise<Object | null> {
    let response = null;
    const url = SERVER_ADDRESS + endpoint
    switch (method) {
        case RESTMethod.GET:
            response = await axios.get(url, {
                params: data,
                withCredentials: true
            })
            break;
        case RESTMethod.POST:
            response = await axios.post(url, data, {withCredentials: true})
            break;
        case RESTMethod.PUT:
            response = await axios.put(url, data, {withCredentials: true})
    }
    if (response == null) return null;
    if (response.status == 200) return response.data;
    return null
}
