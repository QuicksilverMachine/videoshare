import './Controls.css';
import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faFile, faFolder} from "@fortawesome/free-regular-svg-icons";


export class Controls extends React.Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(e) {
        this.props.onSelectedNodeChange(e.target.value)
    }

    render() {
        const selectedNode = this.props.selectedNode;

        return (
            <div className="Controls">
                <button><FontAwesomeIcon icon={faFile} /></button>
                <button><FontAwesomeIcon icon={faFolder} /></button>
            </div>
        )
    }
}
