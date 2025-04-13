document.addEventListener("DOMContentLoaded", () => {
  // Fetch the prediction data from the JSON file
  fetch("prediction.json")
    .then(response => response.json())
    .then(data => {
      // Format the prediction text based on the prediction (Up or Down)
      const predictionText = `Apple Inc share is expected to go ${data.prediction === "Up" ? "UP" : "DOWN"}`;
      
      // Set the prediction text in the HTML
      document.getElementById("prediction").textContent = predictionText;
      
      // Optionally, add a class for styling purposes (for example: "up" or "down" class for different styles)
      document.getElementById("prediction").className = data.prediction.toLowerCase();
      
      // Set the date when the prediction was made
      document.getElementById("date").textContent = `Prediction Date: ${data.date}`;
      
      // Set the timestamp for when the prediction was last updated
      document.getElementById("timestamp").textContent = `Last Updated: ${new Date(data.updated_at).toLocaleString()}`;
    })
    .catch(error => {
      // Handle errors in fetching the data
      document.getElementById("prediction").textContent = "Error loading prediction.";
      console.error("Prediction load failed:", error);
    });
});
