import { useEffect, useRef } from "react";
import { createChart, ColorType, IChartApi, ISeriesApi, CandlestickData, LineData, Time } from "lightweight-charts";

interface ChartProps {
  data: Array<{
    timestamp: string;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
  }>;
  type?: "candlestick" | "line";
  height?: number;
  showVolume?: boolean;
}

export function TradingChart({ data, type = "candlestick", height = 400, showVolume = false }: ChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<"Candlestick"> | ISeriesApi<"Line"> | null>(null);
  const volumeSeriesRef = useRef<ISeriesApi<"Histogram"> | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const chart = createChart(containerRef.current, {
      width: containerRef.current.clientWidth,
      height: height,
      layout: {
        background: { type: ColorType.Solid, color: "transparent" },
        textColor: "#64748b",
        fontFamily: "Inter, system-ui, sans-serif",
      },
      grid: {
        vertLines: { color: "#e2e8f0" },
        horzLines: { color: "#e2e8f0" },
      },
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
      },
      rightPriceScale: {
        borderColor: "#e2e8f0",
      },
    });

    chartRef.current = chart;

    if (type === "candlestick") {
      const candleSeries = chart.addCandlestickSeries({
        upColor: "#22c55e",
        downColor: "#ef4444",
        borderUpColor: "#22c55e",
        borderDownColor: "#ef4444",
        wickUpColor: "#22c55e",
        wickDownColor: "#ef4444",
      });
      seriesRef.current = candleSeries;

      const candleData: CandlestickData[] = data.map((d) => ({
        time: (new Date(d.timestamp).getTime() / 1000) as Time,
        open: d.open,
        high: d.high,
        low: d.low,
        close: d.close,
      }));
      candleSeries.setData(candleData);
    } else {
      const lineSeries = chart.addLineSeries({
        color: "#22c55e",
        lineWidth: 2,
      });
      seriesRef.current = lineSeries;

      const lineData: LineData[] = data.map((d) => ({
        time: (new Date(d.timestamp).getTime() / 1000) as Time,
        value: d.close,
      }));
      lineSeries.setData(lineData);
    }

    if (showVolume && data.length > 0) {
      const volumeSeries = chart.addHistogramSeries({
        color: "#94a3b8",
        priceFormat: { type: "volume" },
        priceScaleId: "",
      });
      volumeSeries.priceScale().applyOptions({
        scaleMargins: { top: 0.8, bottom: 0 },
      });
      volumeSeriesRef.current = volumeSeries;
      volumeSeries.setData(
        data.map((d) => ({
          time: (new Date(d.timestamp).getTime() / 1000) as Time,
          value: d.volume,
          color: d.close >= d.open ? "#22c55e80" : "#ef444480",
        }))
      );
    }

    chart.timeScale().fitContent();

    const handleResize = () => {
      if (containerRef.current && chartRef.current) {
        chartRef.current.applyOptions({ width: containerRef.current.clientWidth });
      }
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      chart.remove();
      chartRef.current = null;
      seriesRef.current = null;
      volumeSeriesRef.current = null;
    };
  }, [data, type, height, showVolume]);

  return <div ref={containerRef} className="w-full" style={{ height }} />;
}