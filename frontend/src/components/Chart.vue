<template>
    <div class="booking-summary-chart">
      <h2>Active Bookings per Parking Lot</h2>
      <canvas ref="barChartCanvas"></canvas>
  
      <p v-if="loading">Loading data...</p>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import Chart from 'chart.js/auto'
  
  const barChart = ref(null)
  const barChartCanvas = ref(null)
  
  const loading = ref(false)
  const error = ref('')
  
  const chartData = ref({
    labels: [],
    datasets: []
  })
  
  function renderChart() {
    // To Destroy old chart instance before creating new chrat
    if (barChart.value) {
      barChart.value.destroy()
      barChart.value = null
    }
    if (!barChartCanvas.value) return
  
    const { labels, datasets } = chartData.value
    if (
      Array.isArray(labels) &&
      Array.isArray(datasets) &&
      datasets.length > 0 &&
      Array.isArray(datasets[0].data) &&
      labels.length === datasets[0].data.length
    ) {
      barChart.value = new Chart(barChartCanvas.value, {
        type: 'bar',
        data: chartData.value,
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
            tooltip: { enabled: true }
          },
          scales: {
            y: {
              beginAtZero: true,
              precision: 0,
              title: { display: true, text: 'Active Bookings' }
            },
            x: {
              title: { display: true, text: 'Parking Lot' }
            }
          }
        }
      })
    }
  }
  
  const fetchSummary = async () => {
    loading.value = true
    error.value = ''
    try {
      const res = await fetch('/api/admin/bookings_summary', {
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' }
      })
  
      if (!res.ok) {
        const errData = await res.json()
        throw new Error(errData.error || 'Failed to load booking summary')
      }
  
      const data = await res.json()
  
      // Safely mapping API data into chart to suit the format
      const labels = Array.isArray(data.summary) ? data.summary.map(item => item.address) : []
      const values = Array.isArray(data.summary) ? data.summary.map(item => item.active_bookings) : []
  
      chartData.value = {
        labels,
        datasets: [{
          label: 'Active Bookings',
          backgroundColor: '#33a7e2',
          data: values
        }]
      }
  
      renderChart()
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }
  
  onMounted(fetchSummary)
  </script>
  
  <style scoped>
  .booking-summary-chart {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: #082852;
    padding: 1.5em 2em 2em;
    box-sizing: border-box;
    font-family: Arial, sans-serif;
    color: #e0e7ff;
    display: flex;
    flex-direction: column;
    border-radius: 0;
    box-shadow: none;
  }
  
  .booking-summary-chart > h2 {
    margin: 0 0 1em 0;
    color: #33a7e2;
    user-select: none;
    flex: 0 0 auto;
  }
  
  .booking-summary-chart canvas {
    flex: 1 1 auto;
    width: 100% !important;
    height: 100% !important;
    max-width: 100% !important;
    max-height: 100% !important;
  }
  
  .error {
    margin-top: 1em;
    color: #ff8282;
    font-weight: 600;
    user-select: none;
    flex: none;
  }
  </style>
  