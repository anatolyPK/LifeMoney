const url = `http://localhost:8000/api/v1`;

export const AuthAPI = {
    // отправка данных для авторизации
    async register(username: string, email: string, password: string) {
        const res = await fetch(`${url}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({username, email, password}),
        })
        if (!res.ok) {
            // Если ответ не успешен, выбрасываем ошибку с сообщением
            const errorData = await res.json();
            throw new Error(errorData.message || 'Ошибка при регистрации');
        }

        return res; // Возвращаем данные, если ответ успешен
    },
    // отправка данных для авторизации
    async login(username: string, password: string) {
        const res = await fetch(`${url}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({username, password}).toString(),
        })
        if (!res.ok) {
            // Если ответ не успешен, выбрасываем ошибку с сообщением
            const errorData = await res.json();
            throw new Error(errorData.message || 'Ошибка при авторизации');
        }

        return res.json(); // Возвращаем данные, если ответ успешен
    },
}

export const UserAPI = {
    // запрос данных о пользователе
    async me(token: string) {
        const res = await fetch(`${url}/users/me`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!res.ok) {
            // Если ответ не успешен, выбрасываем ошибку с сообщением
            const errorData = await res.json();
            throw new Error(errorData.message || 'Ошибка при запросе данных пользователя');
        }
        return res.json();
    },
}

export const CMApi = {
    // поиск токенов в выпадающем списке
    async search(token: string, tokenSymbol: string) {
        const res = await fetch(`${url}/cryptos/token/search?token_symbol=${tokenSymbol}`, {
            method: 'GET',
            headers: {
                'accept': 'application/json',
                'Authorization': `Bearer ${token}`,
            }
        });
        if (!res.ok) {
            // Если ответ не успешен, выбрасываем ошибку с сообщением
            const errorData = await res.json();
            throw new Error(errorData.message || 'Ошибка при поиске токенов');
        }
        return res.json();
    },

    // запрос на баланс токена из поиска
    async balance(token: string, tokenId: number) {
        const res = await fetch(`${url}/cryptos/token/balance?token_id=${tokenId}`, {
            method: 'GET',
            headers: {
                'accept': 'application/json',
                'Authorization': `Bearer ${token}`,
            }
        });
        if (!res.ok) {
            // Если ответ не успешен, выбрасываем ошибку с сообщением
            const errorData = await res.json();
            throw new Error(errorData.message || 'Ошибка при запросе баланса токена');
        }
        return res.json();
    },

    // отправка транзакции
    async transactions(token: string, body: object) {
        const res = await fetch(`${url}/cryptos/transactions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': `Bearer ${token}`,

            },
            body: JSON.stringify(body)
        });
        if (!res.ok) {
            // Если ответ не успешен, выбрасываем ошибку с сообщением
            const errorData = await res.json();
            throw new Error(errorData.message || 'Ошибка при отправке транзакции');
        }
        return res.json();
    },

    // внесение изменений в транзакцию
    async transactionsEdit(token: string, body: object, id: number) {
        const res = await fetch(`${url}/cryptos/transactions/${id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': `Bearer ${token}`,

            },
            body: JSON.stringify(body)
        });
        if (!res.ok) {
            // Если ответ не успешен, выбрасываем ошибку с сообщением
            const errorData = await res.json();
            throw new Error(errorData.message || 'Ошибка при изменении транзакции');
        }
        return res.json();
    },

    //получение истории транзакций
    async getTransactions(token: string) {
        const res = await fetch(`${url}/cryptos/transactions`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,

            },
        });
        if (!res.ok) {
            // Если ответ не успешен, выбрасываем ошибку с сообщением
            const errorData = await res.json();
            throw new Error(errorData.message || 'Ошибка при получении истории транзакций');
        }
        return res.json();
    },

    //получение крипто портфеля
    async getCryptos(token: string) {
        const res = await fetch(`${url}/cryptos`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,

            },
        });
        if (!res.ok) {
            // Если ответ не успешен, выбрасываем ошибку с сообщением
            const errorData = await res.json();
            throw new Error(errorData.message || 'Ошибка при запросе крипто портфеля');
        }
        return res.json();
    },

    //получение данных для граифика крипто портфеля
    async getDataGraph(token: string, timePeriod: string) {
        const res = await fetch(`${url}/cryptos/graph?time_period=${timePeriod}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,

            },
        });
        if (!res.ok) {
            // Если ответ не успешен, выбрасываем ошибку с сообщением
            const errorData = await res.json();
            throw new Error(errorData.message || 'Ошибка при запросе данных для графика');
        }
        return res.json();
    },


};
