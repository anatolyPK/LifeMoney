'use client'

import React, {useEffect, useState} from "react";
import {useAuth} from "@/app/context/AuthContext";
import Excel from "@/app/cryptosMarket/history/Excel";
import {CMApi} from "@/app/api/api";


interface Token {
    id: number;
    name: string;
    symbol: string;
    cg_id: string;
}

interface Transaction {
    operation: 'BUY' | 'SELL';
    quantity: number;
    price: number;
    timestamp: string;
    token: Token;
    id: number;
}


export default function Page() {
    const [data, setData] = useState<Transaction[] | null>(null);
    const [error, setError] = useState<string | null>(null);
    const {accessToken} = useAuth();
    const headers = [`№`, `Вид`, `Количество`, `Цена ($)`, `Дата`, `Название (тикер)`, `Действие`];


    useEffect(() => {
        const fetchData = async () => {
            try {
                const result: Transaction[] = await CMApi.getTransactions(accessToken!);
                setData(result.reverse());
            } catch (err) {
                if (err instanceof Error) {
                    setError(err.message);
                } else {
                    setError('Неизвестная ошибка при получении истории транзакций');
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
            <div>{error && <p>Error: {error}</p>}</div>
            <Excel data = {data} />
        </div>
    );
}
