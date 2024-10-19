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
          <button>Может какой-нибудь виджет для заметок и тп</button>
        </li>

      </ul>
    </div>
    );
}
