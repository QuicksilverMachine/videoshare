import "./Contents.css";
import React from "react";
import {
    Draggable,
    Droppable,
    DnDContextWithSensors,
} from "../dnd/DragAndDrop";
import { Node, NODE_TYPE_FOLDER } from "../node/Node";

export class Contents extends React.Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.handleDragEnd = this.handleDragEnd.bind(this);
    }

    handleClick(e) {
        e.preventDefault();
        if (e.target === e.currentTarget) {
            this.props.onSelectedNodeChange(null);
        }
    }

    handleDragEnd(e) {
        if (!e.over) {
            return;
        }
        if (e.active.id === e.over.id) {
            return;
        }
        if (e.over.data.current.type !== NODE_TYPE_FOLDER) {
            return;
        }
        this.props.onMoveNode(e.active.data.current, e.over.data.current);
        this.setState({ dragging: false });
    }

    render() {
        const selectedNode = this.props.selectedNode;
        const contents = this.props.contents;

        const selectedNodeId = selectedNode ? selectedNode.id : null;
        if (contents) {
            const listItems = contents.map((node) => (
                <Droppable
                    className="Droppable"
                    node={node}
                    key={node.id}
                    children={
                        <Draggable
                            className="Draggable"
                            node={node}
                            key={node.id}
                            children={
                                <Node
                                    id={node.id}
                                    node={node}
                                    selected={selectedNodeId === node.id}
                                    onSelectedNodeChange={
                                        this.props.onSelectedNodeChange
                                    }
                                    onContentsChange={
                                        this.props.onContentsChange
                                    }
                                />
                            }
                        />
                    }
                />
            ));
            return (
                <div
                    id="contentsContainer"
                    className="Contents"
                    onClick={this.handleClick}
                >
                    <DnDContextWithSensors onDragEnd={this.handleDragEnd}>
                        {listItems}
                    </DnDContextWithSensors>
                </div>
            );
        }
        return <div className="Contents" onClick={this.handleClick}></div>;
    }
}
