import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";
import { Button } from "./ui/button";

export default function Navbar() {
  return (
    <nav
      className={cn("flex justify-between items-center p-4 shadow-sm border-b")}
    >
      <div className="text-xl font-bold">Eye Diseases Classifier</div>
      <div className="space-x-6">
        <Link to="/" className="text-muted-foreground hover:text-primary">
          Home
        </Link>
        <Link to="/about" className="text-muted-foreground hover:text-primary">
          About
        </Link>
        <Button>
          <Link
            to="/contact"
            className="text-muted-foreground hover:text-primary"
          >
            Contact
          </Link>
        </Button>
      </div>
    </nav>
  );
}
