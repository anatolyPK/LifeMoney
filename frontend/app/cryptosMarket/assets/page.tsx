'use client'

import {useEffect, useState} from "react";
import {CMApi} from "@/app/api/api";
import {useAuth} from "@/app/context/AuthContext";
import {CryptosPortfolio} from "@/app/types";

const fetchCryptos = async (accessToken:string, setError: any) => {
    try {
        return await CMApi.getCryptos(accessToken!);
    } catch (err) {
        if (err instanceof Error) {
            setError(err.message);
        } else {
            setError('Неизвестная ошибка при запросе крипто портфеля');
        }
    }
}

export default function Page() {
    const [data, setData] = useState<CryptosPortfolio | null>(null);
    const [error, setError] = useState<string | null>(null);
    const {accessToken} = useAuth();

    useEffect(() => {
        fetchCryptos(accessToken!, setError).then(cryptos => setData(cryptos));
    }, [accessToken]);


    if (data === null) {
        return <div>Loading...</div>
    }
    return (
        <div>
              ЖОПА
        </div>
    );
}
