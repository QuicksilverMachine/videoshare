import './Path.css';
import React from "react";
import {faCopy} from "@fortawesome/free-regular-svg-icons";
import {Button} from '../button/Button'

export class Path extends React.Component {
    render () {
        const currentFolder = this.props.currentFolder;

        return (
            <div className="Path">
                <h1>
                    {currentFolder ? currentFolder: "Root"}
                    &nbsp;
                    <Button icon={faCopy} help={'Copy current path'}/>
                </h1>
            </div>
        )
    }
}
