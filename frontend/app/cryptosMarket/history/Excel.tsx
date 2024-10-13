import React from "react";
import {formatTimestamp} from "@/app/lib/formatTimestamp";
import editImage from "@/public/editImage.svg";
import deleteImage from "@/public/deleteImage.svg";
import Image from "next/image";
import Button from "@/app/ui/Button";
import {Transaction} from "@/app/types";

interface ExcelProps {
    headers: string[];
    data: Transaction[];
    handleActionButton: (id: number) => void;
}

export default  function Excel({ headers, data, handleActionButton }: ExcelProps) {

    return (
        <div>
            <table className = {`m-2 p-2`}>
                <thead>
                    <tr>{headers.map((title, idx) => {
                        return (
                            <th key = {idx}
                                className = {`m-2 p-2 font-bold border-2  border-solid border-blue-400`}>{title}</th>
                        )
                    })}</tr>
                </thead>
                <tbody>
                    {data.map((transaction) => {
                        return (
                            <tr key = {transaction.id}>
                                <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{transaction.id} </td>
                                <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{transaction.operation}</td>
                                <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{transaction.quantity}</td>
                                <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{transaction.price}</td>
                                <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{formatTimestamp(transaction.timestamp)}</td>
                                <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{transaction.token.name} ({transaction.token.symbol})</td>
                                <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>
                                    <Button type = {`actionImage`} onClick = {() => handleActionButton(transaction.id)}><Image
                                        src = {editImage} alt = {`Редактировать`} /></Button>
                                    <Button type = {`actionImage`} onClick = {() => alert(`Удалить`)}><Image
                                        src = {deleteImage} alt = {`Удалить`} /></Button>
                                </td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        </div>
    );
}
