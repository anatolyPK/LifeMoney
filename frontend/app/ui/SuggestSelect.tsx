import React from "react";
import {FormInputProps} from "@/app/ui/FormInput";

const SuggestSelect: React.FC<FormInputProps> = (props) => {
    const {type, options} = props;

    return (
        <>
         <select id = {options.id}
                 value={options.value}
                 onChange = {(e) => options.onChange(e.target.value)}
                 className = "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 indent-2.5"
         >
             {(options.optionsSuggest || []).map((option, idx) => (
                 <option key={idx} value={option.value}>{option.children}</option>
             ))}
         </select>
        </>
    );
}

export default SuggestSelect;