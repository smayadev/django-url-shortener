"use client";

import { useState } from "react";

export default function Home() {
  const [inputValue, setInputValue] = useState("");
  const [responseMessage, setResponseMessage] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponseMessage(null);

    try {
      const response = await fetch("/api/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ dest_url: inputValue }),
      });

      console.log("inputValue:", inputValue);
      console.log("JSON:", JSON.stringify({ dest_url: inputValue }))

      const data = await response.json();
      console.log(data);
      if (data.short_url) {
        setResponseMessage(`Success! Your shortened URL is ${data.short_url}`);
      } else {
        console.log("got an error that needs to be returned as error in backend (but it wasn't)");
        console.log(data);
        setResponseMessage("an error occurred that wasn't handled as an error");
      }
    } catch (error) {
      setResponseMessage("Error submitting the form. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-full bg-gray-100 mt-10 md:mt-20 lg:mt-20">
      <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-[800px]">
        <h1 className="text-2xl font-bold mb-4 text-center">URL Shortener</h1>
        <form onSubmit={handleSubmit} className="flex items-center space-x-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Enter something..."
            required
            name="dest_url"
            className="p-4 h-14 text-lg border border-gray-300 rounded flex-1 w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            type="submit"
            className="bg-blue-500 text-white p-4 h-14 px-6 text-xl rounded hover:bg-blue-600 transition"
            disabled={loading}
          >
            {loading ? "Submitting..." : "Go!"}
          </button>
        </form>
        {responseMessage && (
          <p className="mt-4 text-center font-semibold">{responseMessage}</p>
        )}
      </div>
    </div>
  );
}
