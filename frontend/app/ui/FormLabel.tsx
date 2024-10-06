import React from "react";

interface FormLabelProps {
    htmlFor: string;
    className?: string;
    children: string;
}

const FormInput: React.FC<FormLabelProps> = (props) => {
    const {htmlFor, className, children} = props;

    return (
        <>
            <label htmlFor = {htmlFor}
                   className = {className}>
                {children}
            </label>
        </>
    );
}

export default FormInput;