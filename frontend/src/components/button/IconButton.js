import './IconButton.css'
import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";


export class IconButton extends React.Component {

    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this)
    }

    handleClick(e) {
        if (this.props.onClick) {
            this.props.onClick(e.target.value);
        }
    }

    render() {
        const icon = this.props.icon;
        const title = this.props.title;
        const disabled = this.props.disabled;
        return <button className="IconButton" title={title} disabled={disabled} onClick={this.handleClick}>
            <FontAwesomeIcon icon={icon} />
        </button>
    }
}
