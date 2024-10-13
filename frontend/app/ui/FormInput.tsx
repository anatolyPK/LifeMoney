import React from "react";
import {OptionsFormInput, TypeFormInput} from "@/app/types";


export interface FormInputProps {
    type: TypeFormInput,
    options: OptionsFormInput,
}

const FormInput: React.FC<FormInputProps> = (props) => {
    const {type, options} = props;

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (type === `date`) {
            options.onChange(`${Math.floor(new Date(e.target.value).getTime() / 1000)}`);
        } else {
            options.onChange(e.target.value);
        }
    };

    return (
        <>
            <input
                type = {type}
                className = "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 indent-2.5"
                id = {options.id}
                value = {options.value}
                onChange = {handleChange}
                placeholder = {options.placeholder}
                required = {options.required}
                autoComplete = {options.autoComplete}
                min = {options.min}
            />
        </>
    );
}

export default FormInput;