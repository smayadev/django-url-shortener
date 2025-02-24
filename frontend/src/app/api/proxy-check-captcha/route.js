export async function POST(req) {
    try {
      const { captcha_id, answer } = await req.json();
      const apiKey = process.env.BACKEND_API_KEY;
      let backendURL = process.env.BACKEND_API_BASE_URL

      if (backendURL.endsWith("/")) {
          // strip the trailing slash /
          // i.e. http://127.0.0.1/ becomes http://127.0.0.1
          backendURL = backendURL.slice(0, -1)
      }
  
      const response = await fetch(`${backendURL}/api/captcha/${captcha_id}/check/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Api-Key ${apiKey}`,
        },
        body: JSON.stringify({ answer }),
      });
  
      if (!response.ok) {
        throw new Error("Captcha validation failed");
      }
  
      const data = await response.json();
      return Response.json(data);
    } catch (error) {
      return Response.json({ error: error.message }, { status: 500 });
    }
  }
  