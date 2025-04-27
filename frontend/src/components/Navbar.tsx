import { cn } from "@/lib/utils";
import { Button } from "./ui/button";

import { Link } from "react-router-dom";
import { Separator } from "@/components/ui/separator";
import { DarkModeToggle } from "./DarkModeToggle";

export default function Navbar() {
  return (
    <nav className="w-full shadow-sm ">
      <div className="flex items-center justify-between p-4 container mx-auto">
        <div className="text-lg font-bold">
          Optimization Holt-winter using Genetic algorithm
        </div>
        <div className="flex gap-6 text-muted-foreground">
          <DarkModeToggle />
        </div>
      </div>
      <Separator />
    </nav>
  );
}
