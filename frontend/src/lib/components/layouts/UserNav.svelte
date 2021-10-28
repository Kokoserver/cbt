<script>
  import { navigateTo } from 'svelte-router-spa'
  import {
    currectuser,
    logout as candidateLogout,
  } from '../../../../stores/candidate'
  async function logout() {
    candidateLogout()
    navigateTo('/')
  }
</script>

<div class="navbar mb-2 md:px-12 shadow-md bg-primary text-neutral-content">
  <div class="flex-1 px-2 mx-2">
    <span class="text-2xl font-bold base">
      <a href="/">E-exam</a>
    </span>
  </div>
  <div class="flex-none hidden px-2 mx-2 lg:flex space-x-3">
    <button class="capitalize">
      welcome, {currectuser.user.user.matric_no}
    </button>
    <button on:click={logout} class="btn bg-primary-focus btn-sm rounded-btn">
      logout
    </button>
  </div>
</div>
