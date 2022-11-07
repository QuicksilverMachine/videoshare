import './Controls.css';
import React from "react";
import {faCircleLeft, faCircleUp} from "@fortawesome/free-regular-svg-icons";
import {faFileCirclePlus, faFolderPlus} from "@fortawesome/free-solid-svg-icons";
import {Button} from '../button/Button'

export class Controls extends React.Component {
    constructor(props) {
        super(props);
        this.onSelectedNodeChange = this.onSelectedNodeChange.bind(this);
        this.handleClickNavigateBack = this.handleClickNavigateBack.bind(this);
        this.handleClickCreateFolder = this.handleClickCreateFolder.bind(this);
        this.handleClickCreateVideo = this.handleClickCreateVideo.bind(this);
        this.handleClickMoveNodeUp = this.handleClickMoveNodeUp.bind(this);
    }

    onSelectedNodeChange(e) {
        this.props.onSelectedNodeChange(e.target.value)
    }

    handleClickNavigateBack() {
        this.props.onContentsChange(null)
    }

    handleClickCreateFolder() {
        const name = "My Name"
        this.props.onCreateFolder(name);
    }

    handleClickCreateVideo() {
        const name = "My Name"
        this.props.onCreateVideo(name);
    }

    handleClickMoveNodeUp() {
        this.props.onMoveNodeUp();
    }

    render() {
        const selectedNode = this.props.selectedNode;
        const currentFolder = this.props.currentFolder;

        return (
            <div className="Controls">
                <Button onClick={this.handleClickNavigateBack} icon={faCircleLeft} help={'Back one level'} disabled={currentFolder === null}/>
                <Button onClick={this.handleClickCreateVideo} icon={faFileCirclePlus} help={'Create new video'} />
                <Button onClick={this.handleClickCreateFolder} icon={faFolderPlus} help={'Create new folder'} />
                <Button onClick={this.handleClickMoveNodeUp} icon={faCircleUp} help={'Move selected node one level up'} disabled={selectedNode === null || currentFolder === null}/>
            </div>
        )
    }
}
