export async function GET() {
    try {
      const apiKey = process.env.BACKEND_API_KEY;
      let backendURL = process.env.BACKEND_API_BASE_URL

      if (backendURL.endsWith("/")) {
          // strip the trailing slash /
          // i.e. http://127.0.0.1/ becomes http://127.0.0.1
          backendURL = backendURL.slice(0, -1)
      }
  
      const response = await fetch(`${backendURL}/api/captcha/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Api-Key ${apiKey}`,
        },
      });
  
      if (!response.ok) {
        throw new Error("Failed to fetch captcha");
      }
  
      const data = await response.json();
      return Response.json(data);
    } catch (error) {
      return Response.json({ error: error.message }, { status: 500 });
    }
  }
  