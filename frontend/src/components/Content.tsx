import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
// import { Textarea } from "@/components/ui/textarea";
// import { Progress } from "@/components/ui/progress";
import React, { useState } from "react";
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts";
// import { motion } from "framer-motion";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import { Button } from "./ui/button";
// import { sendData } from "@/utils/store";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"; // pastikan ini sudah ada ya
import { Loader2 } from "lucide-react"; // import icon spinner

// const chartData = [
//   { month: "Jan", national: 4000, international: 2400 },
//   { month: "Feb", national: 3000, international: 1398 },
//   { month: "Mar", national: 2000, international: 9800 },
//   { month: "Apr", national: 2780, international: 3908 },
//   { month: "May", national: 1890, international: 4800 },
//   { month: "Jun", national: 2390, international: 3800 },
//   { month: "Jul", national: 2390, international: 3800 },
//   { month: "Aug", national: 2390, international: 3800 },
//   { month: "Sep", national: 2390, international: 3800 },
//   { month: "Nov", national: 2390, international: 3800 },
//   { month: "Dec", national: 2390, international: 3800 },
// ];

// const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

const chartConfig = {
  national: {
    label: "National",
    color: "#00C49F", // Color for the 'national' chart
  },
  international: {
    label: "International",
    color: "#0088FE", // Color for the 'international' chart
  },
};
type ForecastData = {
  month: string;
  national: number;
  international: number;
};

export default function Content() {
  const [activeChart, setActiveChart] =
    React.useState<keyof typeof chartConfig>("national");
  // const [isPending, startTransition] = useTransition();
  const [forecastData, setForecastData] = useState<ForecastData[]>([]);
  const [isPending, setIsPending] = useState(false);

  const [result, setResult] = useState<{
    mape?: number;
    best_alpha?: number;
    best_beta?: number;
    best_gamma?: number;
  } | null>(null);

  // const total = React.useMemo(
  //   () => ({
  //     national: chartData.reduce((acc, curr) => acc + curr.national, 0),
  //     international: chartData.reduce(
  //       (acc, curr) => acc + curr.international,
  //       0
  //     ),
  //   }),
  //   []
  // );

  const formatNumber = (num: number) => {
    if (num >= 1_000_000) {
      return `${(num / 1_000_000).toFixed(2)} M`;
    } else if (num >= 1_000) {
      return `${(num / 1_000).toFixed(2)} rb`; // opsional kalau mau ada "rb"
    } else {
      return num.toLocaleString(); // angka kecil biasa
    }
  };

  // const config = {
  //   // Menggunakan forecastData untuk membangun data chart
  //   views: forecastData.reduce((acc, data) => {
  //     // Menambahkan objek untuk setiap bulan yang ada di forecastData
  //     acc[data.month] = {
  //       label: data.month, // Label untuk setiap bulan
  //       color: getColorForMonth(data.month), // Menggunakan fungsi untuk menentukan warna berdasarkan bulan
  //     };
  //     return acc;
  //   }, {}),
  // };

  // // Fungsi untuk menentukan warna berdasarkan bulan
  // const getColorForMonth = (month) => {
  //   switch (month) {
  //     case "Jan":
  //       return "#FF5733"; // Contoh warna untuk Januari
  //     case "Feb":
  //       return "#33FF57"; // Contoh warna untuk Februari
  //     case "Mar":
  //       return "#3357FF"; // Contoh warna untuk Maret
  //     case "Apr":
  //       return "#57FF33"; // Contoh warna untuk April
  //     case "May":
  //       return "#33A1FF"; // Contoh warna untuk Mei
  //     case "Jun":
  //       return "#A133FF"; // Contoh warna untuk Juni
  //     default:
  //       return "#CCCCCC"; // Default color jika bulan tidak ditemukan
  //   }
  // };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsPending(true); // Mulai loading

    const formData = new FormData(e.currentTarget);
    const generation = formData.get("generation")?.toString() || "";
    const kromosom = formData.get("kromosom")?.toString() || "";
    const probability = formData.get("probability")?.toString() || "";

    try {
      const backendUrl = "http://127.0.0.1:8000/";
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
          international: 0, // You can adjust this as needed
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
                        forecastData.reduce((acc, curr) => acc + curr[chart], 0)
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
                Jan: {
                  label: "January",
                  color: "#FF5733", // Contoh warna untuk Januari
                },
                Feb: {
                  label: "February",
                  color: "#33FF57", // Contoh warna untuk Februari
                },
                Mar: {
                  label: "March",
                  color: "#3357FF", // Contoh warna untuk Maret
                },
                Apr: {
                  label: "April",
                  color: "#57FF33", // Contoh warna untuk April
                },
                May: {
                  label: "May",
                  color: "#33A1FF", // Contoh warna untuk Mei
                },
                Jun: {
                  label: "June",
                  color: "#A133FF", // Contoh warna untuk Juni
                },
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
                    {typeof result?.mape === "number"
                      ? result.mape.toFixed(2)
                      : "0"}
                    %
                  </span>
                </div>
                <div className="flex justify-between">
                  <Label>Best Alpha:</Label>
                  <span className="font-bold text-primary">
                    {typeof result?.best_alpha === "number"
                      ? result.best_alpha.toFixed(4)
                      : "0"}
                  </span>
                </div>
                <div className="flex justify-between">
                  <Label>Best Beta:</Label>
                  <span className="font-bold text-primary">
                    {typeof result?.best_beta === "number"
                      ? result.best_beta.toFixed(4)
                      : "0"}
                  </span>
                </div>
                <div className="flex justify-between">
                  <Label>Best Gamma:</Label>
                  <span className="font-bold text-primary">
                    {typeof result?.best_gamma === "number"
                      ? result.best_gamma.toFixed(4)
                      : "0"}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Card Prediction (Nomor 5) */}
      <div className="flex flex-col p-6 gap-6">
        {/* Card Prediction (Nomor 5) */}
        <Card>
          <CardHeader className="flex flex-col items-start border-b p-0 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex flex-col px-6 py-5 sm:py-6">
              <CardTitle className="text-xl font-semibold white:text-gray-800 black:text-white">
                Forecast Results
              </CardTitle>
              <CardDescription className="text-sm text-muted-foreground">
                Passenger prediction for the next 12 months in 2023
              </CardDescription>
            </div>
          </CardHeader>

          <CardContent className="overflow-x-auto px-2 sm:px-6 sm:pb-6">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="text-center w-12">No</TableHead>
                  <TableHead className="text-center">Bulan</TableHead>
                  <TableHead className="text-center">Hasil Prediksi</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {forecastData.map((data, index) => (
                  <TableRow
                    key={index}
                    className={index % 2 === 0 ? "bg-muted/20" : ""}
                  >
                    <TableCell className="text-center font-medium text-muted-foreground">
                      {index + 1}
                    </TableCell>
                    <TableCell className="text-center font-medium text-gray-700">
                      {data.month}
                    </TableCell>
                    <TableCell className="text-center font-semibold text-gray-900">
                      {data.national.toLocaleString("id-ID")}
                    </TableCell>
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
