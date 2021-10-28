<script>
  import { Navigate, navigateTo } from 'svelte-router-spa'
  import { login } from '../../../stores/candidate'
  import request from '../../lib/config/request'
  import { examEndpoint } from '../../lib/config/urls'
  import Card from '../../lib/components/Card.svelte'
  import FormControl from '../../lib/components/form/FormControl.svelte'
  import Input from '../../lib/components/form/Input.svelte'
  import Label from '../../lib/components/form/Label.svelte'
  import InforText from '../../lib/components/form/InforText.svelte'
  import Button from '../../lib/components/form/Button.svelte'
  import Details from '../../lib/components/form/Details.svelte'
  let userData = { matric_no: '', pasword: '' }
  let formError = { matricError: '' }

  const loginFunction = () => {
    request
      .post(examEndpoint.login, userData)
      .then((user) => {
        if (user.status == 200) {
          const { data, status } = user
          if (status === 200) {
            if (data.user.matric_no) {
              login(data, true)

              window.location.href = "/user/dashboard"
              navigateTo('/user/dashboard')
              formError.matricError = ''
            }
          }
        }
      })
      .catch((error) => {
        const { data, status } = error.response
        console.log(data);
        if (status == 401) {
          formError.matricError = data.message.AuthError || ''
        }
        if (status == 404) {
          formError.matricError = data.message.Notfound || ''
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
          <Label label="Username" />
          <Input
            type="text"
            placeholder="Username"
            bind:value={userData.matric_no} />
          <InforText text={formError.matricError} color="text-error" />
        </FormControl>
        <FormControl>
          <Label label="Password" />
          <Input
            type="password"
            placeholder="Password"
            bind:value={userData.password} />
        </FormControl>
        <FormControl>
          <Details>
            <span class="label-text-alt mr-5" />
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
