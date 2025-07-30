<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useUserStore } from '@/stores/user';



const email = ref('');
const password = ref('');
const router=useRouter();
const errorMessages=ref('');
const userStore=useUserStore();

const loginUser = async () => {
  if (!email.value || !password.value) {
    alert('Enter both the fields');
    return;
  }

  try {
    const response = await axios.post(
      'http://127.0.0.1:5000/api/auth/login',
      JSON.stringify({
        email: email.value,
        password: password.value
      }),
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
      console.log(response.data);
    if (response.data.success) {
    try {
      const userInfo = await axios.get('http://127.0.0.1:5000/api/auth/user', {
        withCredentials: true
      });
      console.log(userInfo.data.roles);
      userStore.setUserInfo(userInfo.data);
      router.push('/user-dashboard');

    } catch (error) {
      errorMessages.value = 'Failed to fetch user info';
    }
}
 else {
      errorMessages.value = response.data.message || 'Login failed';
    }

  } catch (err) {
    console.error('Login request failed:', err);
    errorMessages.value = 'Server error. Please try again later.';
  }
};

</script>

<template>
  <div id="login-container">
    <div class="login-box">
      <h1 class="display-4">Login to ParkEase</h1>
      <h3 class="lead mb-4">Access your parking dashboard</h3>

      <form @submit.prevent="loginUser">
        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input v-model="email" type="email" class="form-control" id="email" >
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" id="password" >
        </div>

        <button type="submit" class="btn btn-primary w-100">Login</button>
        <h3>or</h3>
        <RouterLink to='/signup' class="btn btn-primary btn-lg">Signup</RouterLink>
        <RouterLink to='/admin-login' class="btn btn-primary btn-lg">Login as Admin</RouterLink>
      </form>
    </div>
  </div>
</template>

<style scoped>
#login-container {
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

.login-box {
  
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

.login-box input.form-control {
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
