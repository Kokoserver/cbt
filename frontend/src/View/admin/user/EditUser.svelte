<script>
  import { navigateTo } from 'svelte-router-spa'
  import Card from '../../../lib/components/Card.svelte'
  import FormControl from '../../../lib/components/form/FormControl.svelte'
  import Input from '../../../lib/components/form/Input.svelte'
  import Label from '../../../lib/components/form/Label.svelte'
  import InforText from '../../../lib/components/form/InforText.svelte'
  import Button from '../../../lib/components/form/Button.svelte'
  import request, { userBaseUrl } from '../../../lib/config/request'
  import { userEndpoint } from '../../../lib/config/urls'
  import { onMount } from 'svelte'
  export let currentRoute = {}
  let id = currentRoute.namedParams.id
  onMount(() => {
    request
      .get(`${userBaseUrl}/${id}`)
      .then((user) => {
        const { data, status } = user
        if (status === 200) {
          userData = data
        }
      })
      .catch((error) => {
        const { data, status } = error.response
        if (status === 401) {
          alert(data.AuthError)
        }
        if (status === 404) {
          alert(data.NotFound)
          navigateTo('/admin/user/')
        }
      })
  })

  let userData = {}
  let formError = {
    firstnameError: '',
    lastnameError: '',
    emailError: ''
  }

  const update = () => {
    request
      .put(userEndpoint.update, userData)
      .then((res) => {
        const { data, status } = res
        if (status == 200) {
          alert(data.message)
          navigateTo('/admin/user')
        }
      })
      .catch((err) => {
        const { status, data } = err.response
        if (status == 400) {
          const { message } = data.content || data
          formError.firstnameError = message.firstname || ''
          formError.lastnameError = message.lastname || ''
          formError.emailError = message.email || ''
        }
        if (status == 404) {
          formError.statusError = data.content
        }
        if (status == 401) {
          formError.statusError = data.AuthError
        }
      })
  }
</script>

<svelte:head>
  <title>Edit use</title>
</svelte:head>
<div class="hero my-16">
  <Card>
    <h1 slot="title">Update user details</h1>
    <div slot="body">
      <form on:submit|preventDefault={update}>
        <FormControl>
          <Label label="First name" />
          <Input
            type="text"
            placeholder="firstname"
            bind:value={userData.firstname} />
          <InforText text={formError.firstnameError} color="text-error" />
        </FormControl>
        <FormControl>
          <Label label="Last name" />
          <Input
            type="text"
            placeholder="Lastname"
            bind:value={userData.lastname} />
          <InforText text={formError.lastnameError} color="text-error" />
        </FormControl>
        <FormControl>
          <Label label="Email" />
          <Input type="email" placeholder="Email" bind:value={userData.email} />
          <InforText text={formError.emailError} color="text-error" />
        </FormControl>
        <FormControl>
          <Button label="submit" type="submit" color="btn-primary" />
        </FormControl>
      </form>
    </div>
  </Card>
</div>
