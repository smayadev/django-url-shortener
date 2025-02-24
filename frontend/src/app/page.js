"use client";

import { useState } from "react";

export default function Home() {
  const [inputValue, setInputValue] = useState("");
  const [responseMessage, setResponseMessage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [captcha, setCaptcha] = useState(null);
  const [captchaAnswer, setCaptchaAnswer] = useState("");
  const [captchaError, setCaptchaError] = useState(null);
  const [isCaptchaVisible, setIsCaptchaVisible] = useState(false);

  const handleCaptchaCancel = () => {
    setIsCaptchaVisible(false);
    setLoading(false);
  };

  const handleGetCaptcha = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponseMessage(null);
    setCaptchaError(null);

    try {
      const response = await fetch("/api/proxy-captcha");
      const data = await response.json();

      if (response.ok) {
        setCaptcha(data);
        setIsCaptchaVisible(true);
      } else {
        throw new Error("Failed to load captcha");
      }
    } catch (error) {
      setResponseMessage("An error occurred.");
      setLoading(false);
    }
  };

  const handleCaptchaCheck = async () => {
    if (!captcha || !captchaAnswer.trim()) return;
    setCaptchaError(null);
  
    try {
      const response = await fetch("/api/proxy-check-captcha", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ captcha_id: captcha.captcha_id, answer: captchaAnswer }),
      });
  
      //const data = await response.json();
  
      if (response.ok) {
        setIsCaptchaVisible(false);
        setCaptchaAnswer("");
        submitForm();
      } else {
        setCaptchaError("Incorrect answer. Try again.");
      }
    } catch (error) {
      setCaptchaError("Error verifying captcha.");
    }
  };

  const submitForm = async () => {
    try {
      const response = await fetch("/api/proxy-submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ dest_url: inputValue }),
      });

      const data = await response.json();

      if (data.short_url) {
        setResponseMessage(`Success! Your shortened URL is ${data.short_url}`);
        setInputValue("");
      } else if (data.error) {
        setResponseMessage(data.error);
      } else {
        setResponseMessage("Unexpected error.");
      }

    } catch (error) {
      setResponseMessage("An error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-full bg-gray-100 mt-10 md:mt-20 lg:mt-20">
      <div className="bg-white p-6 rounded-lg w-full max-w-[800px]">
        <h1 className="text-2xl font-bold mb-4 text-center">URL Shortener</h1>
        <form onSubmit={handleGetCaptcha} className="flex items-center space-x-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="URL"
            required
            name="dest_url"
            className="p-4 h-14 text-lg border border-gray-300 rounded flex-1 w-full focus:outline-none focus:ring-2 focus:ring-blue-400" />
          <button
            type="submit"
            className="bg-blue-500 text-white p-4 h-14 px-6 text-xl rounded hover:bg-blue-600 transition"
            disabled={loading}>
            {loading ? "Loading..." : "Go!"}
          </button>
        </form>
        {responseMessage && <p className="mt-4 text-center font-semibold">{responseMessage}</p>}
      </div>

      {/* Captcha Modal */}
      {isCaptchaVisible && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
          <div className="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
            <h2 className="text-xl font-bold mb-4">Security Check</h2>
            <p className="mb-4">{captcha?.question}</p>
            <input
              type="text"
              value={captchaAnswer}
              onChange={(e) => setCaptchaAnswer(e.target.value)}
              className="p-2 border border-gray-300 rounded w-full mb-4" />
            {captchaError && <p className="text-red-500">{captchaError}</p>}
            <div className="flex justify-end space-x-2">
              <button
                onClick={handleCaptchaCheck}
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                Submit
              </button>
              <button 
                onClick={handleCaptchaCancel}
                className="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500">
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
