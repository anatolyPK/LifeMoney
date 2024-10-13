import React, {FormEvent, useEffect, useState} from "react";
import Form from "@/app/ui/Form";
import {formatTimestamp} from "@/app/lib/formatTimestamp";
import {useAuth} from "@/app/context/AuthContext";
import {CMApi} from "@/app/api/api";
import {Token} from "@/app/types";

interface DialogProps {
    header: string;
    id: number;
    onClose: () => void;
}

function Dialog(props: DialogProps) {
    const {header, id, onClose} = props;
    const {accessToken} = useAuth();
    const [operation, setOperation] = useState<string>('BUY');
    const [quantity, setQuantity] = useState<string>(`0`);
    const [priceInUsd, setPriceInUsd] = useState<string>(`0`);
    const [timestamp, setTimestamp] = useState<string>(`${Math.floor(new Date().getTime() / 1000)}`);
    const [tokenId, setTokenId] = useState<number>(0);
    const [tokenSymbol, setTokenSymbol] = useState<string>(``);
    const [tokensSearch, setTokensSearch] = useState<Token[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const result: Token[] = await CMApi.search(accessToken!, tokenSymbol);
                setTokensSearch(result);

                setLoading(false);
            } catch (err) {
                if (err instanceof Error) {
                    setError(err.message);
                } else {
                    setError('Неизвестная  при поиске токенов');
                }
            }

        }
        fetchData();
    }, [accessToken]);

    useEffect(() => {
        const selectedToken = tokensSearch.find(token => token.name === tokenSymbol);
        if (selectedToken) {
            setTokenId(selectedToken.id);
        } else {
            setTokenId(0);
        }
    }, [tokenSymbol]);

    const closeDialog = () => {
        onClose();
    };

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
            await CMApi.transactionsEdit(accessToken!, body, id);
            onClose();

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
        <div className = "block fixed inset-0 z-50 bg-black bg-opacity-50 overflow-auto">
            <div className = "flex items-center justify-center h-full">
                <div className = "bg-white rounded-lg shadow-lg p-6 w-11/12 md:w-1/3">
                    <span
                        className = "cursor-pointer text-blue-400 hover:text-amber-300 transition-colors float-right text-2xl"
                        onClick = {closeDialog}
                    >&times;</span>
                    <h2 className = "text-lg font-semibold">{header}</h2>
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
                        textButton = {loading ? 'Отправка данных...' : 'Внести изменения'}
                        loading = {loading}
                        error = {error}
                    />
                </div>
            </div>
        </div>
    );
}

export default Dialog;
