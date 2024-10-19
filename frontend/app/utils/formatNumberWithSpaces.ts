export function formatNumberWithSpaces(num: number, toFixed: number): string {
    return num.toFixed(toFixed).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}