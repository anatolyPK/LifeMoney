'use client'

import React, {useEffect, useState} from "react";
import Chart from "@/app/cryptosMarket/about/Chart";
import {CMApi} from "@/app/api/api";
import SuggestSelect from "@/app/ui/SuggestSelect";
import {useAuth} from "@/app/context/AuthContext";


interface CryptosPortfolio {
    main_info: {
        total_value: number,
        total_investment: number,
        total_profit_in_currency: number,
        total_profit_in_percent: number
    },
    assets:
        {
            asset: {
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

interface DataPoint {
    date: string; // Дата в формате строки
    value: number; // Значение
}

export type TimePeriod = `daily` | `weekly` | `monthly` | `yearly`;

export default function Page() {
    const [data, setData] = useState<CryptosPortfolio | null>(null);
    const [dataChart, setDataChart] = useState<DataPoint[]>([]);
    const [timePeriod, setTimePeriod] = useState<TimePeriod>(`daily`);
    const [errorData, setErrorData] = useState<string | null>(null);
    const [errorDataChart, setErrorDataChart] = useState<string | null>(null);
    const {accessToken} = useAuth();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const result: CryptosPortfolio = await CMApi.getCryptos(accessToken!);
                setData(result);
            } catch (err) {
                if (err instanceof Error) {
                    setErrorData(err.message);
                } else {
                    setErrorData('Неизвестная ошибка при запросе крипто портфеля');
                }
            }
        }
        fetchData();

    }, [accessToken]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const jsonResponse = await CMApi.getDataGraph(accessToken!, timePeriod);
                const dataString = jsonResponse.ok;
                const data = JSON.parse(dataString);
                // Преобразование в нужный формат
                const result: DataPoint[] = Object.entries(data).map(([timestamp, value]) => {
                    const date = new Date(Number(timestamp) * 1000); // Преобразование временной метки в миллисекунды
                    return {
                        date: date.toISOString().split('T')[0], // Форматирование даты в 'YYYY-MM-DD'
                        value: value as number
                    };
                });
                setDataChart(result);
            } catch (err) {
                if (err instanceof Error) {
                    setErrorDataChart(err.message);
                } else {
                    setErrorDataChart('Неизвестная ошибка (запрос графика)');
                }
            }
        }
        fetchData();

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
                      className = {`grid grid-cols-2 gap-x-4 justify-center items-center border border-stone-100 border-b-stone-600`}
                  >
                    <div className = {``}>
                      <div>Баланс: {data.main_info.total_value} ₽</div>
                      <div>
                        Прибыль:{" "}
                          <span className = {``}>
                          {data.main_info.total_profit_in_currency} ₽ {data.main_info.total_profit_in_percent} %
                        </span>
                      </div>
                    </div>
                    <div className = {``}>
                      <div>Баланс {`XXX`} $</div>
                      <div>
                        Прибыль:{" "}
                          <span className = {``}>
                          {`+ XXX`} $ {`+ XXX`} %
                        </span>
                      </div>
                    </div>
                  </div>

                  <div
                      className = {`grid grid-cols-2 gap-x-4 justify-center items-center border border-stone-100 border-b-stone-600`}
                  >
                    <div>
                      <div>Вложено: {data.main_info.total_investment} ₽</div>
                      <div>
                        <span className = {``}>
                          {`+ XXX`} ₽ {`+ XXX`} %
                        </span>
                      </div>
                    </div>
                    <div>
                      <div>Вложено {`XXX`} $</div>
                      <div>
                        <span className = {``}>
                          {`+ XXX`} $ {`+ XXX`} %
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
                  <div>
                    <h1>График значений</h1>
                    <Chart dataChart = {dataChart} />
                       <label htmlFor = "timePeriodSelect" className = "block text-sm font-medium leading-6 text-gray-900">
                            Период отображения графика
                        </label>
                      <SuggestSelect value = {timePeriod} onChange = {setTimePeriod} />
                  </div>
              </div>
        </div>

    );
}
