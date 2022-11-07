import './Button.css'
import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";


export class Button extends React.Component {

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
        const help = this.props.help;
        const disabled = this.props.disabled;
        return <button className="Button" title={help} disabled={disabled} onClick={this.handleClick}>
            <FontAwesomeIcon icon={icon} />
        </button>
    }
}
