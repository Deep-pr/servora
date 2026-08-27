document.addEventListener('DOMContentLoaded', () => {
  const mapEl = document.getElementById('provider-map');
  if (mapEl && window.L) {
    const markerEl = document.getElementById('provider-markers');
    const markers = markerEl ? JSON.parse(markerEl.textContent) : [];
    const map = L.map(mapEl).setView([27.4886, 95.3558], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
    if (markers.length) {
      const bounds = [];
      markers.forEach((provider) => {
        const point = [provider.lat, provider.lng];
        bounds.push(point);
        L.marker(point).addTo(map).bindPopup(`<strong>${provider.name}</strong><br>Rating ${provider.rating}<br>Trust ${provider.trust_score}<br><a href="${provider.url}">View profile</a>`);
      });
      map.fitBounds(bounds, { padding: [30, 30] });
    } else {
      L.marker([27.4886, 95.3558]).addTo(map).bindPopup('Servora demo area');
    }
  }

  const chartEl = document.getElementById('bookingChart');
  if (chartEl && window.Chart) {
    new Chart(chartEl, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
          label: 'Bookings',
          data: [12, 18, 28, 24, 38, 46],
          borderColor: '#1267d8',
          backgroundColor: 'rgba(18, 103, 216, .12)',
          fill: true,
          tension: .35
        }]
      }
    });
  }

  document.querySelectorAll('.analytics-chart').forEach((canvas) => {
    if (!window.Chart) return;
    const labels = JSON.parse(canvas.dataset.labels.replaceAll("'", '"'));
    const values = JSON.parse(canvas.dataset.values);
    new Chart(canvas, {
      type: canvas.dataset.chartType,
      data: {
        labels,
        datasets: [{
          label: 'Total',
          data: values,
          borderColor: '#1267d8',
          backgroundColor: ['#1267d8', '#ffc247', '#21a67a', '#ef5b5b', '#6b7cff', '#16a3b8', '#8b5cf6', '#f97316'],
          tension: .35,
          fill: canvas.dataset.chartType === 'line'
        }]
      },
      options: { responsive: true, maintainAspectRatio: true }
    });
  });
});
