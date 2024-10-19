'use client'

import React, {ReactElement, useEffect, useState} from "react";
import {useAuth} from "@/app/context/AuthContext";
import Excel from "@/app/cryptosMarket/history/Excel";
import {CMApi} from "@/app/api/api";
import Dialog from "@/app/components/Dialog";
import {Transaction} from "@/app/types";


const fetchTransactions = async (accessToken:string, setError: any) => {
    try {
        return await CMApi.getTransactions(accessToken);
    } catch (err) {
        if (err instanceof Error) {
            setError(err.message);
        } else {
            setError('Неизвестная ошибка при получении истории транзакций');
        }
    }
}


export default function Page() {
    const [data, setData] = useState<Transaction[] | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [dialog, setDialog] = useState<ReactElement | null>(null);

    const {accessToken} = useAuth();
    const headers = [`№`, `Вид`, `Количество`, `Цена ($)`, `Дата`, `Название (тикер)`, `Действие`];

    useEffect(() => {
        fetchTransactions(accessToken!, setError).then(transactions => setData(transactions.reverse()));
    }, [accessToken, dialog]);


    const closeModal = () => setDialog(null);

    function handleActionButton(transaction: Transaction) {
        setDialog(<Dialog header = {`Внести изменения в транзакцию`}
                          transaction= {transaction}
                          onClose = {closeModal} />)
    }

    if (data === null) {
        return <div>Loading...</div>
    }
    return (
        <div>
            <div>{error && <p>Error: {error}</p>}</div>
            <Excel headers = {headers} data = {data} handleActionButton = {handleActionButton} />
            {dialog}
        </div>
    );
}
