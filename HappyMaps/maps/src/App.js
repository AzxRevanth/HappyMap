import React, { useEffect } from 'react';
import './App.css';

let latitudes = [];
let longitudes = [];
let happinessScores = [];
let map, heatmap;

function App() {
  useEffect(() => {
    initMap();
  }, []);

  function getEmojiUrl(score) {
    if (score >= 6) {
      return "/emoji/super-happy.png";
    } else if (score >= 5) {
      return "/emoji/happy.png";
    } else if (score >= 4) {
      return "/emoji/neutral.png";
    } else if (score >= 2) {
      return "/emoji/sad.png";
    } else {
      return "/emoji/super-sad.png";
    }
  }

  function initMap() {
    fetch("http://localhost:5000/api/emotion")
      .then(response => response.json())
      .then(data => {
        if (data.length > 0) {
          data.forEach(row => {
            latitudes.push(parseFloat(row.latitude));
            longitudes.push(parseFloat(row.longitude));
            happinessScores.push(parseFloat(row.score));
          });

          if (latitudes.length > 0) {
            map = new window.google.maps.Map(document.getElementById("map"), {
              zoom: 5.3,
              center: { lat: 22.9734, lng: 78.6569 },
              mapTypeId: "satellite",
            });

            const gradient = [
              "rgba(0, 255, 255, 0)",
              "rgba(0, 255, 255, 1)",
              "rgba(0, 191, 255, 1)",
              "rgba(0, 127, 255, 1)",
              "rgba(0, 63, 255, 1)",
              "rgba(0, 0, 255, 1)",
              "rgba(0, 0, 223, 1)",
              "rgba(0, 0, 191, 1)",
              "rgba(0, 0, 159, 1)",
              "rgba(0, 0, 127, 1)",
              "rgba(63, 0, 91, 1)",
              "rgba(127, 0, 63, 1)",
              "rgba(191, 0, 31, 1)",
              "rgba(255, 0, 0, 1)",
            ];

            heatmap = new window.google.maps.visualization.HeatmapLayer({
              data: getPoints(),
              map: map,
              gradient: gradient,
              radius: 40,
            });

            latitudes.forEach((lat, index) => {
              if (!isNaN(lat) && !isNaN(longitudes[index]) && !isNaN(happinessScores[index])) {
                const marker = new window.google.maps.Marker({
                  position: { lat: lat, lng: longitudes[index] },
                  map: map,
                  title: `Happiness Score: ${happinessScores[index]}`,
                  icon: {
                    url: getEmojiUrl(happinessScores[index]),
                    scaledSize: new window.google.maps.Size(25, 25),
                  },
                });
              }
            });

            document
              .getElementById("toggle-heatmap")
              .addEventListener("click", toggleHeatmap);
            document
              .getElementById("change-opacity")
              .addEventListener("click", changeOpacity);
            document
              .getElementById("change-radius")
              .addEventListener("click", changeRadius);
          }
        } else {
          console.error("No data received for emotions.");
        }
      })
      .catch(error => console.error("Error fetching emotion data:", error));
  }

  function toggleHeatmap() {
    heatmap.setMap(heatmap.getMap() ? null : map);
  }

  function changeRadius() {
    heatmap.set("radius", heatmap.get("radius") ? null : 50);
  }

  function changeOpacity() {
    heatmap.set("opacity", heatmap.get("opacity") ? null : 0.2);
  }

  function getPoints() {
    return latitudes.map((lat, index) => {
      return {
        location: new window.google.maps.LatLng(lat, longitudes[index]),
        weight: happinessScores[index],
      };
    });
  }

  return (
    <div className="landing-page">
      <div className="content">
        <h1 className="title">Happy Maps</h1>
        <p className="subtitle">Happiness Has a Location!</p>
      </div>

      <div className='Map'>
        <div id='floating-panel'>
          <button id="toggle-heatmap">Toggle Heatmap</button>
          <button id="change-radius">Change radius</button>
          <button id="change-opacity">Change opacity</button>
        </div>

        <div id="map" style={{ height: '650px', width: '150%' }}></div>
      </div>
    </div>
  );
}

export default App;
