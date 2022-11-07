import React from 'react';

import './App.css';
import {GetFolder, ResolvePath} from './client';

import {Path} from './components/path/Path.js'
import {Controls} from './components/controls/Controls.js'
import {Contents} from './components/contents/Contents.js'


class App extends React.Component {
    constructor(props) {
        super(props);
        this.handleSelectedNodeChange = this.handleSelectedNodeChange.bind(this);
        this.handleContentsChange = this.handleContentsChange.bind(this);
        this.state = {
            path: window.location.pathname,
            selectedNode: null,
            currentFolder: null,
            parentFolder: null,
            contents: [],
        }
    }

    componentDidMount() {
        const result = ResolvePath();
        result.then(value => {
            this.setState({
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
                    currentFolder: value['name'],
                    parentFolder: value["parent_id"],
                    contents: value["contents"],
                })
            });
        } else {
            const result = ResolvePath();
            result.then(value => {
                this.setState({
                    currentFolder: value["name"],
                    parentFolder: value["parent_id"],
                    contents: value["contents"],
                })
            });
        }
    }

    render() {
        const contents = this.state.contents
        const currentFolder = this.state.currentFolder
        const selectedNode = this.state.selectedNode

        return (
            <div className="App">
                <Path
                    currentFolder={currentFolder} />
                <Controls
                    currentFolder={currentFolder}
                    selectedNode={selectedNode}
                    onContentsChange={this.handleContentsChange}
                    onSelectedNodeChange={this.handleSelectedNodeChange} />
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
