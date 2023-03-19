import { BlockInterface } from "./Block";
import {APIFormState} from "./APIObjects";


export interface ResponseDataInterface {
    id: number;
    title: string;
    blocks: Array<BlockInterface>;
    state: APIFormState
}
