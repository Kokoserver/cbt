<script>
  import { Router } from 'svelte-router-spa'
  import { routes } from './lib/routes/routes'
  import Footer from './lib/components/layouts/Footer.svelte'

  let options = { gaPageviews: true }
</script>

<svelte:head>
  <title>Wokkisearch</title>
</svelte:head>
<main>
  <Router {routes} {options} />
</main>
<Footer />
