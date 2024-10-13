import React from "react";
import {FormInputProps} from "@/app/ui/FormInput";

const SuggestData: React.FC<FormInputProps> = (props) => {
    const {type, options} = props;

    return (
        <>
         <input
             type = {type}
             id = {options.id}
             value = {options.value}
             onChange = {(e) => options.onChange(e.target.value)}
             required
             list={options.id + `List`}
             className = "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6 indent-2.5"
         />
         <datalist id = {options.id + `List`}>
             {(options.optionsDatalist || []).map((item) =>
                     <option key = {item.id} value = {item.name}/>
             )}
         </datalist>

        </>
    );
}

export default SuggestData;