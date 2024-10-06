import React from "react";
import {TimePeriod} from "@/app/cryptosMarket/about/page";

interface SuggestSelectProps {
    value: TimePeriod,
    onChange: (value: TimePeriod) => void;
}

const SuggestSelect: React.FC<SuggestSelectProps> = (props) => {
    const {value, onChange} = props;

    const handleChange: React.ChangeEventHandler<HTMLSelectElement> = (event) => {
        onChange(event.target.value as TimePeriod);
    };

    return (
        <>
         <select id = "timePeriodSelect"
                 name = {`timePeriod`}
                 value={value}
                 onChange = {handleChange}
                 className = "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 indent-2.5"
         >
             <option value = {`daily`}>День</option>
             <option value = {`weekly`}>Неделя</option>
             <option value = {`monthly`}>Месяц</option>
             <option value = {`yearly`}>Год</option>
         </select>
        </>
    );
}

export default SuggestSelect;