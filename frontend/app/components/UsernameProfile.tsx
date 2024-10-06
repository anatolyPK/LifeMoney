'use client';

import React, {useEffect, useState} from "react";
import {useAuth} from "@/app/context/AuthContext";
import {UserAPI} from "@/app/api/api";

interface User {
    id: string;                // Уникальный идентификатор пользователя
    username: string;         // Имя пользователя
    email: string;            // Электронная почта
    is_active: boolean;       // Статус активности пользователя
    is_superuser: boolean;    // Статус суперпользователя
    is_verified: boolean;     // Статус верификации пользователя
    logged_in_at: number;     // Время входа в формате timestamp (число)
}

const UsernameProfile: React.FC = () => {
    const {isAuthenticated, accessToken} = useAuth();
    const [user, setUser] = useState<User | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (isAuthenticated) {
            const fetchData = async () => {
                try {
                    const result: User = await UserAPI.me(accessToken!);
                    setUser(result);
                } catch (err) {
                    if (err instanceof Error) {
                        setError(err.message);
                    } else {
                        setError('Неизвестная ошибка (запрос профиля)');
                    }
                }
            }
            fetchData();
        } else {
            setUser(null);
        }


    }, [isAuthenticated, accessToken]);


    return (
        <div>
            {error ? <p>{error}</p> : null}
            {user ? user.username : null}
        </div>
    );
};

export default UsernameProfile;