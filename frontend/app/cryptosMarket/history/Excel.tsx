'use client'

import React from "react";
import {formatTimestamp} from "@/app/lib/formatTimestamp";
import editImage from "@/public/editImage.svg";
import deleteImage from "@/public/deleteImage.svg";
import Image from "next/image";
import Button from "@/app/ui/Button";


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

interface ExcelProps {
    data: Transaction[];
}


export default  function Excel({ data }: ExcelProps) {
    const headers = [ `№`, `Вид`, `Количество`, `Цена ($)`, `Дата`, `Название (тикер)`, `Действие`];

    return (
        <table className = {`m-2 p-2`}>
            <thead>
                <tr>{headers.map((title,idx) => {
                    return (
                        <th key={idx} className = {`m-2 p-2 font-bold border-2  border-solid border-blue-400`}>{title}</th>
                    )
                })}</tr>
            </thead>
            <tbody>
                {data.map((transaction) => {
                    return (
                        <tr key={transaction.id}>
                            <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{transaction.id} </td>
                            <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{transaction.operation}</td>
                            <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{transaction.quantity}</td>
                            <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{transaction.price}</td>
                            <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{formatTimestamp(transaction.timestamp)}</td>
                            <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{transaction.token.name} ({transaction.token.symbol})</td>
                            <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>
                                <Button type={`actionImage`}><Image src={editImage} alt={`Редактировать`}/></Button>
                                <Button type={`actionImage`}><Image src={deleteImage} alt={`Удалить`}/></Button>
                            </td>
                        </tr>
                    )
                })}
            </tbody>
        </table>
    );
}
