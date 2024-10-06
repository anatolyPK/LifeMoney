'use client';

import {FormEvent, useState} from 'react';
import { useRouter } from 'next/navigation';
import Button from "@/app/ui/Button";
import FormInput from "@/app/ui/FormInput";
import {AuthAPI} from "@/app/api/api";
import FormLabel from "@/app/ui/FormLabel";
import Form from "@/app/ui/Form";

const Register = () => {
    const [username, setUsername] = useState<string>('');
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const router = useRouter();

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            await AuthAPI.register(username, email, password);
            router.push('/login');
        } catch (err) {
            if (err instanceof Error) {
                setError(err.message);
            } else {
                setError('Неизвестная ошибка при регстрации');
            }
        } finally {
            setLoading(false);
        }
    }

    return (
        <div
              className = {'flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8'}>
            <div className = "sm:mx-auto sm:w-full sm:max-w-sm">
                <h2 className = "mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
                    Регистрация профиля
                </h2>
            </div>

            <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
                <Form
                    fields = {
                        {
                            email: {
                                label: `Электронная почта`,
                                type: `email`,
                                options: {
                                    id: `email`,
                                    value: username,
                                    onChange: setUsername,
                                    placeholder: `user@example.com`,
                                    autoComplete: "email",
                                    required: true,
                                }
                            },
                            password: {
                                label: `Пароль`,
                                type: `password`,
                                options: {
                                    id: `password`,
                                    value: password,
                                    onChange: setPassword,
                                    placeholder: `*****`,
                                    autoComplete: "password",
                                    required: true,
                                }

                            },
                        }
                    }
                    onSubmit = {handleSubmit}
                    textButton = {loading ? 'Вход...' : 'Войти'}
                    loading={loading}
                    error={error}
                />
                
                <form onSubmit = {handleSubmit} className = "space-y-6">
                    <div>
                        <FormLabel htmlFor={`username`}>Имя пользователя</FormLabel>
                        <div className = "mt-2">
                             <FormInput type={`text`}
                                        id={`username`}
                                        value={username}
                                        onChange={setUsername}
                                        placeholder={`Имя пользователя`}
                                        autoComplete={"username"}
                                        required = {true}
                             />
                        </div>
                    </div>

                    <div>
                        <FormLabel htmlFor={`email`}>Электронная почта</FormLabel>
                        <div className = "mt-2">
                             <FormInput type={`email`}
                                        id={`email`}
                                        value={email}
                                        onChange={setEmail}
                                        placeholder={`user@example.com`}
                                        autoComplete={"email"}
                                        required = {true}
                             />
                        </div>
                    </div>

                    <div>
                        <FormLabel htmlFor={`password`}>Пароль</FormLabel>
                        <div className = "mt-2">
                            <FormInput type={`password`}
                                       id={`password`}
                                       value={password}
                                       onChange={setPassword}
                                       placeholder={`*****`}
                                       autoComplete={"password"}
                                       required = {true}
                            />
                        </div>
                    </div>

                    <div>
                        <Button type={`submit`} disabled = {loading}>{loading ? 'Регистрация...' : 'Зарегистрироваться'}</Button>
                    </div>
                    {error && <p style = {{color: 'red'}}>{error}</p>}
                </form>
            </div>

     </div>
    );
};

export default Register;
