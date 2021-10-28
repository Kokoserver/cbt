<script>
  import { Route } from 'svelte-router-spa'
  import UserNav from "../../lib/components/layouts/UserNav.svelte"
  export let currentRoute
</script>

<svelte:head>
  <title>User</title>
</svelte:head>
<UserNav/>
<section>
  <Route {currentRoute} />
</section>
