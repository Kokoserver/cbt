<script>
  import Card from '../../lib/components/Card.svelte'
  import FormControl from '../../lib/components/form/FormControl.svelte'
  import Input from '../../lib/components/form/Input.svelte'
  import Label from '../../lib/components/form/Label.svelte'
  import InforText from '../../lib/components/form/InforText.svelte'
  import Button from '../../lib/components/form/Button.svelte'
  import request from '../../lib/config/request'
  import { userEndpoint } from '../../lib/config/urls'
  let userData = { email: '' }
  let formError = { usernameError: '' }

  const register = () => {
    request
      .post(userEndpoint.passwordLink, userData)
      .then((res) => {
        const { data, status } = res
        if (status == 200) {
          alert(data.details)
        }
      })
      .catch((err) => {
        const { status, data } = err
        if (status == 400 || 401) {
          formError.usernameError = data.details
        }
        if (status == 422) {
          formError.statusError = 'invalid information provided'
        }
      })
  }
</script>

<svelte:head>
  <title>password reset</title>
</svelte:head>

<div class=" hero flex justify-center content-center min-h-screen">
  <Card>
    <h1 slot="title">Password reset Form</h1>
    <div slot="body">
      <form action="">
        <FormControl>
          <Label label="Email" />
          <Input type="email" placeholder="Email" bind:value={userData.email} />
          <InforText text={formError.usernameError} color="text-error" />
        </FormControl>
        <FormControl>
          <Button label="submit" type="submit" color="btn-primary" />
        </FormControl>
      </form>
    </div>
  </Card>
</div>
