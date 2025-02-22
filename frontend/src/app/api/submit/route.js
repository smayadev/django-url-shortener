export async function POST(req) {
    try {
      const { dest_url } = await req.json();

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

      if (!response.ok) {
        console.log(response);

        if (response.status === 400) {
          throw new Error("400 Bad Request");
        }

      }

      return Response.json(data);

    } catch (error) {

      return Response.json({ error: `${error}` });

    }
}