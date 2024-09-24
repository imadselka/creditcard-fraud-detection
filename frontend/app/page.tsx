"use client";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import axios from "axios";
import { useState } from "react";

export default function Home() {
  const [cardNumber, setCardNumber] = useState("");
  const [amount, setAmount] = useState("");
  const [result, setResult] = useState<{
    is_fraudulent: boolean;
    fraud_probability: number;
    error?: string;
  } | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setResult(null);

    try {
      const currentTime = new Date();
      const secondsSinceMidnight =
        currentTime.getHours() * 3600 +
        currentTime.getMinutes() * 60 +
        currentTime.getSeconds();

      const { data } = await axios.post("http://localhost:8000/predict/", {
        card_number: cardNumber,
        amount: parseFloat(amount),
        time: secondsSinceMidnight,
      });

      setResult(data);
    } catch (error) {
      console.error("Error:", error);
      setResult({
        is_fraudulent: false,
        fraud_probability: 0,
        error: "An error occurred while processing your request.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>Credit Card Fraud Detection</CardTitle>
          <CardDescription>
            Enter credit card details to check if it&apos;s legitimate or
            fraudulent.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="grid w-full items-center gap-4">
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="cardNumber">Credit Card Number</Label>
                <Input
                  id="cardNumber"
                  placeholder="Enter credit card number"
                  value={cardNumber}
                  onChange={(e) => setCardNumber(e.target.value)}
                />
              </div>
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="amount">Transaction Amount</Label>
                <Input
                  id="amount"
                  type="number"
                  placeholder="Enter transaction amount"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                />
              </div>
            </div>
          </form>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button onClick={handleSubmit} disabled={isLoading}>
            {isLoading ? "Checking..." : "Check Card"}
          </Button>
        </CardFooter>
      </Card>
      {result && (
        <Card className="mt-4 p-4">
          {result.error ? (
            <p className="text-center text-red-600">{result.error}</p>
          ) : (
            <>
              <p className="text-center font-semibold">
                Result:{" "}
                <span
                  className={
                    result.is_fraudulent ? "text-red-600" : "text-green-600"
                  }
                >
                  {result.is_fraudulent ? "Fraudulent" : "Legitimate"}
                </span>
              </p>
              <p className="text-center">
                Fraud Probability: {(result.fraud_probability * 100).toFixed(2)}
                %
              </p>
            </>
          )}
        </Card>
      )}
    </main>
  );
}
