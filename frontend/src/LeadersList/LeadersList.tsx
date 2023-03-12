import {useState} from "react";
import axios from "axios";

enum State {
    Idle,
    Sent
}

function LeadersList() {
    const [text, setText] = useState("Loading...");
    const [state, setState] = useState(State.Idle)

    if (state == State.Idle) {
        axios.get("http://127.0.0.1:5000/forms?form_type=LEADER", {withCredentials: true}).then((res) => {
            setText(res.data.toString())
        })
        setState(State.Sent)
    }
    
    return <div>
        <h1>LeadersList component</h1>
        <h5>{text}</h5>
    </div>
}

export default LeadersList;