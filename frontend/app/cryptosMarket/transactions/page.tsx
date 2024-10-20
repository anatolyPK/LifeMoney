'use client';

import React, {FormEvent, useEffect, useState} from 'react';
import {useAuth} from "@/app/context/AuthContext";
import {CMApi} from "@/app/api/api";
import Form from "@/app/ui/Form";
import {formatTimestamp} from "@/app/utils/formatTimestamp";
import {Token} from "@/app/types";


const fetchBalance = async (accessToken: string, tokenId: number, setError: any) => {
    try {
        return await CMApi.balance(accessToken, tokenId);
    } catch (err) {
        if (err instanceof Error) {
            setError(err.message);
        } else {
            setError('Неизвестная ошибка при запросе баланса');
        }
    }
}

const fetchTokensSearch = async (accessToken: string, tokenSymbol: string, setError: any) => {
    try {
        return await CMApi.search(accessToken, tokenSymbol);
    } catch (err) {
        if (err instanceof Error) {
            setError(err.message);
        } else {
            setError('Неизвестная  при поиске токенов');
        }
    }

}


export default function Transaction() {
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
        if (tokenId) {
            fetchBalance(accessToken!, tokenId, setError).then(balance => setBalanceTokens(balance));
        }
    }, [accessToken, tokenId]);

    useEffect(() => {
        fetchTokensSearch(accessToken!, tokenSymbol, setError).then(TokensSearch => setTokensSearch(TokensSearch));
    }, [accessToken, tokenSymbol]);


    useEffect(() => {
        const selectedToken = tokensSearch.find(token => token.name === tokenSymbol);
        if (selectedToken) {
            setTokenId(selectedToken.id);
        } else {
            setTokenId(0);
        }
    }, [tokenSymbol, tokensSearch]);

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
            // setTokensSearch([]);
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

                <Form
                    fields = {
                        {
                            operation: {
                                label: `Вид операции`,
                                type: `suggestSelect`,
                                options: {
                                    id: `operation`,
                                    value: operation,
                                    onChange: setOperation,
                                    required: true,
                                    optionsSuggest: [
                                        {
                                            value: `BUY`,
                                            children: `Покупка`
                                        },
                                        {
                                            value: `SELL`,
                                            children: `Продажа`
                                        },
                                    ]
                                }
                            },
                            number: {
                                label: `Количество`,
                                type: `number`,
                                options: {
                                    id: `quantity`,
                                    value: quantity,
                                    onChange: setQuantity,
                                    placeholder: `0`,
                                    min: `0`,
                                    required: true,
                                }
                            },
                            priceInUsd: {
                                label: `Цена ( $ ):`,
                                type: `number`,
                                options: {
                                    id: `priceInUsd`,
                                    value: priceInUsd,
                                    onChange: setPriceInUsd,
                                    placeholder: `0`,
                                    min: `0`,
                                    required: true,
                                }
                            },
                            timestamp: {
                                label: `Время операции:`,
                                type: `date`,
                                options: {
                                    id: `timestamp`,
                                    value: formatTimestamp(timestamp),
                                    onChange: setTimestamp,
                                    required: true,
                                }
                            },
                            tokenSymbol: {
                                label: `Название токена:`,
                                type: `suggestDatalist`,
                                options: {
                                    id: `tokenSymbol`,
                                    value: tokenSymbol,
                                    onChange: setTokenSymbol,
                                    required: true,
                                    optionsDatalist: tokensSearch,
                                }
                            },
                        }
                    }
                    onSubmit = {handleSubmit}
                    textButton = {loading ? 'Отправка данных...' : 'Отправить данные'}
                    loading = {loading}
                    error = {error}
                />
                {tokenId ? (<div>Баланс: {balanceTokens}</div>) : null}
                {highlight ? <span>Успешно</span> : null}
            </div>
        </div>
    )
}