import "./Node.css";
import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
    faFile,
    faFileVideo,
    faFolder,
} from "@fortawesome/free-regular-svg-icons";

export class Node extends React.Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.handleDoubleClick = this.handleDoubleClick.bind(this);
    }

    handleClick() {
        this.props.onSelectedNodeChange(this.props.node);
    }

    handleDoubleClick() {
        const nodeType = this.props.node.type;
        if (nodeType === "folder") {
            this.props.onContentsChange(this.props.node.id);
        }
    }

    render() {
        const nodeId = this.props.node.id;
        const nodeName = this.props.node.name;
        const nodeType = this.props.node.type;
        const selected = this.props.selected;

        let icon = faFile;
        if (nodeType === "video") {
            icon = faFileVideo;
        } else if (nodeType === "folder") {
            icon = faFolder;
        }
        return (
            <div
                className={`Node ${selected ? "NodeSelected" : ""}`}
                key={nodeId}
                onClick={this.handleClick}
                onDoubleClick={this.handleDoubleClick}
            >
                <div className="NodeIcon">
                    <FontAwesomeIcon icon={icon} />
                </div>
                <div className="NodeName">{nodeName}</div>
            </div>
        );
    }
}
