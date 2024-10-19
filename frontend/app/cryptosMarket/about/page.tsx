'use client'

import React, {useEffect, useState} from "react";
import Chart from "@/app/cryptosMarket/about/Chart";
import {CMApi} from "@/app/api/api";
import SuggestSelect from "@/app/ui/SuggestSelect";
import {useAuth} from "@/app/context/AuthContext";
import {CryptosPortfolio, DataPoint} from "@/app/types";
import {formatNumberWithSpaces} from "@/app/utils/formatNumberWithSpaces";


const fetchCryptos = async (accessToken: string, setErrorData: any) => {
    try {
        return await CMApi.getCryptos(accessToken!);
    } catch (err) {
        if (err instanceof Error) {
            setErrorData(err.message);
        } else {
            setErrorData('Неизвестная ошибка при запросе крипто портфеля');
        }
    }
}

const fetchCryptoChart = async (accessToken: string, timePeriod: string, setErrorDataChart: any) => {
    try {
        return await CMApi.getDataGraph(accessToken!, timePeriod);

    } catch (err) {
        if (err instanceof Error) {
            setErrorDataChart(err.message);
        } else {
            setErrorDataChart('Неизвестная ошибка (запрос графика)');
        }
    }
}




export default function Page() {
    const [data, setData] = useState<CryptosPortfolio | null>(null);
    const [dataChart, setDataChart] = useState<DataPoint[]>([]);
    const [timePeriod, setTimePeriod] = useState<string>(`daily`);
    const [errorData, setErrorData] = useState<string | null>(null);
    const [errorDataChart, setErrorDataChart] = useState<string | null>(null);
    const {accessToken} = useAuth();

    const headers = [`Название (тикер)`, `Количество`, `Средняя цена покупки`, `Текущая цена покупки`, `Прибыль`, `Баланс`, `Процент от портфеля`];

    useEffect(() => {
        fetchCryptos(accessToken!, setErrorData).then(cryptos => setData(cryptos));
    }, [accessToken]);

    useEffect(() => {
        fetchCryptoChart(accessToken!, timePeriod, setErrorDataChart).then((cryptoChart) => {
            const data = JSON.parse(cryptoChart.graph_data);
            // Преобразование в нужный формат
            const result: DataPoint[] = Object.entries(data).map(([timestamp, value]) => {
                const date = new Date(Number(timestamp) * 1000); // Преобразование временной метки в миллисекунды
                return {
                    date: date.toISOString().split('T')[0], // Форматирование даты в 'YYYY-MM-DD'
                    value: value as number
                };
            });
            setDataChart(result);
        });

    }, [accessToken, timePeriod]);


    if (data === null) {
        return <div>Loading...</div>
    }
    return (
        <div>
              <div className = {`flex-auto px-12 h-[600px] text-center `}>
                  <div>Общая информация</div>
                  <div>{errorData && <p>ErrorData: {errorData}</p>}</div>
                  <div>{errorDataChart && <p>ErrorDataChart: {errorDataChart}</p>}</div>

                  <div className = {`grid grid-rows-2 gap-y-2 my-5`}>
                      <div
                          className = {`grid grid-cols-3 gap-x-4 justify-center items-center border border-stone-100 border-b-stone-600`}
                      >
                          <div className = {``}>
                              Баланс: {formatNumberWithSpaces(data.main_info.total_value, 2)} ₽
                          </div>

                          <div className = {``}>
                              Вложено: {formatNumberWithSpaces(data.main_info.total_investment, 2)} ₽
                          </div>

                          <div className = {``}>
                                  Прибыль: {formatNumberWithSpaces(data.main_info.total_profit_in_currency, 2)} ₽ ({formatNumberWithSpaces(data.main_info.total_profit_in_percent, 2)}) %
                          </div>
                      </div>
                  </div>

                  <div>
                    <h1>График значений</h1>
                    <Chart dataChart = {dataChart} />
                       <label htmlFor = "timePeriodSelect"
                              className = "block text-sm font-medium leading-6 text-gray-900">
                            Период отображения графика
                        </label>
                      <SuggestSelect type = {`suggestSelect`} options = {{
                          id: `timePeriodSelect`,
                          value: timePeriod,
                          onChange: setTimePeriod,
                          optionsSuggest: [
                              {
                                  value: `daily`,
                                  children: `День`,
                              },
                              {
                                  value: `weekly`,
                                  children: `Неделя`,
                              },
                              {
                                  value: `monthly`,
                                  children: `Месяц`,
                              },
                              {
                                  value: `yearly`,
                                  children: `Год`,
                              },
                          ]
                      }} />
                  </div>
              </div>
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
                    {data.assets.map((asset, idx) => {
                        return (
                            <tr key = {idx}>

                                <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{asset.asset.name} ({asset.asset.symbol})</td>
                                <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{formatNumberWithSpaces(asset.quantity,0)}</td>
                                <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{formatNumberWithSpaces(asset.average_price_buy,2)}</td>
                                <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{formatNumberWithSpaces(asset.current_price,2)}</td>
                                <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{formatNumberWithSpaces(asset.profit_in_currency, 2)} ({formatNumberWithSpaces(asset.profit_in_percent,2)} %)</td>
                                <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{formatNumberWithSpaces(asset.balance, 2)}</td>
                                <td className = {`m-2 p-2 border-2  border-solid border-blue-400 text-center`}>{formatNumberWithSpaces(asset.percent_of_portfolio, 2)}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
            </div>
        </div>

    );
}
