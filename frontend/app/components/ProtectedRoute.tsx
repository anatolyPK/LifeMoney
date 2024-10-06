'use client';

import React, { useEffect, useState } from 'react';

import { useAuth } from '../context/AuthContext';
import {useRouter} from "next/navigation";

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const { isAuthenticated, accessToken, refreshToken } = useAuth();
    const router = useRouter();
    const [loading, setLoading] = useState(true); // Индикатор загрузки


    useEffect(() => {
        if (isAuthenticated === null) {
            setLoading(false);
            return;
        }
        if (!isAuthenticated) {
            setLoading(false);
            router.push('/login'); // Перенаправление на страницу входа
        }
        setLoading(false);
    }, [isAuthenticated, accessToken, router, refreshToken]);

    if (loading) {
        return <div>Loading...</div>; // Индикатор загрузки
    }

    return <>{children}</>;
};

export default ProtectedRoute;
