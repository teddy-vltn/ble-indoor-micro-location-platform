import React from "react";
import mermaid from "mermaid";

export default class Mermaid extends React.Component {
    componentDidMount() {
        mermaid.contentLoaded();
    }
    render() {
        return <div className="mermaid">{this.props.chart}</div>;
    }
}