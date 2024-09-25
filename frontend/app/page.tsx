"use client";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import axios from "axios";
import { CheckCircle, XCircle } from "lucide-react";
import { useState } from "react";

export default function Home() {
  const [cardNumber, setCardNumber] = useState("");
  const [amount, setAmount] = useState("");
  const [result, setResult] = useState<{
    is_fraudulent: boolean;
    fraud_probability: number;
    is_valid_card: boolean;
  } | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setResult(null);

    try {
      const response = await axios.post(`${process.env.API_URL}/predict/`, {
        card_number: cardNumber,
        amount: parseFloat(amount),
      });

      setResult(response.data);
    } catch (error) {
      console.error("Error:", error);
      setResult({
        is_fraudulent: true,
        fraud_probability: 1,
        is_valid_card: false,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <Card className="w-[400px]">
        <CardHeader>
          <CardTitle className="text-2xl font-bold">Fraud Detection</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="cardNumber">Card Number</Label>
              <Input
                id="cardNumber"
                type="text"
                value={cardNumber}
                onChange={(e) => setCardNumber(e.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="amount">Amount</Label>
              <Input
                id="amount"
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
              />
            </div>

            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? "Checking..." : "Check Fraud"}
            </Button>
          </form>

          {result && (
            <div className="mt-6 space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-semibold">Card Validity:</span>
                {result.is_valid_card ? (
                  <div className="flex items-center text-green-500">
                    <CheckCircle className="w-5 h-5 mr-1" />
                    Valid
                  </div>
                ) : (
                  <div className="flex items-center text-red-500">
                    <XCircle className="w-5 h-5 mr-1" />
                    Invalid
                  </div>
                )}
              </div>
              <div className="flex items-center justify-between">
                <span className="font-semibold">Fraud Status:</span>
                {result.is_fraudulent ? (
                  <div className="flex items-center text-red-500">
                    <XCircle className="w-5 h-5 mr-1" />
                    Fraudulent
                  </div>
                ) : (
                  <div className="flex items-center text-green-500">
                    <CheckCircle className="w-5 h-5 mr-1" />
                    Not Fraudulent
                  </div>
                )}
              </div>
              <div className="flex items-center justify-between">
                <span className="font-semibold">Fraud Probability:</span>
                <span
                  className={
                    result.fraud_probability > 0.5
                      ? "text-red-500"
                      : "text-green-500"
                  }
                >
                  {(result.fraud_probability * 100).toFixed(2)}%
                </span>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
