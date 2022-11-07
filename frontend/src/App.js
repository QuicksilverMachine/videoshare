import React from 'react';

import './App.css';
import {ResolvePath} from './client';

import {Path} from './components/path/Path.js'
import {Controls} from './components/controls/Controls.js'
import {Contents} from './components/contents/Contents.js'


class App extends React.Component {
    constructor(props) {
        super(props);
        this.handleSelectedNodeChange = this.handleSelectedNodeChange.bind(this);
        this.state = {selectedNode: null, currentFolder: null, contents: []}
    }

    componentDidMount() {
        const result = ResolvePath();
        result.then(value => {
            console.log(value["contents"])
            this.setState({
                "currentFolder": value['name'],
                "contents": value["contents"],
            })
        });
    }

    handleCurrentFolderChange(currentFolder) {
        this.setState({currentFolder: currentFolder});
    }

    handleSelectedNodeChange(selectedNode) {
        this.setState({selectedNode: selectedNode});
    }

    handleContentsChange(contents) {
        this.setState({contents: contents});
    }

    render() {
        const contents = this.state.contents
        const currentFolder = this.state.currentFolder
        const selectedNode = this.state.selectedNode

        return (
            <div className="App">
                <Path
                    currentFolder={currentFolder}
                    onCurrentFolderChange={this.handleCurrentFolderChange} />
                <Controls
                    selectedNode={selectedNode}
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
