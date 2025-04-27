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
import React, { useTransition } from "react";
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts";
import { motion } from "framer-motion";
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";

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
    color: "#00C49F",
  },
  international: {
    label: "International",
    color: "#0088FE",
  },
} satisfies ChartConfig;

export default function Content() {
  const [activeChart, setActiveChart] =
    React.useState<keyof typeof chartConfig>("national");
  const [isPending, startTransition] = useTransition();

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
                      {total[key as keyof typeof total].toLocaleString()}
                    </span>
                  </button>
                );
              })}
            </div>
          </CardHeader>
          <CardContent className="px-2 sm:p-6">
            <ChartContainer
              config={chartConfig}
              className="aspect-auto h-[250px] w-full"
            >
              <BarChart
                accessibilityLayer
                data={chartData}
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
                  fill={`var(--color-${activeChart})`}
                />
              </BarChart>
            </ChartContainer>
          </CardContent>
        </Card>

        {/* Card Prediction (Nomor 4) */}
        <div className="flex flex-col gap-6">
          <form action={""}>
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
              </CardContent>
            </Card>
          </form>

          {/* Text Area Diagnosis Info (Nomor 8) */}
          <Card>
            <CardHeader>
              <CardTitle>Diagnosis: Glaucoma</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <Label>What is it?</Label>
                <Textarea
                  className="resize-none"
                  rows={4}
                  value="Glaucoma is a group of eye conditions that damage the optic nerve, which connects the eye to the brain..."
                  readOnly
                />
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Card Prediction (Nomor 5) */}
      <div className="flex flex-col p-6 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Diagnosis: Glaucoma</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <Label>What is it?</Label>
              <Textarea
                className="resize-none"
                rows={4}
                value="Glaucoma is a group of eye conditions that damage the optic nerve, which connects the eye to the brain..."
                readOnly
              />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
