'use client';

import {FormEvent, useState} from 'react';
import {useRouter} from 'next/navigation';
import {useAuth} from "@/app/context/AuthContext";
import Button from "@/app/ui/Button";
import {AuthAPI} from "@/app/api/api";
import Form from "@/app/ui/Form";

export default function SignIn() {
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const router = useRouter();
    const {login} = useAuth();


    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const data = await AuthAPI.login(username, password);
            login(data.access_token);
            router.push('/dashboard'); // Перенаправляем на защищенную страницу
        } catch (err) {
            if (err instanceof Error) {
                setError(err.message);
            } else {
                setError('Неизвестная ошибка при авторизации');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className = {'flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8'}>
            <div className = "sm:mx-auto sm:w-full sm:max-w-sm">
                <h2 className = "mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
                    Войти в Ваш профиль
                </h2>
            </div>

            <div className = "mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
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

                <p className = "mt-10 text-center text-sm text-gray-500">
                    Отсутсвует профиль? {` `}
                    <Button type = {"register"} href = {'/register'}>Зарегистрироваться...</Button>
                </p>
            </div>
        </div>
    )
}