import './Path.css';
import React from "react";


export class Path extends React.Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(e) {
        this.props.onCurrentFolderChange(e.target.value);
    }

    render () {
        const currentFolder = this.props.currentFolder;

        return (
            <div className="Path">
                <h1>{currentFolder ? currentFolder: "Root"}</h1>
            </div>
        )
    }
}
