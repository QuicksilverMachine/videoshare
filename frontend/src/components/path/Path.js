import './Path.css';
import React from "react";
import {faCopy} from "@fortawesome/free-regular-svg-icons";
import {Button} from '../button/Button'

export class Path extends React.Component {
    constructor(props) {
        super(props);
        this.handleCopyURLClick = this.handleCopyURLClick.bind(this);
    }

    handleCopyURLClick() {
        this.props.onCopyURLToClipboard()
    }

    render() {
        const path = this.props.path;
        const currentFolder = this.props.currentFolder;

        return (
            <div className="Path">
                <h1>
                    {currentFolder ? currentFolder: "Root"}
                    &nbsp;
                    <Button onClick={this.handleCopyURLClick} icon={faCopy} help={'Copy current path'}/>
                </h1>
                <div className="PathFull">{path}</div>
            </div>
        )
    }
}
