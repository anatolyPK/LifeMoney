'use client';

import {usePathname, useRouter} from "next/navigation";


export default  function Page() {
    const pathname = usePathname();
    const router = useRouter();

    if (pathname === '/cryptosMarket') {
        router.push("/cryptosMarket/about");
    }
    return <></>;
}
