import "./Controls.css";
import React from "react";
import { faCircleLeft, faCircleUp } from "@fortawesome/free-regular-svg-icons";
import {
    faFileCirclePlus,
    faFolderPlus,
} from "@fortawesome/free-solid-svg-icons";
import { IconButton } from "../button/IconButton";
import { NameDialog } from "../dialog/Dialog";

export class Controls extends React.Component {
    constructor(props) {
        super(props);
        this.onSelectedNodeChange = this.onSelectedNodeChange.bind(this);
        this.handleClickNavigateBack = this.handleClickNavigateBack.bind(this);
        this.handleClickCreateFolder = this.handleClickCreateFolder.bind(this);
        this.handleCreateFolder = this.handleCreateFolder.bind(this);
        this.handleClickCreateVideo = this.handleClickCreateVideo.bind(this);
        this.handleCreateVideo = this.handleCreateVideo.bind(this);
        this.handleClickMoveNodeUp = this.handleClickMoveNodeUp.bind(this);
        this.handleCloseNewVideoDialog =
            this.handleCloseNewVideoDialog.bind(this);
        this.handleCloseNewFolderDialog =
            this.handleCloseNewFolderDialog.bind(this);
        this.state = {
            showNewVideoDialog: false,
            showNewFolderDialog: false,
        };
    }

    onSelectedNodeChange(e) {
        this.props.onSelectedNodeChange(e.target.value);
    }

    handleClickNavigateBack() {
        this.props.onContentsChange(null);
    }

    handleClickCreateFolder() {
        this.setState({ showNewFolderDialog: true });
    }

    handleCreateFolder(name) {
        this.props.onCreateFolder(name);
        this.handleCloseNewFolderDialog();
    }

    handleClickCreateVideo() {
        this.setState({ showNewVideoDialog: true });
    }

    handleCreateVideo(name) {
        this.props.onCreateVideo(name);
        this.handleCloseNewVideoDialog();
    }

    handleClickMoveNodeUp() {
        this.props.onMoveNodeUp();
    }

    handleCloseNewFolderDialog() {
        this.setState({ showNewFolderDialog: false });
    }

    handleCloseNewVideoDialog() {
        this.setState({ showNewVideoDialog: false });
    }

    render() {
        const selectedNode = this.props.selectedNode;
        const currentFolder = this.props.currentFolder;

        return (
            <div className="Controls">
                <IconButton
                    onClick={this.handleClickNavigateBack}
                    icon={faCircleLeft}
                    title={"Back one level"}
                    disabled={currentFolder === null}
                />
                <IconButton
                    onClick={this.handleClickCreateVideo}
                    icon={faFileCirclePlus}
                    title={"Create new video"}
                />
                <IconButton
                    onClick={this.handleClickCreateFolder}
                    icon={faFolderPlus}
                    title={"Create new folder"}
                />
                <IconButton
                    onClick={this.handleClickMoveNodeUp}
                    icon={faCircleUp}
                    title={"Move selected node one level up"}
                    disabled={selectedNode === null || currentFolder === null}
                />
                <NameDialog
                    nodeType="video"
                    showDialog={this.state.showNewVideoDialog}
                    onConfirmClick={this.handleCreateVideo}
                    onCancelClick={this.handleCloseNewVideoDialog}
                />
                <NameDialog
                    nodeType="folder"
                    showDialog={this.state.showNewFolderDialog}
                    onConfirmClick={this.handleCreateFolder}
                    onCancelClick={this.handleCloseNewFolderDialog}
                />
            </div>
        );
    }
}
