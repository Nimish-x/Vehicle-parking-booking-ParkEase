<template>
  <div class="container">
    <h1>My Bookings</h1>

    <div v-if="loading" class="loading">Loading bookings...</div>

    <div class="content" v-else>
     
      <section class="bookings-table">
        <table cellpadding="8" cellspacing="0" border="1" style="width: 100%; border-collapse: collapse;">
          <thead>
            <tr>
              <th>Booking ID</th>
              <th>Spot ID</th>
              <th>Parking Lot</th>
              <th>Address</th>
              <th>Parking Time</th>
              <th>Leaving Time</th>
              <th>Fee (₹)</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            
            <tr v-for="booking in activeBookings" :key="booking.id">
              <td>{{ booking.id }}</td>
              <td>{{ booking.spot_id }}</td>
              <td>{{ booking.lot_address || 'Unknown' }}</td>
              <td>{{ booking.lot_address || 'Unknown' }}</td>
              <td>{{ formatDateTime(booking.parking_time) }}</td>
              <td>{{ booking.leaving_time ? formatDateTime(booking.leaving_time) : 'N/A' }}</td>
              <td>{{ formatCurrency(booking.parking_fee) }}</td>
              <td>Active</td>
              <td>
                <button
                  @click="releaseBooking(booking.id)"
                  :disabled="releasingBookingId === booking.id"
                  title="Release Booking"
                >
                  {{ releasingBookingId === booking.id ? 'Releasing...' : 'Release' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="activeBookings.length === 0" style="margin-top: 12px;">No active bookings found.</p>
      </section>

     
      <aside class="booking-wall">
        <h2>Booking History Wall</h2>
        <div v-if="bookings.length">
          <div 
            v-for="booking in bookings" 
            :key="booking.id" 
            class="booking-card" 
            :class="{ active: !booking.leaving_time, completed: booking.leaving_time }"
          >
            <strong>Booking ID:</strong> {{ booking.id }}<br />
            <strong>Lot:</strong> {{ booking.lot_address || 'Unknown' }}<br />
            <strong>Spot:</strong> {{ booking.spot_id }}<br />
            <strong>Parking:</strong> {{ formatDateTime(booking.parking_time) }}<br />
            <strong>Leaving:</strong> {{ booking.leaving_time ? formatDateTime(booking.leaving_time) : 'N/A' }}<br />
            <strong>Fee:</strong> {{ formatCurrency(booking.parking_fee) }}<br />
            <strong>Status:</strong> {{ booking.leaving_time ? 'Completed' : 'Active' }}
          </div>
        </div>
        <p v-else>No booking history yet.</p>
      </aside>
    </div>

    
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bookings: [],
      error: '',
      success: '',
      releasingBookingId: null,
      loading: false,
    };
  },
  computed: {
    activeBookings() {
      
      return this.bookings.filter(b => !b.leaving_time);
    }
  },
  mounted() {
    this.fetchBookings();
  },
  methods: {
    async fetchBookings() {
      this.error = '';
      this.success = '';
      this.loading = true;
      try {
        const response = await fetch('/api/my_bookings', {
          method: 'GET',
          credentials: 'include', 
        });

        if (!response.ok) {
          if (response.status === 401) {
            this.error = 'You must be logged in to view bookings.';
          } else {
            this.error = 'Failed to load bookings.';
          }
          this.bookings = [];
          return;
        }

        const data = await response.json();
        console.log("Fetched bookings:", data);
        this.bookings = data;
      } catch (e) {
        this.error = e.message || 'An unexpected error occurred.';
      } finally {
        this.loading = false;
      }
    },

    async releaseBooking(bookingId) {
      this.error = '';
      this.success = '';
      this.releasingBookingId = bookingId;

      try {
        const response = await fetch(`/api/reservation/${bookingId}`, {
          method: 'DELETE',
          credentials: 'include',
        });

        if (!response.ok) {
          let errMsg = 'Failed to release booking.';
          try {
            const errData = await response.json();
            if (errData && errData.error) {
              errMsg = errData.error;
            }
          } catch {}
          throw new Error(errMsg);
        }

        this.success = 'Booking released successfully.';
        await this.fetchBookings();
      } catch (e) {
        this.error = e.message;
      } finally {
        this.releasingBookingId = null;
      }
    },

    formatDateTime(dtString) {
      if (!dtString) return 'N/A';
      const d = new Date(dtString);
      return d.toLocaleString();
    },

    formatCurrency(amount) {
      if (amount == null) return 'N/A';
      return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(amount);
    }
  },
};
</script>


<style scoped>
.container {
  max-width: 1200px;
  margin: 2em auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #082852; 
  color: #e0e7ff;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(4, 20, 66, 0.5);
}


.loading {
  margin: 10px 0;
  font-weight: 600;
  color: #90caf9; 
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


.content {
  display: flex;
  gap: 30px;
  align-items: flex-start;
}

.bookings-table {
  flex: 2;
  overflow-x: auto;
  background-color: #041c32;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(6, 45, 97, 0.7);
  padding: 15px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  color: #dbe9ff;
}

th,
td {
  border: 1px solid #1a3a6d;
  padding: 10px 14px;
  font-size: 0.95rem;
}

th {
  background-color: #1953b7;
  color: #e0e7ff;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-align: left;
}

tbody tr:hover {
  background-color: rgba(75, 135, 255, 0.15);
  cursor: default;
}

button {
  padding: 6px 12px;
  background-color: #33a7e2;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover:not(:disabled) {
  background-color: #1953b7;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.booking-wall {
  flex: 1;
  border-left: 2px solid #164e9b;
  padding-left: 20px;
  max-height: 600px;
  overflow-y: auto;
  min-width: 320px;
  background-color: #041c32;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(6, 45, 97, 0.7);
}

.booking-wall h2 {
  margin-bottom: 15px;
  color: #90caf9;
  font-weight: 700;
  font-size: 1.3rem;
}

.booking-card {
  border: 1px solid #1a3a6d;
  padding: 12px;
  margin-bottom: 12px;
  border-radius: 8px;
  background-color: #0c2a5d;
  font-size: 0.9rem;
  color: #dbe9ff;
  line-height: 1.4;
  user-select: none;
}

.booking-card.active {
  border-color: #4caf50;
  background-color: #194d27;
  color: #c8facc;
}

.booking-card.completed {
  opacity: 0.7;
  background-color: #162a45;
  color: #7ea3c9;
}

@media (max-width: 900px) {
  .content {
    flex-direction: column;
  }
  .booking-wall {
    border-left: none;
    border-top: 2px solid #164e9b;
    padding-left: 0;
    padding-top: 20px;
    max-height: none;
    min-width: 100%;
  }
}
</style>


