export type TypeFormInput = 'text' | 'password' | `email` | `number` | `date` | `suggestSelect` | `suggestDatalist`;

export interface OptionsFormInput {
    id: string;
    value: string | number;
    onChange: (value: any) => void;
    placeholder?: string;
    autoComplete?: string;
    required?: boolean;
    min?: string;
    optionsSuggest?: {
        value: string;
        children: string;
    }[],
    optionsDatalist?: Token[],

}

export interface Field {
    label: string; // Метка поля
    type: TypeFormInput; // Тип поля
    options: OptionsFormInput; // Опции для поля
}


export interface Token {
    id: number;
    name: string;
    symbol: string;
    cg_id: string;
}

export interface Transaction {
    operation: 'BUY' | 'SELL';
    quantity: number;
    price: number;
    timestamp: string;
    token: Token;
    id: number;
}

export interface CryptosPortfolio {
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

export interface DataPoint {
    date: string; // Дата в формате строки
    value: number; // Значение
}
