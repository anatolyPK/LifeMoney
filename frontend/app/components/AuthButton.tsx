'use client';

import { useAuth } from '../context/AuthContext';
import {usePathname, useRouter} from 'next/navigation';
import Button from "@/app/ui/Button";

const AuthButton = () => {
    const { isAuthenticated, logout } = useAuth();
    const router = useRouter();
    const pathname = usePathname();

    const handleLogout = () => {
        logout();
        router.push('/'); // Перенаправление на страницу входа после выхода
    };

    return (
        <Button className = {`${pathname === '/login' ? 'text-amber-300' : ''}`}
                type={'auth'}
                onClick={isAuthenticated ? handleLogout : () => router.push('/login')}
                >
            {isAuthenticated ? 'Выйти' : 'Войти'}
        </Button>
    );
};

export default AuthButton;