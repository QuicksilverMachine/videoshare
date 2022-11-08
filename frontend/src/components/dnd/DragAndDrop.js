import "./DragAndDrop.css";
import React from "react";

import {
    DndContext,
    MouseSensor,
    useDraggable,
    useDroppable,
    useSensor,
    useSensors,
} from "@dnd-kit/core";

export function Draggable(props) {
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

export function Droppable(props) {
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

export function DnDContextWithSensors(props) {
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
