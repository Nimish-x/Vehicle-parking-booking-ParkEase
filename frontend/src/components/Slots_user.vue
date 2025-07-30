<template>
    <div>
      <h1>Parking Lots Availability</h1>
      <div v-for="lot in parkingLots" :key="lot.id" class="lot-card">
        <p><strong>Address:</strong> {{ lot.address }}</p>
        <p><strong>Price:</strong> ₹{{ lot.price }}</p>
        <p><strong>Total Spots:</strong> {{ lot.total_spots }}</p>
        <p>
          <strong>Free Spots:</strong> {{ lot.free_spots }}
          <button 
            :disabled="lot.free_spots === 0 || bookingLotId === lot.id" 
            @click="bookSpot(lot.id)">
            {{ bookingLotId === lot.id ? "Booking..." : "Book Spot" }}
          </button>
        </p>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">{{ success }}</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        parkingLots: [],
        bookingLotId: null,
        error: '',
        success: ''
      }
    },
    mounted() {
      this.fetchParkingLots();
    },
    methods: {
      async fetchParkingLots() {
        try {
          const response = await fetch('/api/parking_lots/availability', {
            credentials: 'include' 
          });
          if (!response.ok) throw new Error('Failed to fetch parking lots');
          this.parkingLots = await response.json();
        } catch (e) {
          this.error = e.message;
        }
      },
      async bookSpot(lotId) {
        this.error = '';
        this.success = '';
        this.bookingLotId = lotId;
        try {
          const response = await fetch(`/api/parking_lots/${lotId}/book`, {
            method: 'POST',
            credentials: 'include', 
            headers: { 'Content-Type': 'application/json' }
            
          });
          if (!response.ok) {
            const errResp = await response.json();
            throw new Error(errResp.error || 'Booking failed');
          }
          const data = await response.json();
          this.success = data.message || 'Spot booked successfully';
          this.fetchParkingLots(); // refresh spots , this line basically refreshes it...
        } catch (e) {
          this.error = e.message;
        } finally {
          this.bookingLotId = null;
        }
      }
    }
  };
  </script>
  
  <style scoped>
.lot-card {
  border: 1px solid #164e1f; 
  padding: 20px;
  margin-bottom: 15px;
  background-color: #082852; 
  border-radius: 10px;
  color: #e0e7ff; 
  box-shadow: 0 4px 12px rgba(4, 20, 66, 0.6);
  transition: box-shadow 0.3s ease;
}

.lot-card:hover {
  box-shadow: 0 6px 20px rgba(33, 167, 226, 0.5);
}

button {
  margin-left: 10px;
  padding: 7px 14px;
  background-color: #33a7e2;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:disabled {
  background-color: #1953b7;
  cursor: not-allowed;
  opacity: 0.6;
}

button:hover:not(:disabled) {
  background-color: #1953b7;
}

.error {
  color: #ff6b6b; 
  margin-top: 15px;
  font-weight: 600;
}

.success {
  color: #81c784; 
  margin-top: 15px;
  font-weight: 600;
}

h1 {
  color: #33a7e2;
  margin-bottom: 20px;
  font-weight: 700;
  font-family: Arial, sans-serif;
}
</style>

  