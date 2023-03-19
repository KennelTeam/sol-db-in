import FilterTablePage from "../FiltersTablePage";
import {useEffect, useState} from "react";
import axios, {AxiosResponse} from "axios";

enum State {
    Idle,
    Sent,
    Received
}

function LeadersList() {
    return <FilterTablePage formType='LEADER'/>
}

export default LeadersList;