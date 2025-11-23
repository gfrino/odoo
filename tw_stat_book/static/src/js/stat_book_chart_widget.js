/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useEffect, useRef, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

// Import Chart.js (assicurati che sia disponibile in Odoo)
const { Chart } = window;

/**
 * Widget per visualizzare grafici statistici a linee
 */
export class StatBookChartWidget extends Component {
    setup() {
        this.orm = useService("orm");
        this.canvasRef = useRef("chartCanvas");
        this.state = useState({
            viewType: "monthly",
            chartData: [],
            loading: true,
        });
        this.chart = null;

        useEffect(
            () => {
                this.loadChartData();
            },
            () => [this.props.record.resId, this.state.viewType]
        );
    }

    async loadChartData() {
        if (!this.props.record.resId) return;

        this.state.loading = true;
        
        try {
            const departmentId = this.props.record.resId;
            const department = await this.orm.read(
                "stat.book.department",
                [departmentId],
                ["forecast_min_3months", "forecast_max_3months"]
            );

            const chartData = await this.orm.call(
                "stat.book.data",
                "get_chart_data",
                [departmentId, this.state.viewType]
            );

            this.state.chartData = chartData;
            this.renderChart(chartData, department[0]);
        } catch (error) {
            console.error("Errore nel caricamento dei dati del grafico:", error);
        } finally {
            this.state.loading = false;
        }
    }

    renderChart(data, department) {
        if (!this.canvasRef.el) return;

        const ctx = this.canvasRef.el.getContext("2d");

        // Distruggi il grafico esistente se presente
        if (this.chart) {
            this.chart.destroy();
        }

        const labels = data.map(d => d.period);
        const values = data.map(d => d.value);

        const minForecast = department.forecast_min_3months;
        const maxForecast = department.forecast_max_3months;

        this.chart = new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Valori Effettivi",
                        data: values,
                        borderColor: "rgb(75, 192, 192)",
                        backgroundColor: "rgba(75, 192, 192, 0.2)",
                        tension: 0.1,
                        fill: true,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        min: minForecast,
                        max: maxForecast,
                        title: {
                            display: true,
                            text: "Valore",
                        },
                    },
                    x: {
                        title: {
                            display: true,
                            text: "Periodo",
                        },
                    },
                },
                plugins: {
                    legend: {
                        display: true,
                        position: "top",
                    },
                    title: {
                        display: true,
                        text: `Grafico ${this.getViewTypeLabel()}`,
                    },
                },
            },
        });
    }

    getViewTypeLabel() {
        const labels = {
            weekly: "Settimanale",
            monthly: "Mensile",
            yearly: "Annuale",
        };
        return labels[this.state.viewType] || "Mensile";
    }

    onViewTypeChange(viewType) {
        this.state.viewType = viewType;
    }
}

StatBookChartWidget.template = "tw_stat_book.StatBookChartWidget";
StatBookChartWidget.props = {
    record: Object,
};

registry.category("fields").add("stat_book_chart", StatBookChartWidget);
