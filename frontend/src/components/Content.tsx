import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Progress } from "@/components/ui/progress";
import React, { useState, useTransition } from "react";
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts";
import { motion } from "framer-motion";
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import { Button } from "./ui/button";
import { sendData } from "@/utils/store";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"; // pastikan ini sudah ada ya
import { Loader2 } from "lucide-react"; // import icon spinner

const chartData = [
  { month: "Jan", national: 4000, international: 2400 },
  { month: "Feb", national: 3000, international: 1398 },
  { month: "Mar", national: 2000, international: 9800 },
  { month: "Apr", national: 2780, international: 3908 },
  { month: "May", national: 1890, international: 4800 },
  { month: "Jun", national: 2390, international: 3800 },
  { month: "Jul", national: 2390, international: 3800 },
  { month: "Aug", national: 2390, international: 3800 },
  { month: "Sep", national: 2390, international: 3800 },
  { month: "Nov", national: 2390, international: 3800 },
  { month: "Dec", national: 2390, international: 3800 },
];

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

const chartConfig = {
  views: {
    label: "Page Views",
  },
  national: {
    label: "National",
    color: "#4ADE80",
  },
  international: {
    label: "International",
    color: "#60A5FA",
  },
} satisfies ChartConfig;

export default function Content() {
  const [activeChart, setActiveChart] =
    React.useState<keyof typeof chartConfig>("national");
  // const [isPending, startTransition] = useTransition();
  const [forecastData, setForecastData] = useState<any[]>([]);
  const [isPending, setIsPending] = useState(false);

  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  const total = React.useMemo(
    () => ({
      national: chartData.reduce((acc, curr) => acc + curr.national, 0),
      international: chartData.reduce(
        (acc, curr) => acc + curr.international,
        0
      ),
    }),
    []
  );

  const formatNumber = (num: number) => {
    if (num >= 1_000_000) {
      return `${(num / 1_000_000).toFixed(2)} M`;
    } else if (num >= 1_000) {
      return `${(num / 1_000).toFixed(2)} rb`; // opsional kalau mau ada "rb"
    } else {
      return num.toLocaleString(); // angka kecil biasa
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsPending(true); // Mulai loading

    const formData = new FormData(e.currentTarget);
    const generation = formData.get("generation")?.toString() || "";
    const kromosom = formData.get("kromosom")?.toString() || "";
    const probability = formData.get("probability")?.toString() || "";

    try {
      const backendUrl = import.meta.env.VITE_BACKEND_URL;
      if (!backendUrl) {
        throw new Error("Backend URL is not defined in environment variables.");
      }

      const data = {
        population_size: generation,
        generations: kromosom,
        mutation_prob: probability,
        dataset: [],
      };

      const response = await fetch(`${backendUrl}api/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData);
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const responseData = await response.json();
      const months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
      ];

      const forecast = responseData;
      setResult(forecast);

      const chartData = responseData.forecast.map(
        (value: number, index: number) => ({
          month: months[index],
          national: value,
          international: 0,
        })
      );

      setForecastData(chartData);
    } catch (error) {
      console.error("Error sending data:", error);
      throw error;
    } finally {
      setIsPending(false); // Selesai loading
    }
  };

  return (
    <div className="container mx-auto mt-6 flex flex-col gap-6">
      <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart (Nomor 3) */}
        <Card>
          <CardHeader className="flex flex-col items-stretch space-y-0 border-b p-0 sm:flex-row">
            <div className="flex flex-1 flex-col justify-center gap-1 px-6 py-5 sm:py-6 xl:text-center">
              <CardTitle>Passager prediction at Soekarno-Hatta</CardTitle>
              <CardDescription className="text-sm text-muted-foreground sm:hidden ">
                Showing total visitors for the next 12 months at 2023
              </CardDescription>
            </div>

            <div className="flex">
              {["national", "international"].map((key) => {
                const chart = key as keyof typeof chartConfig;
                return (
                  <button
                    key={chart}
                    data-active={activeChart === chart}
                    className="relative z-30 flex flex-1 flex-col justify-center gap-1 border-t px-6 py-4 text-left even:border-l data-[active=true]:bg-muted/50 sm:border-l sm:border-t-0 sm:px-8 sm:py-6"
                    onClick={() => setActiveChart(chart)}
                  >
                    <span className="text-xs text-muted-foreground">
                      {chartConfig[chart].label}
                    </span>
                    <span className="text-lg font-bold leading-none sm:text-3xl">
                      {formatNumber(
                        forecastData.reduce((acc, curr) => acc + curr[key], 0)
                      )}
                    </span>
                  </button>
                );
              })}
            </div>
          </CardHeader>
          <CardContent className="px-2 sm:p-6">
            <ChartContainer
              config={{
                views: forecastData.map((data) => ({
                  label: data.month,
                  value: data.national,
                })),
              }}
              className="aspect-auto h-[250px] w-full"
            >
              <BarChart
                accessibilityLayer
                data={forecastData.map((data) => ({
                  month: data.month,
                  national: data.national,
                  international: data.international,
                }))}
                margin={{
                  left: 12,
                  right: 12,
                }}
              >
                <CartesianGrid vertical={false} />
                <XAxis
                  dataKey="month"
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  minTickGap={32}
                  tickFormatter={(value) => value}
                />
                <ChartTooltip
                  content={
                    <ChartTooltipContent
                      className="w-[150px]"
                      nameKey="views"
                      labelFormatter={(value) => value}
                    />
                  }
                />
                <Bar
                  dataKey={activeChart}
                  fill={chartConfig[activeChart].color}
                />
              </BarChart>
            </ChartContainer>
          </CardContent>
        </Card>

        {/* Card Prediction (Nomor 4) */}
        <div className="flex flex-col gap-6">
          <form onSubmit={handleSubmit}>
            <Card>
              <CardHeader>
                <CardTitle>Genetic Algorithm</CardTitle>
              </CardHeader>
              <CardContent className="flex flex-col gap-4">
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="generation">Generation</Label>
                  <Input
                    id="generation"
                    name="generation"
                    placeholder="Enter your iteration"
                    type="generation"
                    required
                    disabled={isPending}
                  />
                </div>
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="kromosom">Kromosom</Label>
                  <Input
                    id="kromosom"
                    name="kromosom"
                    placeholder="Enter your kromosom"
                    type="kromosom"
                    required
                    disabled={isPending}
                  />
                </div>
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="probability">Probability</Label>
                  <Input
                    id="probability"
                    name="probability"
                    placeholder="Enter your probability"
                    type="probability"
                    required
                    disabled={isPending}
                  />
                </div>
                <Button className="w-full" type="submit" disabled={isPending}>
                  {isPending ? (
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  ) : (
                    "Submit"
                  )}
                </Button>
              </CardContent>
            </Card>
          </form>

          {/* Text Area Diagnosis Info (Nomor 8) */}
          <Card>
            <CardHeader>
              <CardTitle>Model Performance</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between">
                  <Label>MAPE (Error):</Label>
                  <span className="font-bold text-primary">
                    {result?.mape?.toFixed(2)}%
                  </span>
                </div>
                <div className="flex justify-between">
                  <Label>Best Alpha:</Label>
                  <span className="font-bold text-primary">
                    {result?.best_alpha?.toFixed(4)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <Label>Best Beta:</Label>
                  <span className="font-bold text-primary">
                    {result?.best_beta?.toFixed(4)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <Label>Best Gamma:</Label>
                  <span className="font-bold text-primary">
                    {result?.best_gamma?.toFixed(4)}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Card Prediction (Nomor 5) */}
      <div className="flex flex-col p-6 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Forecast Results</CardTitle>
          </CardHeader>
          <CardContent className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>No</TableHead>
                  <TableHead>Bulan</TableHead>
                  <TableHead>Hasil Prediksi</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {forecastData.map((data, index) => (
                  <TableRow key={index}>
                    <TableCell>{index + 1}</TableCell>
                    <TableCell>{data.month}</TableCell>
                    <TableCell>{data.national.toLocaleString()}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
