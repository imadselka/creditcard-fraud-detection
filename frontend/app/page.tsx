"use client";

import { Button } from "@/components/ui/button";
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
      const response = await axios.post("http://localhost:8000/predict/", {
        card_number: cardNumber,
        amount: parseFloat(amount),
      });

      setResult(response.data);
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
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h1 className="text-2xl font-bold mb-4">Fraud Detection</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">
              Card Number
            </label>
            <input
              type="text"
              value={cardNumber}
              onChange={(e) => setCardNumber(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary sm:text-sm"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">
              Amount
            </label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary sm:text-sm"
              required
            />
          </div>

          <Button
            type="submit"
            variant="outline"
            className="flex items-center justify-center w-full"
          >
            {isLoading ? "Checking..." : "Check Fraud"}
          </Button>
        </form>

        {result && (
          <div className="mt-6">
            {result.error ? (
              <p className="text-red-500">{result.error}</p>
            ) : (
              <div>
                <p>
                  <strong>Is Fraudulent:</strong>{" "}
                  {result.is_fraudulent ? "Yes" : "No"}
                </p>
                <p>
                  <strong>Fraud Probability:</strong>{" "}
                  {result.fraud_probability.toFixed(4)}
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
