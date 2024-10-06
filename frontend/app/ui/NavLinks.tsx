'use client'

import {usePathname} from 'next/navigation'
import Button from "@/app/ui/Button";

export function NavLinks() {
    const pathname = usePathname();

    return (
        <nav className={`flex flex-row justify-between items-center gap-6`}>
            <div className = {`flex flex-row justify-around gap-6`}>
                <Button className = {`${pathname === '/dashboard' ? 'text-amber-300' : ''}`}
                        type={`headerNavbar`}
                        href={`/dashboard`}>Портфель
                </Button>
                <Button className = {`${pathname.startsWith(`/cryptosMarket`) ? 'text-amber-300' : ''}`}
                        type={`headerNavbar`}
                        href = "/cryptosMarket">Крипто рынок
                </Button>
            </div>
        </nav>
    )
}