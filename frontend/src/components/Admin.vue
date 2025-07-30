<template>
    <div id="dashboard-container">
      <nav class="navbar">
        <div class="navbar-brand">ParkEase</div>
        <ul class="navbar-menu">
          <RouterLink to="/" class="btn">Logout</RouterLink>
        </ul>
      </nav>
  
      <div class="dashboard-content">
        <h1 class="display-4">Welcome Admin</h1>
        <p class="lead">Manage your parking customers with ease</p>
  
        
        <div class="dashboard-widgets">
          <RouterLink to='/manage_slots' class="widget">🚗 Manage Parking Spot</RouterLink>
          <RouterLink to='/app_bookings' class="widget">📅 App Bookings</RouterLink>
          <RouterLink to="/user_details" class="widget">👨‍🦰 User Details</RouterLink>
          <RouterLink to="/chart" class="widget" >📊 Summary</RouterLink>
          <!-- <RouterLink to='/user_info' class="widget">👤 Account Info</RouterLink> -->
        </div>
        <div style="margin-top: 40px; text-align: center;">
          <button @click="sendPromotionalEmails" :disabled="sendingPromo" style="margin-right: 10px;">
            {{ sendingPromo ? 'Sending Promotional Emails...' : 'Sent Promotional Emails' }}
          </button>
          <button @click="sendParkingSummaryEmails" :disabled="sendingSummary" >
            {{ sendingSummary ? 'Sending Parking Summaries...' : 'Send Parking Summary Emails' }}
          </button>
          <p v-if="message" :style="{ color: messageColor, marginTop: '10px' }">{{ message }}</p>
        </div>
      </div>
    </div>
  </template>
  
<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const sendingPromo = ref(false)
const sendingSummary = ref(false)
const message = ref('')
const messageColor = ref('green')

const sendPromotionalEmails = async () => {
  sendingPromo.value = true
  message.value = ''
  try {
    const res = await fetch('/api/admin/send_promotional_email', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    })
    if (!res.ok) {
      const errData = await res.json()
      throw new Error(errData.error || 'Failed to send promotional emails')
    }
    const data = await res.json()
    message.value = data.message || 'Promotional emails sent!'
    messageColor.value = 'green'
  } catch (e) {
    message.value = e.message
    messageColor.value = 'red'
  } finally {
    sendingPromo.value = false
  }
}

const sendParkingSummaryEmails = async () => {
  sendingSummary.value = true
  message.value = ''
  try {
    const res = await fetch('/api/admin/send_parking_summary_email', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    })
    if (!res.ok) {
      const errData = await res.json()
      throw new Error(errData.error || 'Failed to send parking summary emails')
    }
    const data = await res.json()
    message.value = data.message || 'Parking summary emails sent!'
    messageColor.value = 'green'
  } catch (e) {
    message.value = e.message
    messageColor.value = 'red'
  } finally {
    sendingSummary.value = false
  }
}
</script>
  
  <style>
  #dashboard-container {
    padding: 60px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.2);
    max-width: 1000px;
    margin: auto;
    position: relative;
  }
  
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #007bff;
    padding: 15px 30px;
    border-radius: 10px;
    color: white;
  }
  
  .navbar-brand {
    font-size: 24px;
    font-weight: bold;
  }
  
  .navbar-menu {
    list-style: none;
    display: flex;
    gap: 20px;
  }
  
  .navbar-menu li a {
    color: white;
    text-decoration: none;
    font-weight: 500;
  }
  
  .navbar-menu li a:hover {
    text-decoration: underline;
  }
  
  .dashboard-content {
    text-align: center;
    margin-top: 40px;
  }
  
  .display-4 {
    font-weight: bold;
    color: #007bff;
  }
  
  .lead {
    font-size: 20px;
    color: #333333;
    margin-bottom: 30px;
  }
  
  .dashboard-widgets {
    display: flex;
    justify-content: center;
    gap: 30px;
    flex-wrap: wrap;
  }
  
  .widget {
    background-color: #f0f8ff;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 5px 15px rgba(0, 123, 255, 0.1);
    font-size: 18px;
    font-weight: 500;
    min-width: 200px;
  }
  </style>
  