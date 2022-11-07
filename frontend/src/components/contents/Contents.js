import './Contents.css';
import React from "react";


export class Contents extends React.Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(e) {
        this.props.onSelectedNodeChange(e.target.value);
        this.props.onContentsChange(e.target.value);
    }

    render() {
        const selectedNode = this.props.selectedNode;
        const contents = this.props.contents;
        const listItems = contents.map((item) =>  <li key={item.id}>{item.name}</li>);

        // Make component for each
        return (
            <div className="Contents">
                <ul>{listItems}</ul>
            </div>
        )
    }
}
