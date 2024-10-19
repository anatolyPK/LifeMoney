export const formatTimestamp = (ts: string) => {
    const date = new Date(+ts * 1000); // Умножаем на 1000, чтобы получить миллисекунды
    return date.toISOString().split('T')[0]; // Получаем строку в формате YYYY-MM-DD
};