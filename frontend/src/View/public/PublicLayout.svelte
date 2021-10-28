<script>
  import { Route } from 'svelte-router-spa'
  // import TopHeader from './top_header.svelte'
  export let currentRoute
  const params = {}
</script>

<style>
  section {
    background-image: url('/image/lagos-techie-IgUR1iX0mqM-unsplash.jpg');
    background-size: cover;
    background-position: center center;
    object-fit: cover;
  }
</style>

<svelte:head>
  <title>welcome to wokisearch</title>
</svelte:head>
<section class="hero flex justify-center content-center min-h-screen">
  <Route {currentRoute}/>
</section>

