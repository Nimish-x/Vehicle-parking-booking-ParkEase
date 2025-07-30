<script>
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <!-- <div class="container text-center mt-5">
    <div class="jumbotron">
      <h1 class="display-4">Welcome to ParkEase Vehicle Parking</h1>
      <h3 class="lead">Your journey ends here.</h3>
      <hr class="my-4">
      <RouterLink to='/login' class="btn btn-primary btn-lg">Get Started</RouterLink>
    </div>
  </div> -->
  <div id="app-flex">
    <RouterView />
  </div>
</template>

<style scoped>
/* Add this in your main App.vue or dashboard wrapper */


</style>
