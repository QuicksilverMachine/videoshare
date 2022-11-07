import React from 'react';

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
        this.handleCopyURLToClipboard = this.handleCopyURLToClipboard.bind(this);
        this.state = {
            path: "",
            selectedNode: null,
            currentFolderId: null,
            currentFolder: null,
            parentFolder: null,
            contents: [],
        }
    }

    componentDidMount() {
        const result = ResolvePath(window.location.pathname);
        result.then(value => {
            this.setState({
                path: value["path"],
                currentFolderId: value["id"],
                currentFolder: value["name"],
                parentFolder: value["parent_id"],
                contents: value["contents"],
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
            response.then(value => {
                this.setState({
                    path: value["path"],
                    currentFolderId: value["id"],
                    currentFolder: value['name'],
                    parentFolder: value["parent_id"],
                    contents: value["contents"],
                })
            });
        } else {
            const result = ResolvePath();
            result.then(value => {
                this.setState({
                    path: value["path"],
                    currentFolderId: value["id"],
                    currentFolder: value["name"],
                    parentFolder: value["parent_id"],
                    contents: value["contents"],
                })
            });
        }
    }

    handleCreateFolder(name) {
        const parentId = this.state.currentFolderId;
        const result = CreateFolder(name, parentId);
        result.then(_ => {
            this.handleContentsChange(parentId)
        });
    }

    handleCreateVideo(name) {
        const parentId = this.state.currentFolderId;
        const result = CreateVideo(name, parentId);
        result.then(_ => {
            this.handleContentsChange(parentId)
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
        result.then(value => {
            if (!value.code || value.code < 400) {
                this.handleContentsChange(parentFolder)
            }
        });
    }

    handleCopyURLToClipboard() {
        const path = this.state.path ? this.state.path : ""
        const url = `${window.location.origin}/${path}`
        navigator.clipboard.writeText(url).then();
    }

    render() {
        const path = this.state.path
        const contents = this.state.contents
        const currentFolder = this.state.currentFolder
        const selectedNode = this.state.selectedNode

        return (
            <div className="App">
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
                    onSelectedNodeChange={this.handleSelectedNodeChange} />
            </div>
        );
    }
}

export default App;
