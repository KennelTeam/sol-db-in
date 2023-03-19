import { BlockInterface } from "./Block";
import {APIFormState, APIFormType} from "./APIObjects";


export interface ResponseDataInterface {
    id: number;
    title: string;
    blocks: Array<BlockInterface>;
    state: APIFormState;

    form_type: APIFormType
}
