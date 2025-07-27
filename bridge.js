const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;

app.use(bodyParser.json());

app.post('/api/happiness', async (req, res) => {
  const query = req.body.query;
  console.log("Received query from user:", query);

  try {
    const response = await axios.post('http://localhost:5000/analyze', {
      query: query
    });

    console.log("Response from Python Flask:", response.data);
    res.json(response.data);
  } catch (error) {
    console.error("Error calling Flask service:", error.message);
    res.status(500).json({ error: "Flask service error" });
  }
});

app.listen(PORT, () => {
  console.log(`✅ Node server is running on http://localhost:${PORT}`);
});
