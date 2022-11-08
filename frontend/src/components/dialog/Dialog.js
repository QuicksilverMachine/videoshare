import "./Dialog.css";
import React from "react";
import { DialogContent, DialogOverlay } from "@reach/dialog";
import "@reach/dialog/styles.css";

export class NameDialog extends React.Component {
    constructor(props) {
        super(props);
        this.handleNameChange = this.handleNameChange.bind(this);
        this.handleConfirmClick = this.handleConfirmClick.bind(this);
        this.handleCancelClick = this.handleCancelClick.bind(this);
        this.state = {
            name: "",
        };
    }

    handleNameChange(e) {
        this.setState({ name: e.target.value });
    }

    handleConfirmClick() {
        const name = this.state.name;
        this.setState({ name: "" });
        this.props.onConfirmClick(name);
    }

    handleCancelClick() {
        this.setState({ name: "" });
        this.props.onCancelClick();
    }

    render() {
        const isOpen = this.props.showDialog;
        const nodeType = this.props.nodeType;
        // noinspection RequiredAttributes
        return (
            <div className="Dialog">
                <DialogOverlay
                    className="DialogOverlay"
                    isOpen={isOpen}
                    onDismiss={this.handleCancelClick}
                >
                    <DialogContent className="DialogContent">
                        <p className="DialogText">Enter new {nodeType} name</p>
                        <div className="DialogNameContainer">
                            <input
                                className="DialogName"
                                onChange={this.handleNameChange}
                                type="text"
                            />
                        </div>
                        <div className="DialogButtonsContainer">
                            <button
                                className="DialogButton"
                                onClick={this.handleConfirmClick}
                            >
                                Confirm
                            </button>
                            <button
                                className="DialogButton"
                                onClick={this.handleCancelClick}
                            >
                                Cancel
                            </button>
                        </div>
                    </DialogContent>
                </DialogOverlay>
            </div>
        );
    }
}
