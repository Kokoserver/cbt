<script>
  import { Navigate } from 'svelte-router-spa'
</script>

<style>
  .hero {
    background-image: url('/image/lagos-techie-IgUR1iX0mqM-unsplash.jpg');
  }
</style>

<svelte:head>
  <title>User Dashboard</title>
</svelte:head>

<div class="hero min-h-screen">
  <div class="hero-overlay bg-opacity-60" />
  <div class="text-center hero-content text-neutral-content">
    <div class="max-w-md">
      <h1 class="mb-5 text-4xl font-bold">Welcome to E-exam</h1>
      <p class="mb-5">
        kindly click on the bottom bellow to start examination.
      </p>
      <Navigate to="/user/exam-center">
        <spen class="btn btn-primary bg-primary-focus">Get Started</spen>
      </Navigate>
    </div>
  </div>
</div>
