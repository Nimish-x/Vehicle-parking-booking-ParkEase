<template>
    <div id="dashboard-container">
      <nav class="navbar">
        <div class="navbar-brand">ParkEase</div>
        <ul class="navbar-menu">
          <RouterLink to="/" class="btn">Logout</RouterLink>
        </ul>
      </nav>
  
      <div class="dashboard-content">
        <h1 class="display-4">Welcome to your dashboard</h1>
        <p class="lead">Manage your parking with ease</p>
  
        <div class="dashboard-widgets">
          <RouterLink to='/slots_user' class="widget">🚗 Slot availaiblity</RouterLink>
          <RouterLink to='/bookings_user' class="widget">📅 My Bookings</RouterLink>
          <RouterLink to='/user_info' class="widget">👤 Account Info</RouterLink>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'; 
import { RouterLink } from 'vue-router';
  </script>
  
  <style>
  #dashboard-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-40%,-50%);
  max-width: 100vh; 
  margin: auto;
  padding: 60px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
    box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.2);
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
    background-color: #085ba3;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 5px 15px rgba(0, 123, 255, 0.1);
    font-size: 18px;
    font-weight: 500;
    min-width: 200px;
  }
  </style>
  