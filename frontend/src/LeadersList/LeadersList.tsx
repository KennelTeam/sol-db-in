import {useEffect, useState} from "react";
import axios, {AxiosResponse} from "axios";

enum State {
    Idle,
    Sent,
    Received
}

function LeadersList() {
    const [text, setText] = useState("Loading...");
    const [state, setState] = useState(State.Idle)

    function processResponse(res: AxiosResponse) {
        setText(JSON.stringify(res.data))
    }

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/forms?form_type=LEADER", {withCredentials: true}).then(processResponse)
    }, [])
    
    return <div>
        <h1>LeadersList component</h1>
        <h5>{text}</h5>
    </div>
}

export default LeadersList;