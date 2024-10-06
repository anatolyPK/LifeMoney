import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
} from 'recharts';
import React from "react";

interface DataPoint {
    date: string; // Дата в формате строки
    value: number; // Значение
}

interface MyComponentProps {
    dataChart: DataPoint[];
}
const MyChart: React.FC<MyComponentProps> = ({ dataChart }) => {
    return (
        <ResponsiveContainer width="100%" height={300}>
            <LineChart data={dataChart}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="value" stroke="#8884d8" />
            </LineChart>
        </ResponsiveContainer>
    );
};

export default MyChart;
