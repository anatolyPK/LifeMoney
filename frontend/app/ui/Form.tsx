import FormInput, {OptionsFormInput, TypeFormInput} from "@/app/ui/FormInput";
import FormLabel from "@/app/ui/FormLabel";
import React from "react";
import Button from "@/app/ui/Button";

export interface Field {
    label: string; // Метка поля
    type: TypeFormInput; // Тип поля (например, email, password)
    options: OptionsFormInput; // Опции для поля
}

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

    return (
        <form className = "space-y-6" onSubmit={onSubmit}>
            {Object.keys(fields).map((id) => {
                const {label, type, options} = fields[id];
                return (
                    <div key = {options.id}>
                        <FormLabel htmlFor={options.id}>{label}</FormLabel>
                        <FormInput type={type} options={options} />
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