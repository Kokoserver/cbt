<script>
  import { navigateTo, Navigate } from 'svelte-router-spa'
  import { login } from '../../../stores/AdminStore'
  import request from '../../lib/config/request'
  import { userEndpoint } from '../../lib/config/urls'
  import Card from '../../lib/components/Card.svelte'
  import FormControl from '../../lib/components/form/FormControl.svelte'
  import Input from '../../lib/components/form/Input.svelte'
  import Label from '../../lib/components/form/Label.svelte'
  import InforText from '../../lib/components/form/InforText.svelte'
  import Button from '../../lib/components/form/Button.svelte'
  import Details from '../../lib/components/form/Details.svelte'
  let userData = { email: '', password: '' }
  let formError = { emailError: '', paswordError: '' }

  const loginFunction = () => {
    request
      .post(userEndpoint.login, userData)
      .then((user) => {
        const { data, status } = user
        if (status === 200) {
          login(data.user, data.token, true)
          window.location.href = '/admin/dashboard'
        }
        navigateTo('/admin')
      })
      .catch((error) => {
        const { data, status } = error.response
        if (status == 404) {
          formError.emailError = 'account does not exist'
        } else if (status == 400) {
          const { message } = data.message
          formError.usernameError = message.email
          formError.passwordError = message.password
        }
      })
  }
</script>

<svelte:head>
  <title>login</title>
</svelte:head>

<div class=" hero flex justify-center content-center min-h-screen">
  <Card>
    <h1 slot="title">Login Form</h1>
    <div slot="body">
      <form on:submit|preventDefault={loginFunction}>
        <FormControl>
          <Label label="Email" />
          <Input type="email" placeholder="Email" bind:value={userData.email} />
          <InforText text={formError.emailError} color="text-error" />
        </FormControl>
        <FormControl>
          <Label label="Password" />
          <Input
            type="password"
            placeholder="Password"
            bind:value={userData.password} />
          <InforText text={formError.paswordError} color="text-error" />
        </FormControl>
        <FormControl>
          <Details>
            <span class="label-text-alt mr-5">
              Not a student yet?
              <Navigate to="/register">
                <b class="text-primary mr-1">Register</b>
              </Navigate>
            </span>
            <span class="label-text-alt">
              <Navigate to="/forgotpassword">Forgot password?</Navigate>
            </span>
          </Details>
        </FormControl>
        <FormControl>
          <Button label="login" type="submit" color="btn-primary" />
        </FormControl>
      </form>
    </div>
  </Card>
</div>
