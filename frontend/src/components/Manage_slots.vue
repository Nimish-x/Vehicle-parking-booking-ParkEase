<script setup>
import { ref, reactive, onMounted } from 'vue'

const lots = ref([])
const loading = ref(false)
const error = ref(null)

const adding = ref(false)
const addError = ref(null)
const newLot = reactive({
  address: '',
  prime_location: '',
  price: '',
  no_of_spots: ''
})

const editingLotId = ref(null)
const editedLot = reactive({
  price: null,
  no_of_spots: null
})

const fetchLots = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await fetch('/api/parking_lot')
    if (!res.ok) throw new Error('Failed to fetch parking lots')
    lots.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

const addLot = async () => {
  addError.value = null
  if (!newLot.address || !newLot.prime_location || !newLot.price || !newLot.no_of_spots) {
    addError.value = 'Please fill in all fields.'
    return
  }
  if (isNaN(parseInt(newLot.price)) || isNaN(parseInt(newLot.no_of_spots))) {
    addError.value = 'Price and Number of Spots must be numbers.'
    return
  }
  adding.value = true
  try {
    const res = await fetch('/api/parking_add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        address: newLot.address,
        prime_location: newLot.prime_location,
        price: parseInt(newLot.price),
        no_of_spots: parseInt(newLot.no_of_spots)
      })
    })
    if (!res.ok) {
      const errData = await res.json()
      throw new Error(errData.error || 'Failed to add parking lot')
    }
    await fetchLots()
    Object.assign(newLot, { address: '', prime_location: '', price: '', no_of_spots: '' })
  } catch (e) {
    addError.value = e.message
  } finally {
    adding.value = false
  }
}

const deleteLot = async (id) => {
  if (!confirm('Are you sure you want to delete this parking lot?')) return
  try {
    const res = await fetch(`/api/parking_lot/${id}`, { method: 'DELETE' })
    if (!res.ok) {
      const errData = await res.json()
      throw new Error(errData.error || 'Failed to delete parking lot')
    }
    lots.value = lots.value.filter(lot => lot.id !== id)
  } catch (e) {
    alert(e.message)
  }
}

const startEditing = (lot) => {
  editingLotId.value = lot.id
  editedLot.price = lot.price
  editedLot.no_of_spots = lot.no_of_spots
}

// Cancel editing
const cancelEditing = () => {
  editingLotId.value = null
  editedLot.price = null
  editedLot.no_of_spots = null
}

const saveEdit = async (lotId) => {
  if (editedLot.price === null || editedLot.no_of_spots === null) {
    alert('Price and Number of Spots are required')
    return
  }
  if (isNaN(parseInt(editedLot.price)) || isNaN(parseInt(editedLot.no_of_spots))) {
    alert('Price and Number of Spots must be valid numbers')
    return
  }
  try {
    const res = await fetch(`/api/admin/parking_lot/${lotId}/update`, { 
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        price: parseInt(editedLot.price),
        no_of_spots: parseInt(editedLot.no_of_spots)
      })
    })
    if (!res.ok) {
      const errData = await res.json()
      throw new Error(errData.error || 'Failed to update parking lot')
    }
    await fetchLots()
    cancelEditing()
  } catch (e) {
    alert(e.message)
  }
}

onMounted(fetchLots)
</script>

<template>
  <div class="manage-lots">
    <h2>Manage Parking Lots</h2>

    <div class="add-lot-form">
      <h3>Add New Parking Lot</h3>
      <form @submit.prevent="addLot">
        <input v-model="newLot.address" type="text" placeholder="Address" required />
        <input v-model="newLot.prime_location" type="text" placeholder="Prime Location" required />
        <input v-model="newLot.price" type="number" placeholder="Price" required min="0" />
        <input v-model="newLot.no_of_spots" type="number" placeholder="Number of Spots" required min="1" />
        <button type="submit" :disabled="adding">Add Lot</button>
      </form>
      <div class="error" v-if="addError">{{ addError }}</div>
    </div>

    <div v-if="loading">Loading parking lots...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <table v-else-if="lots.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Address</th>
          <th>Prime Location</th>
          <th>Price</th>
          <th>No. of Spots</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="lot in lots" :key="lot.id">
          <td>{{ lot.id }}</td>
          <td>{{ lot.address }}</td>
          <td>{{ lot.prime_location }}</td>
          <td v-if="editingLotId !== lot.id">{{ lot.price }}</td>
          <td v-else>
            <input type="number" v-model.number="editedLot.price" min="0" />
          </td>
          <td v-if="editingLotId !== lot.id">{{ lot.no_of_spots }}</td>
          <td v-else>
            <input type="number" v-model.number="editedLot.no_of_spots" min="1" />
          </td>
          <td>
            <template v-if="editingLotId === lot.id">
              <button @click="saveEdit(lot.id)">Save</button>
              <button @click="cancelEditing">Cancel</button>
            </template>
            <template v-else>
              <button @click="startEditing(lot)">Edit</button>
              <button @click="deleteLot(lot.id)">Delete</button>
            </template>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else>No parking lots available.</div>
  </div>
</template>

<style scoped>
.manage-lots {
  max-width: 900px;
  margin: 2em auto;
  padding: 1.5em;
  background-color: #082852;
  border-radius: 10px;
  color: #ffffff;
  box-shadow: 0 6px 24px rgba(30, 70, 140, 0.12);
}

.add-lot-form {
  margin-bottom: 2em;
  padding: 1.5em;
  background-color: #041c32;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(4, 4, 80, 0.08);
}

.add-lot-form h3 {
  margin-bottom: 1em;
  color: #33a7e2;
  letter-spacing: 0.5px;
}

input[type="text"],
input[type="number"] {
  margin-right: 0.7em;
  margin-bottom: 0.7em;
  padding: 0.5em;
  min-width: 180px;
  border-radius: 6px;
  border: 1px solid #186fa4;
  background-color: #082852;
  color: #ffffff;
  font-size: 1em;
  outline: none;
  transition: border-color 0.2s ease;
}

input[type="text"]:focus,
input[type="number"]:focus {
  border-color: #33a7e2;
}

button {
  padding: 0.4em 1.2em;
  margin-left: 0.3em;
  margin-top: 0.3em;
  background-color: #33a7e2;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  font-size: 0.95em;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(33, 167, 226, 0.09);
  transition: background-color 0.2s ease;
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
  vertical-align: middle;
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
