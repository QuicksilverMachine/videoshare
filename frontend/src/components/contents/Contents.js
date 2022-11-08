import "./Contents.css";
import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
    faFile,
    faFileVideo,
    faFolder,
} from "@fortawesome/free-regular-svg-icons";
import {
    DndContext,
    MouseSensor,
    useDraggable,
    useDroppable,
    useSensor,
    useSensors,
} from "@dnd-kit/core";

function Draggable(props) {
    const { attributes, listeners, setNodeRef, transform } = useDraggable({
        id: props.node.id,
        data: props.node,
    });

    const style = transform
        ? {
              transform: `translate3d(${transform.x}px, ${transform.y}px, 0)`,
          }
        : undefined;

    return (
        <button
            className="DraggableButton"
            ref={setNodeRef}
            style={style}
            {...listeners}
            {...attributes}
        >
            {props.children}
        </button>
    );
}

function Droppable(props) {
    const { setNodeRef } = useDroppable({
        id: props.node.id,
        data: props.node,
    });

    return (
        <div className="DroppableContainer" ref={setNodeRef}>
            {props.children}
        </div>
    );
}

function DnDContextWithSensors(props) {
    const mouseSensor = useSensor(MouseSensor, {
        // Require the mouse to move by 10 pixels before activating
        activationConstraint: {
            distance: 10,
        },
    });
    const sensors = useSensors(mouseSensor);
    return (
        <DndContext sensors={sensors} onDragEnd={props.onDragEnd}>
            {props.children}
        </DndContext>
    );
}

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
        if (e.over.data.current.type !== "folder") {
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
