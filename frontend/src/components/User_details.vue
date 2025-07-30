<template>
    <div class="admin-users">
      <h2>All Registered Users</h2>
  
      <div v-if="loading">Loading users...</div>
      <div v-if="error" class="error">{{ error }}</div>
  
      <table v-if="users.length" class="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Active</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.phone || 'N/A' }}</td>
            <td>{{ user.active ? 'Yes' : 'No' }}</td>
          </tr>
        </tbody>
      </table>
  
      <div v-else>No users found.</div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  
  const users = ref([])
  const loading = ref(false)
  const error = ref('')
  
  const fetchUsers = async () => {
    loading.value = true
    error.value = ''
    try {
      const res = await fetch('/api/admin/users', {
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        },
      })
      if (!res.ok) {
        const errData = await res.json()
        throw new Error(errData.error || 'Failed to fetch users')
      }
      const data = await res.json()
      users.value = data.users
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }
  
  onMounted(fetchUsers)
  </script>
  
  <style scoped>
.admin-users {
  width: 90vw;               
  height: 90vh;              
  margin: 2em auto 0 auto;   
  font-family: Arial, sans-serif;
  background-color: #082852; 
  border-radius: 12px;
  padding: 20px 30px;
  box-shadow: 0 6px 24px rgba(30, 70, 140, 0.3);
  color: #e0e7ff; 
  overflow-y: auto;          
  box-sizing: border-box;    
}

.users-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 15px;
  background-color: #041c32;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(4, 20, 66, 0.6);
  color: #cfd9ff;
}
</style scoped>

<style>
.users-table th,
.users-table td {
  border-bottom: 1px solid #186fa4;
  padding: 10px 14px;
  text-align: left;
  font-size: 1em;
  vertical-align: middle;
}

.users-table th {
  background-color: #1953b7;
  color: #e0e7ff;
  font-weight: 700;
  letter-spacing: 0.5px;
  user-select: none;
}

.users-table tbody tr:hover {
  background-color: rgba(51, 167, 226, 0.15);
  cursor: default;
}

.error {
  color: #ff8282; 
  margin-top: 1em;
  font-weight: 600;
}

@media (max-width: 768px) {
  .admin-users {
    padding: 15px 10px;
  }

  .users-table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }
}
</style>

  