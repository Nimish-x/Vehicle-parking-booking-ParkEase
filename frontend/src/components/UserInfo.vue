<template>
    <div class="user-info-container">
      <h1>My Profile</h1>
  
      <form @submit.prevent="updateProfile">
        <div class="form-group">
          <label for="email">Email:</label>
          <input
            id="email"
            type="email"
            v-model="form.email"
            required
            placeholder="Enter your email"
          />
        </div>
  
        <div class="form-group">
          <label for="username">Username:</label>
          <input
            id="username"
            type="text"
            v-model="form.username"
            required
            placeholder="Enter your username"
          />
        </div>
  
        <div class="form-group">
          <label for="phone">Phone:</label>
          <input
            id="phone"
            type="tel"
            v-model="form.phone"
            placeholder="Enter your phone number"
            pattern="^\d{10}$"
            title="Enter a valid 10-digit phone number"
          />
        </div>
  
        <div class="form-group">
          <label for="password">New Password:</label>
          <input
            id="password"
            type="password"
            v-model="form.password"
            placeholder="Leave blank to keep current password"
            minlength="6"
          />
        </div>
  
        <button type="submit" :disabled="loading">
          {{ loading ? "Updating..." : "Update Profile" }}
        </button>
      </form>
  
      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">{{ success }}</p>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from "vue";
  
  export default {
    name: "UserInfo",
    setup() {
      const form = ref({
        email: "",
        username: "",
        phone: "",
        password: "",
      });
  
      const loading = ref(false);
      const error = ref("");
      const success = ref("");
  
      // Fetch current user info on mount
      const fetchUserInfo = async () => {
        try {
          const response = await fetch("/api/user/current", {
            credentials: "include",
            method: "GET",
          });
  
          if (!response.ok) {
            throw new Error("Failed to load profile info.");
          }
  
          const data = await response.json();
  
          form.value.email = data.user_email || data.email || "";
          form.value.username = data.username || "";
          form.value.phone = data.phone ? data.phone.toString() : "";
        } catch (err) {
          error.value = err.message;
        }
      };
  
      // Updatign the profile on submit
      const updateProfile = async () => {
        error.value = "";
        success.value = "";
        loading.value = true;
  
        try {
          
          const payload = {
            email: form.value.email.trim(),
            username: form.value.username.trim(),
          };
          if (form.value.phone.trim() !== "") {
            payload.phone = form.value.phone.trim();
          }
          if (form.value.password.trim() !== "") {
            payload.password = form.value.password.trim();
          }
  
          const response = await fetch(`/api/user/current`, {
            method: "PUT",
            credentials: "include",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
          });
  
          if (!response.ok) {
            const errResp = await response.json();
            throw new Error(errResp.error || "Failed to update profile.");
          }
  
          success.value = "Profile updated successfully!";
          // Clear password field after successful completion
          form.value.password = "";
        } catch (err) {
          error.value = err.message;
        } finally {
          loading.value = false;
        }
      };
  
      onMounted(fetchUserInfo);
  
      return {
        form,
        loading,
        error,
        success,
        updateProfile,
      };
    },
  };
  </script>
  <style scoped>
  .user-info-container {
    max-width: 1000px;
    margin: 2em auto;
    padding: 25px 30px;
    background-color: #082852; 
    border-radius: 12px;
    box-shadow: 0 6px 24px rgba(30, 70, 140, 0.3);
    color: #e0e7ff;
    font-family: Arial, sans-serif;
  }
  
  .form-group {
    margin-bottom: 1.2em;
  }
  
  label {
    display: block;
    font-weight: 600;
    margin-bottom: 0.4em;
    color: #90caf9; 
  }
  
  input[type="text"],
  input[type="email"],
  input[type="tel"],
  input[type="password"] {
    width: 100vh;
    padding: 10px 12px;
    border: 1.5px solid #1953b7;
    border-radius: 6px;
    font-size: 1rem;
    background-color: #041c32;
    color: #e0e7ff;
    outline: none;
    transition: border-color 0.2s ease;
  }
  
  input[type="text"]:focus,
  input[type="email"]:focus,
  input[type="tel"]:focus,
  input[type="password"]:focus {
    border-color: #33a7e2;
    background-color: #0d2a61;
  }
  
  button {
    width: 100%;
    padding: 12px 0;
    font-size: 1.1rem;
    font-weight: 700;
    background-color: #33a7e2;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(51, 167, 226, 0.35);
    transition: background-color 0.25s ease;
  }
  
  button:hover:enabled {
    background-color: #1953b7;
  }
  
  button:disabled {
    background-color: #1953b7;
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  .error {
    margin-top: 15px;
    font-weight: 600;
    color: #ff8282; 
  }
  
  .success {
    margin-top: 15px;
    font-weight: 600;
    color: #81c784; 
  }
</style>