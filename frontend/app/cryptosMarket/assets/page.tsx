'use client'

import {useEffect, useState} from "react";
import {CMApi} from "@/app/api/api";
import {useAuth} from "@/app/context/AuthContext";


interface CryptosPortfolio {
    total: number,
    assets:
        {
            token: {
                id: number,
                name: string,
                symbol: string,
                cg_id: string
            },
            quantity: number,
            average_price_buy: number,
            balance: number,
            current_price: number,
            profit_in_currency: number,
            profit_in_percent: number,
            percent_of_portfolio: number
        }[]
}


export default  function Page() {
    const [data, setData] = useState<CryptosPortfolio | null>(null);
    const [error, setError] = useState<string | null>(null);
    const {accessToken} = useAuth();

    useEffect(() => {
            const fetchData = async () => {
                try {
                    const result: CryptosPortfolio = await CMApi.getCryptos(accessToken!);
                    setData(result);
                } catch (err) {
                    if (err instanceof Error) {
                        setError(err.message);
                    } else {
                        setError('Неизвестная ошибка при запросе крипто портфеля');
                    }
                }
            }
            fetchData();
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
