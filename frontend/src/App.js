import React from 'react';

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import './App.css';
import {CreateFolder, CreateVideo, GetFolder, MoveFolder, MoveVideo, ResolvePath} from './client';

import {Path} from './components/path/Path.js'
import {Controls} from './components/controls/Controls.js'
import {Contents} from './components/contents/Contents.js'


class App extends React.Component {
    constructor(props) {
        super(props);
        this.handleSelectedNodeChange = this.handleSelectedNodeChange.bind(this);
        this.handleContentsChange = this.handleContentsChange.bind(this);
        this.handleCreateFolder = this.handleCreateFolder.bind(this);
        this.handleCreateVideo = this.handleCreateVideo.bind(this);
        this.handleMoveNodeUp = this.handleMoveNodeUp.bind(this);
        this.handleMoveNode = this.handleMoveNode.bind(this);
        this.handleCopyURLToClipboard = this.handleCopyURLToClipboard.bind(this);
        this.showToastMessage = this.showToastMessage.bind(this);
        this.state = {
            path: "",
            selectedNode: null,
            currentFolderId: null,
            currentFolder: null,
            parentFolder: null,
            contents: [],
        }
    }

    showToastMessage(func, message) {
        func(
            message,
            {
                position: toast.POSITION.TOP_RIGHT,
                autoClose: 3000,
            }
        );
    };

    componentDidMount() {
        const result = ResolvePath(window.location.pathname);
        result.then(response => {
            if (response.code && response.code >= 400) {
                this.showToastMessage(toast.error, response.description)
                return
            }
            this.setState({
                path: response["path"],
                currentFolderId: response["id"],
                currentFolder: response["name"],
                parentFolder: response["parent_id"],
                contents: response["contents"],
            })
        });
    }

    handleSelectedNodeChange(selectedNode) {
        this.setState({selectedNode: selectedNode});
    }

    handleContentsChange(folder_id) {
        const new_folder = folder_id ? folder_id : this.state.parentFolder

        if (new_folder != null) {
            const response = GetFolder(new_folder)
            response.then(response => {
                if (response.code && response.code >= 400) {
                    this.showToastMessage(toast.error, response.description)
                    return
                }
                this.setState({
                    path: response["path"],
                    currentFolderId: response["id"],
                    currentFolder: response['name'],
                    parentFolder: response["parent_id"],
                    contents: response["contents"],
                });
                window.history.pushState({}, null, `/${response["path"] ? response["path"] : ""}`);
            });
        } else {
            const result = ResolvePath();
            result.then(response => {
                if (response.code && response.code >= 400) {
                    this.showToastMessage(toast.error, response.description)
                    return
                }
                this.setState({
                    path: response["path"],
                    currentFolderId: response["id"],
                    currentFolder: response["name"],
                    parentFolder: response["parent_id"],
                    contents: response["contents"],
                })
                window.history.pushState({}, null, `/${response["path"] ? response["path"] : ""}`);
            });
        }
        // Reset selected after traversal
        this.setState({selectedNode: null})
    }

    handleCreateFolder(name) {
        const parentId = this.state.currentFolderId;
        const result = CreateFolder(name, parentId);
        result.then(response => {
            if (response.code && response.code >= 400) {
                this.showToastMessage(toast.error, response.description)
                return
            }
            this.handleContentsChange(parentId)
            this.showToastMessage(toast.success, `Folder ${name} created`)
        });
    }

    handleCreateVideo(name) {
        const parentId = this.state.currentFolderId;
        const result = CreateVideo(name, parentId);
        result.then(response => {
            if (response.code && response.code >= 400) {
                this.showToastMessage(toast.error, response.description)
                return
            }
            this.handleContentsChange(parentId)
            this.showToastMessage(toast.success, `Video ${name} created`)
        });
    }

    handleMoveNodeUp() {
        const parentFolder = this.state.parentFolder;
        const selectedNode = this.state.selectedNode;

        let moveFunction;
        if (selectedNode.type === "video") {
            moveFunction = MoveVideo
        } else if (selectedNode.type === "folder") {
            moveFunction = MoveFolder
        } else {
            return
        }
        const result = moveFunction(selectedNode.id, parentFolder);
        result.then(response => {
            if (response.code && response.code >= 400) {
                this.showToastMessage(toast.error, response.description)
                return
            }
            this.handleContentsChange(parentFolder)
            this.showToastMessage(toast.success, `Moved ${selectedNode.name} up`)
        });
    }

    handleMoveNode(node, parent) {
        let moveFunction;
        if (node.type === "video") {
            moveFunction = MoveVideo
        } else if (node.type === "folder") {
            moveFunction = MoveFolder
        } else {
            return
        }
        const result = moveFunction(node.id, parent.id);
        result.then(response => {
            if (response.code && response.code >= 400) {
                this.showToastMessage(toast.error, response.description)
                return
            }
            this.handleContentsChange(this.state.currentFolderId)
            this.showToastMessage(toast.success, `Moved ${node.name} to ${parent.name}`)
        });
    }

    handleCopyURLToClipboard() {
        const path = this.state.path ? this.state.path : ""
        const url = `${window.location.origin}/${path}`
        navigator.clipboard.writeText(url).then(_ => {
            this.showToastMessage(toast.success, `Copied path to clipboard`)
        });
    }

    render() {
        const path = this.state.path
        const contents = this.state.contents
        const currentFolder = this.state.currentFolder
        const selectedNode = this.state.selectedNode

        return (
            <div className="App">
                <ToastContainer />
                <Path
                    path={path}
                    onCopyURLToClipboard={this.handleCopyURLToClipboard}
                    currentFolder={currentFolder} />
                <Controls
                    currentFolder={currentFolder}
                    selectedNode={selectedNode}
                    onContentsChange={this.handleContentsChange}
                    onSelectedNodeChange={this.handleSelectedNodeChange}
                    onCreateFolder={this.handleCreateFolder}
                    onCreateVideo={this.handleCreateVideo}
                    onMoveNodeUp={this.handleMoveNodeUp}
                />
                <Contents
                    contents={contents}
                    selectedNode={selectedNode}
                    onContentsChange={this.handleContentsChange}
                    onSelectedNodeChange={this.handleSelectedNodeChange}
                    onMoveNode={this.handleMoveNode}
                />
            </div>
        );
    }
}

export default App;
