import React from "react";
import Link from "next/link";
import clsx from "clsx";

interface ButtonProps {
    className?: string;
    type: ButtonType;
    href?: string;
    onClick?: () => void;
    children: React.ReactNode;
    disabled?: boolean;
}

type ButtonType = keyof typeof styleButton;

const styleButton = {
    auth: `hover:text-amber-300 transition-colors`,
    actionNavbar: `w-52 py-2 bg-blue-400 rounded-lg shadow-md hover:text-amber-300 transition-colors `,
    headerNavbar:  `hover:text-amber-300 transition-colors`,
    submit:  `flex w-full justify-center rounded-md bg-blue-400 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-blue-600 transition-colors`,
    register:  `font-semibold leading-6 text-blue-400 hover:text-blue-600 transition-colors`,
    actionImage:  `h-8 w-8`,
}

const Button: React.FC<ButtonProps> = ({className, type, href, onClick, children, disabled}) =>
    href ? (
        <Link href={href}
              className={clsx(styleButton[type], className)}>{children}
        </Link>
    ) : (
        <button className={clsx(styleButton[type], className)}
                onClick={onClick}
                type={type === `submit` ? `submit` : undefined}
                disabled={disabled}>{children}
        </button>
    )

export default Button;