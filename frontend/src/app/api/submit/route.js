export async function POST(req) {
    try {
      const { dest_url } = await req.json();

      console.log("userInput:", dest_url);

      let backendURL = process.env.BACKEND_API_BASE_URL

      if (backendURL.endsWith("/")) {
        // strip the trailing slash /
        // i.e. http://127.0.0.1/ becomes http://127.0.0.1
        backendURL = backendURL.slice(0, -1)
      }
  
      const response = await fetch(`${backendURL}/api/shorten/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Api-Key ${process.env.BACKEND_API_KEY}`,
        },
        body: JSON.stringify({ dest_url }),

      });
  
      const data = await response.json();

      console.log("Data:", data);
  
      return Response.json(data);
    } catch (error) {
        console.log("Error:", error);
      return Response.json({ error: "Failed to fetch data" }, { status: 500 });
    }
}