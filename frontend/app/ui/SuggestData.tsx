import {Token} from "@/app/cryptosMarket/transactions/page";
import React from "react";

interface SuggestDataProps {
    value: string;
    onChange: (tokenSymbol: string) => void;
    suggestData: Token[];
    setTokenId: (tokenId: number) => void
}

const SuggestData: React.FC<SuggestDataProps> = (props) => {
    const {value, onChange, suggestData, setTokenId} = props;
    return (
        <>
         <input
             type = "text"
             id = "tokenId"
             list = 'tokenIds'
             value = {value}
             onChange = {(e) => {
                 onChange(e.target.value);
                 const selectedValue = e.target.value;
                 const selectedToken = suggestData.find(item => item.name === selectedValue);
                 if (selectedToken) {
                     setTokenId(selectedToken.id);
                 } else {
                     setTokenId(0);
                 }
             }}
             required
             className = "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 indent-2.5"
         />
         <datalist id = "tokenIds">
             {suggestData.map((item) => {
                 return (
                     <option key = {item.id} value = {item.name} />
                 );
             })}
         </datalist>
        </>
    );
}

export default SuggestData;