'use client';

import {FormEvent, useState} from 'react';
import {useRouter} from 'next/navigation';
import {AuthAPI} from "@/app/api/api";
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
                            username: {
                                label: `Имя пользователя`,
                                type: `text`,
                                options: {
                                    id: `username`,
                                    value: username,
                                    onChange: setUsername,
                                    placeholder: `Имя пользователя`,
                                    autoComplete: "username",
                                    required: true,
                                }
                            },
                            email: {
                                label: `email`,
                                type: `email`,
                                options: {
                                    id: `email`,
                                    value: email,
                                    onChange: setEmail,
                                    placeholder: `user@example.com`,
                                    autoComplete: "email",
                                    required: true,
                                },
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
                    textButton = {loading ? 'Регистрация...' : 'Зарегистрироваться'}
                    loading={loading}
                    error={error}
                />
            </div>

     </div>
    );
};

export default Register;
