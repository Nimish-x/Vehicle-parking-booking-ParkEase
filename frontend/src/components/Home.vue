<script>
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <div class="container text-center mt-5">
    <div class="jumbotron">
      <h1 class="display-4">Welcome to ParkEase Vehicle Parking</h1><br>
      <h3 class="lead">Your journey ends here.</h3><br><br>
      
      <RouterLink to='/login' class="btn btn-primary btn-lg">Get Started</RouterLink>
    </div>
  </div>
  <RouterView />
</template>

<style>
body {
  background: linear-gradient(to bottom, #007bff, #0056b3);
  color: white;
  font-family: Arial, sans-serif;
}

.jumbotron {
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

.display-4 {
  font-weight: bold;
  color: #007bff;
}

.lead {
  font-size: 20px;
  color: #333333;
  text-align: center;
}

.btn-primary {
  background-color: #007bff;
  border: none;
  padding: 12px 20px;
  font-size: 18px;
  transition: all 0.3s ease-in-out;
  display: block;
  margin: auto auto; 
  text-align: center;
}


.btn-primary:hover {
  background-color: #0056b3;
  transform: scale(1.05);
  border-radius: 30%;
}
</style>