import FormInput from "@/app/ui/FormInput";
import FormLabel from "@/app/ui/FormLabel";
import React from "react";
import Button from "@/app/ui/Button";
import SuggestSelect from "@/app/ui/SuggestSelect";
import SuggestData from "@/app/ui/SuggestData";
import {Field} from "@/app/types";


interface FormProps {
    fields: {
        [key: string]: Field;
    };
    onSubmit: React.FormEventHandler<HTMLFormElement>;
    textButton: string;
    loading: boolean;
    error: string | null;

}

const Form: React.FC<FormProps> = (props) => {
    const {fields, onSubmit, textButton, loading, error} = props;

    if (loading) {
        return (
            <div>
                Loading...
            </div>
        );

    }

    return (
        <form className = "space-y-6" onSubmit={onSubmit} >

            {Object.keys(fields).map((id) => {
                const {label, type, options} = fields[id];
                return (
                    <div key = {options.id}>
                        <FormLabel htmlFor={options.id}>{label}</FormLabel>
                        { (type === `suggestSelect`) ? <SuggestSelect type = {type} options={options} /> :
                            (type === `suggestDatalist`) ? <SuggestData type = {type} options={options} /> :
                                <FormInput type={type} options={options} />
                        }
                    </div>
                );
            })}
            <div>
                <Button type = {'submit'} disabled = {loading}>{textButton}</Button>
            </div>
            {error && <p style = {{color: 'red'}}>{error}</p>}
        </form>
    )
};

export default Form;