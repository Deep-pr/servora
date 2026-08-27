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
});
