'use client';

import {usePathname} from "next/navigation";
import Button from "@/app/ui/Button";

export default function LeftActionNavbar() {
  const pathname = usePathname();

    return (
        <div className={`basis-1/6 h-40 sticky top-[250px] text-white `}>
          <div className={`flex flex-col gap-3 items-end text-center`}>
              <Button className = {`${pathname === '/cryptosMarket/about' ? 'text-amber-300' : ''}`}
                    type={`actionNavbar`}
                    href={`/cryptosMarket/about`}>Общая иформация
              </Button>

              <Button className = {`${pathname === '/cryptosMarket/history' ? 'text-amber-300' : ''}`}
                    type={`actionNavbar`}
                    href={`/cryptosMarket/history`}>История операций
              </Button>
              <Button className = {`${pathname === '/cryptosMarket/transactions' ? 'text-amber-300' : ''}`}
                type={`actionNavbar`}
                href = {`/cryptosMarket/transactions`}>Провести операцию
              </Button>
          </div>
      </div>
    );
}
