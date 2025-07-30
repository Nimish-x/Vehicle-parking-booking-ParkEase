<script setup>
import { ref, onMounted } from 'vue'

const reservations = ref([])
const loading = ref(true)
const error = ref(null)

const fetchReservations = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await fetch('/api/reservations')
    if (!res.ok) throw new Error('Failed to fetch reservations')
    reservations.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchReservations)
</script>

<template>
  <div class="app-bookings">
    <h2>All Reservations</h2>

    <div v-if="loading">Loading reservations...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <table v-if="reservations.length > 0">
        <thead>
          <tr>
            <th>ID</th>
            <th>Spot id</th>
            <th>User id</th>
            <th>Parking Time</th>
            <th>Leaving time</th>
            <th>Parking Fee</th>
            <th>Availability</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="res in reservations" :key="res.id">
            <td>{{ res.id }}</td>
            <td>{{ res.spot_id }}</td>
            <td>{{ res.user_id }}</td>
            <td>{{ res.parking_time }}</td>
            <td>{{ res.leaving_time }}</td>
            <td>{{ res.parking_fee }}</td>
            <td>{{ res.Availability }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else>No reservations found.</div>
    </div>
  </div>
</template>

<style scoped>
.app-bookings {
  max-width: 800px;
  margin: 2em auto;
}
button:hover {
  background-color: #1953b7;
}

.error {
  color: #ff8282;
  margin-top: 0.8em;
  font-weight: 500;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 1em;
  background-color: #041c32;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(14, 45, 70, 0.14);
}

th,
td {
  border-bottom: 1px solid #186fa4;
  padding: 0.7em 0.8em;
  text-align: left;
  font-size: 1em;
}

th {
  background-color: #1953b7;
  color: #ffffff;
  font-weight: 600;
  letter-spacing: 0.5px;
}

tr:last-child td {
  border-bottom: none;
}

tbody tr:hover {
  background-color: rgba(51, 167, 226, 0.07);
}
</style>
