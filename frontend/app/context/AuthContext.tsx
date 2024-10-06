'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

interface AuthContextType {
    isAuthenticated: boolean | null;
    accessToken: string | null;
    login: (token: string) => void;
    logout: () => void;
    refreshToken: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(() => {
        const token = localStorage.getItem('access_token');
        return !!token ; // Если токен есть, считаем, что пользователь аутентифицирован
    });
    const [accessToken, setAccessToken] = useState<string | null>(() => {
        return localStorage.getItem('access_token');
    });

    useEffect(() => {

        // Устанавливаем интервал для обновления токена
        const interval = setInterval(() => {
            refreshToken();
        }, 50 * 60 * 1000); // 50 минут

        // Очистка интервала при размонтировании компонента
        return () => clearInterval(interval);
    }, []);


    const login = (token: string) => {
        localStorage.setItem('access_token', token);
        setAccessToken(token)
        setIsAuthenticated(true);
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        setAccessToken(null);
        setIsAuthenticated(false);
    };

    const refreshToken = async () => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Токен авторизации не надйен');
        }

        try {
            const response = await fetch('http://localhost:8000/api/v1/auth/refresh', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'accept': 'application/json',
                    'x-device-fingerprint': 's',
                },
            });

            if (!response.ok) {
                throw new Error('Ошибка запроса');
            }

            const data = await response.json();
            const newToken = data.access_token;
            localStorage.setItem('access_token', newToken);
        } catch (error) {
            console.error('Ошибка обнолвения токена:', error);
            logout(); // Выйти, если не удалось обновить токен
        }
    };


    return (
        <AuthContext.Provider value={{ isAuthenticated, accessToken, login, logout, refreshToken }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
