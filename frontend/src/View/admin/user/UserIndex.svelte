<script>
  import { onMount } from 'svelte'
  import { navigateTo } from 'svelte-router-spa'
  import { userStore } from '../../../../stores/userStore'
  import { logout } from '../../../../stores/AdminStore'
  import request from '../../../lib/config/request'
  import { userEndpoint } from '../../../lib/config/urls'
  onMount(() => {
    request
      .get(userEndpoint.allUser)
      .then((res) => {
        const { data, status } = res
        if (status == 200) {
          userStore.set(data)
        }
      })
      .catch((err) => {
        const { status, data } = err.response
        if (status == 404) {
          alert(data.message.NotFound)
        }
        if (status === 401) {
          logout()
          navigateTo('/admin/')
          window.location.href = '/adminLogin'
        }
      })
  })

  let error = ''
  if (error) alert(error)
  const deletUser = (id) => {
    request
      .delete(`${userEndpoint.remove}/${id}`)
      .then((user) => {
        if (user.status === 204) {
          alert('user was deleted successfully')
          window.location.reload()
        }
        window.location.reload()
      })
      .catch((error) => {
        const { data, status } = error.response
        if (status === 404) {
          alert(data.NotFound)
          navigateTo('/admin/user')
        }
        if (status === 400) {
          alert('Invalid details provided')
          navigateTo('/admin/user')
        }
        if (status === 401) {
          alert(data.AuthError)
          logout()
          navigateTo('/admin/user')
        }
      })
  }
</script>

<div class="overflow-x-auto">
  <table class="table w-full table-zebra">
    <thead>
      <tr>
        <th />
        <th>firstname</th>
        <th>lastname</th>
        <th>email</th>
        <th>active</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      {#await $userStore}
        <h1>Loading</h1>
      {:then}
        {#if $userStore[0] === {}}
          <h1>No user is Found</h1>
        {:else}
          {#each $userStore as user, index}
            <tr>
              <th>{index + 1}</th>
              <td>{user.firstname}</td>
              <td>{user.lastname}</td>
              <td>{user.email}</td>
              <td>{user.is_active}</td>
              <td class="space-x-4">
                <a href="/admin/user/edit/{user.id}" class="text-primary">
                  view
                </a>
                <button class="text-error" on:click={() => deletUser(user.id)}>
                  delete
                </button>
              </td>
            </tr>
          {/each}
        {/if}
      {/await}
    </tbody>
  </table>
</div>
