'use client'

import {usePathname} from "next/navigation";
import Button from "@/app/ui/Button";

export default function RightActionNavbar() {
    const pathname = usePathname();

    return (
        <div className = {`basis-1/6 h-40 sticky top-[250px] text-white`}>
      <ul className = {`flex flex-col gap-3 items-start text-center`}>
        <li
            className = {`w-52 py-2 bg-blue-400 rounded-lg hover:text-amber-300 transition-colors shadow-md`}
        >
          <button>Внести средства (XXX)</button>
        </li>
        <Button className = {`${pathname === '/cryptosMarket/transactions' ? 'text-amber-300' : ''}`}
                type={`actionNavbar`}
                href = {`/cryptosMarket/transactions`}>Провести операцию
        </Button>
        <li
            className = {`w-52 py-2 bg-blue-400 rounded-lg hover:text-amber-300 transition-colors shadow-md`}
        >
          <button>Транзакция (XXX)</button>
        </li>
      </ul>
    </div>
    );
}
