'use client';

import React, {FormEvent, useEffect, useState} from 'react';
import {useAuth} from "@/app/context/AuthContext";
import {formatTimestamp} from "@/app/lib/formatTimestamp";
import Button from "@/app/ui/Button";
import SuggestData from "@/app/ui/SuggestData";
import FormInput from "@/app/ui/FormInput";
import {CMApi} from "@/app/api/api";
import FormLabel from "@/app/ui/FormLabel";

// Определяем интерфейс для токена
export interface Token {
    id: number;
    name: string;
    symbol: string;
    cg_id: string;
}


export default function SignIn() {
    const {accessToken} = useAuth();
    const [operation, setOperation] = useState<string>('BUY');
    const [quantity, setQuantity] = useState<string>(`0`);
    const [priceInUsd, setPriceInUsd] = useState<string>(`0`);
    const [timestamp, setTimestamp] = useState<string>(`${Math.floor(new Date().getTime() / 1000)}`);
    const [tokenId, setTokenId] = useState<number>(0);
    const [tokenSymbol, setTokenSymbol] = useState<string>(``);
    const [tokensSearch, setTokensSearch] = useState<Token[]>([]);
    const [balanceTokens, setBalanceTokens] = useState<string>(`0`);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [highlight, setHighlight] = useState(false);


    useEffect(() => {
        const fetchData = async () => {
            try {
                const result = await CMApi.balance(accessToken!, tokenId);
                setBalanceTokens(result);
            } catch (err) {
                if (err instanceof Error) {
                    setError(err.message);
                } else {
                    setError('Неизвестная ошибка при запросе баланса');
                }
            }
        }
        fetchData();

    }, [accessToken, tokenId]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const result: Token[] = await CMApi.search(accessToken!, tokenSymbol);
                setTokensSearch(result);
            } catch (err) {
                if (err instanceof Error) {
                    setError(err.message);
                } else {
                    setError('Неизвестная  при поиске токенов');
                }
            }
        }
        fetchData();
    }, [accessToken,tokenSymbol]);


    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        const body = {
            "operation": operation,
            "quantity": quantity,
            "price": priceInUsd,
            "timestamp": timestamp,
            "token_id": tokenId
        }
        try {
            await CMApi.transactions(accessToken!, body);

            // Обновление формы после успешной отправки
            setOperation('BUY');
            setQuantity(`0`);
            setPriceInUsd(`0`);
            setTimestamp(`${Math.floor(new Date().getTime() / 1000)}`);
            setTokenId(0);
            setTokenSymbol(``);
            setTokensSearch([]);
            setBalanceTokens(`0`);
            // Дополнительные действия, уведомление пользователя
            setHighlight(true);
            setTimeout(() => {
                setHighlight(false);
            }, 2000); // Подсветка будет длиться 2 секунды

        } catch (err) {
            if (err instanceof Error) {
                setError(err.message);
            } else {
                setError('Неизвестная ошибка при отравке транзакции');
            }
        } finally {
            setLoading(false);
        }
    };


    return (
        <div className = {'flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8'}>
            <div className = "sm:mx-auto sm:w-full sm:max-w-sm">
                <h2 className = "mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
                    Провести транзакцию
                </h2>

            </div>

            <div className = "mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
                <form onSubmit = {handleSubmit} className = "space-y-6">

                    <div>
                        <FormLabel htmlFor={`operation`}>Вид операции</FormLabel>
                        <div className = "mt-2">
                            <select
                                id = "operations"
                                name = "operation"
                                value = {operation}
                                onChange = {(e) => setOperation(e.target.value)}
                                className = "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 indent-2.5"
                            >
                                <option value = "BUY">Покупка</option>
                                <option value = "SELL">Продажа</option>
                            </select>
                        </div>
                    </div>

                    <div>
                        <FormLabel htmlFor={`quantity`}>Количество</FormLabel>
                        <div className = "mt-2">
                            <FormInput type = {`number`}
                                       id = {`quantity`}
                                       value = {quantity}
                                       onChange = {setQuantity}
                                       min = {`0`}
                                       required = {true}
                            />
                        </div>
                    </div>

                    <div>
                        <FormLabel htmlFor={`price_in_usd`}>Цена ( $ ):</FormLabel>
                        <div className = "mt-2">
                            <FormInput type = {`number`}
                                       id = {`price_in_usd`}
                                       value = {priceInUsd}
                                       onChange = {setPriceInUsd}
                                       min = {`0`}
                                       required = {true}
                            />
                        </div>
                    </div>

                    <div>
                        <FormLabel htmlFor={`timestamp`}>Время операции:</FormLabel>
                        <div className = "mt-2">
                            <FormInput type = {`date`}
                                       id = {`timestamp`}
                                       value = {formatTimestamp(timestamp)}
                                       onChange = {setTimestamp}
                                       required = {true}
                            />
                        </div>
                    </div>

                    <div>
                        <FormLabel htmlFor={`tokenId`}>Название токена:</FormLabel>
                        <div className = "mt-2">
                            <SuggestData tokenSymbol = {tokenSymbol}
                                         setTokenSymbol = {setTokenSymbol}
                                         tokensSearch = {tokensSearch}
                                         setTokenId = {setTokenId} />
                            {tokenId ? (<div>Баланас: {balanceTokens}</div>) : null}
                        </div>
                    </div>

                    <div>
                        <Button type = {"submit"}
                                disabled = {loading}>{loading ? 'Отправка данных...' : 'Отправить данные'}</Button>
                        {highlight ? `Успешно` : ``}
                    </div>
                    {error && <p style = {{color: 'red'}}>{error}</p>}
                </form>
            </div>
        </div>
    )
}