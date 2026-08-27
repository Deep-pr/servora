document.addEventListener('DOMContentLoaded', () => {
  const mapEl = document.getElementById('provider-map');
  if (mapEl && window.L) {
    const map = L.map(mapEl).setView([27.4886, 95.3558], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
    L.marker([27.4886, 95.3558]).addTo(map).bindPopup('Servora demo area');
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
