import React from 'react';
import "./fakebashinterface.css";
import { useEffect, useRef } from 'react';

/**
 * FakeBashInterface component displays a terminal-like interface with the
 * provided output. It automatically scrolls to the bottom when the output
 * changes.
 *
 * @param {Object} props - The component props.
 * @param {string} props.output - The output to display in the terminal.
 * @return {JSX.Element} The FakeBashInterface component.
 */
const FakeBashInterface = ({ output }) => {
    // Create a ref to the terminal body element.
    const terminalRef = useRef(null);

    /**
     * Scrolls the terminal body to the bottom when the output changes.
     */
    useEffect(() => {
        // Check if the terminal body element exists.
        if (terminalRef.current) {
            // Scroll to the bottom of the terminal body.
            terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
        }
    }, [output]);

    return (
        // Render the terminal wrapper.
        <div className="terminalWrapper">
            {/* Render the terminal header. */}
            <div className="terminalHeader">
                <span>Terminal</span>
            </div>
            {/* Render the terminal body and attach the ref. */}
            <div className="terminalBody" ref={terminalRef}>
                {/* Render the output in a pre element. */}
                <pre>{output}</pre>
            </div>
        </div>
    );
};

export default FakeBashInterface;
