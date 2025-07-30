<template>
  <div id="signup-container">
    <div class="signup-box">
      <h1 class="display-4">Sign up for ParkEase</h1>
      <h3 class="lead mb-4">Create your parking account</h3>

      <form @submit.prevent="registerUser">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input v-model="username" type="text" class="form-control" id="username" required autocomplete="username">
        </div>

        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input v-model="email" type="email" class="form-control" id="email" required autocomplete="email">
        </div>

        <div class="mb-3">
          <label for="phone" class="form-label">Phone Number</label>
          <input v-model="phone" type="tel" pattern="^\d{10,15}$" class="form-control" id="phone" required autocomplete="tel" />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" id="password" required autocomplete="new-password">
        </div>

        <div v-if="error" class="error">{{ error }}</div>
        <div v-if="success" class="success">{{ success }}</div>
        <button type="submit" class="btn btn-primary w-100">Signup</button>
        
      </form>
    </div>
  </div>
</template>

<script setup>
import router from '@/router'
import { ref } from 'vue'

const username = ref('')
const email = ref('')
const phone = ref('')
const password = ref('')
const error = ref('')
const success = ref('')

const registerUser = async () => {
  error.value = ''
  success.value = ''
  if (!username.value || !email.value || !password.value || !phone.value) {
    error.value = 'Please fill in all fields.'
    return
  }
  if (!/^\d{10,15}$/.test(phone.value)) {
    error.value = 'Phone number must be 10-15 digits.'
    return
  }
  try {
    const res = await fetch('/api/user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        phone: phone.value,
        password: password.value,
      }),
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.error || 'Failed to sign up.'
    } else {
      success.value = data.message || 'Signup successful! Please log in.'
      username.value = ''
      email.value = ''
      phone.value = ''
      password.value = ''
      alert('Now you can login safely')
      router.push('/login')
    }
  } catch (e) {
    error.value = 'An error occurred. Please try again later.'
  }
}
</script>
  
  <style>
  #signup-container {
    background: rgba(255, 255, 255, 0.9);
    padding: 60px;
    border-radius: 15px;
    box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.2);
    max-width: 800px;
    margin: auto;
    align-self: center;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  
  .signup-box {
    padding: 40px;
    border-radius: 15px;
    width: 100%;
    text-align: center;
    color: #333333;
  }
  
  .display-4 {
    font-weight: bold;
    color: #007bff;
  }
  
  .lead {
    font-size: 20px;
    color: #333333;
    margin-bottom: 20px;
  }
  
  .signup-box input.form-control {
    padding: 12px 16px;
    margin-bottom: 20px;
    border-radius: 6px;
    border: 1px solid #ccc;
    font-size: 16px;
    width: 100%;
  }
  
  .form-label {
    text-align: left;
    display: block;
    margin-bottom: 6px;
    font-weight: 500;
  }
  
  .btn-primary {
    background-color: #007bff;
    border: none;
    padding: 12px 20px;
    font-size: 18px;
    transition: all 0.3s ease-in-out;
  }
  
  .btn-primary:hover {
    background-color: #0056b3;
    transform: scale(1.05);
    border-radius: 30%;
  }
  </style>
  