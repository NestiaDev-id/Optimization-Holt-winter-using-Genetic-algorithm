import { cn } from "@/lib/utils";
import { Button } from "./ui/button";

import { Link } from "react-router-dom";
import { Separator } from "@/components/ui/separator";

export default function Navbar() {
  return (
    <nav className="bg-background w-full shadow-sm">
      <div className="flex items-center justify-between p-4 container mx-auto">
        <div className="text-lg font-bold">Eye Diseases Classifier</div>
        <div className="flex gap-6 text-muted-foreground">
          <Link to="/" className="hover:text-primary">
            Home
          </Link>
          <Link to="/about" className="hover:text-primary">
            About
          </Link>
          <Link to="/contact" className="hover:text-primary">
            Contact
          </Link>
        </div>
      </div>
      <Separator />
    </nav>
  );
}
