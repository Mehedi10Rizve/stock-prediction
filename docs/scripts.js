document.addEventListener("DOMContentLoaded", () => {
    fetch("prediction.json")
      .then(response => response.json())
      .then(data => {
        const predictionText = data.prediction === "Up" ? "📈 Market will go UP" : "📉 Market will go DOWN";
        document.getElementById("prediction").textContent = predictionText;
        document.getElementById("prediction").className = data.prediction.toLowerCase();
        document.getElementById("date").textContent = `Prediction Date: ${data.date}`;
        document.getElementById("timestamp").textContent = `Last Updated: ${new Date(data.updated_at).toLocaleString()}`;
      })
      .catch(error => {
        document.getElementById("prediction").textContent = "Error loading prediction.";
        console.error("Prediction load failed:", error);
      });
  });
  