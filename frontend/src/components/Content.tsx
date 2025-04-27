import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Progress } from "@/components/ui/progress";

export default function Content() {
  return (
    <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Chart (Nomor 3) */}
      <Card className="flex justify-center items-center">
        <CardContent className="p-4">
          <img
            src="/your-image.png"
            alt="Eye Fundus"
            className="rounded-lg max-h-[500px] object-contain"
          />
        </CardContent>
      </Card>

      {/* Card Prediction (Nomor 4) */}
      <div className="flex flex-col gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Prediction</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            <div className="space-y-2">
              <Label>Diagnosis</Label>
              <Input value="Glaucoma" readOnly />
            </div>

            <div className="space-y-2">
              <Label>Confidence</Label>
              <Progress value={86} />
              <div className="text-sm text-muted-foreground">86%</div>
            </div>
          </CardContent>
        </Card>

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
  );
}
