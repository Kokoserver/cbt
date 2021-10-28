<script>
  import { Navigate, navigateTo } from 'svelte-router-spa'
  import Card from '../../lib/components/Card.svelte'
  import FormControl from '../../lib/components/form/FormControl.svelte'
  import Input from '../../lib/components/form/Input.svelte'
  import Label from '../../lib/components/form/Label.svelte'
  import InforText from '../../lib/components/form/InforText.svelte'
  import Button from '../../lib/components/form/Button.svelte'
  import Details from '../../lib/components/form/Details.svelte'
  import request from '../../lib/config/request'
  import { userEndpoint } from '../../lib/config/urls'
  let userData = {
    firstname: '',
    lastname: '',
    email: '',
    phone: '',
    pasword: '',
    confirmPassword: '',
  }
  let formError = {
    firstnameError: '',
    lastnameError: '',
    emailError: '',
    paswordError: '',
    confirmPasswordError: '',
  }

  const register = () => {
    request
      .post(userEndpoint.register, userData)
      .then((res) => {
        const { data, status } = res
        if (status == 201) {
          alert(data.message)
          navigateTo('/adminLogin')
        }
      })
      .catch((err) => {
        const { status, data } = err.response
        if (status == 400) {
          const { message } = data
          formError.firstnameError = message.firstname || ''
          formError.lastnameError = message.lastname || ''
          formError.emailError = message.email || ''
          formError.paswordError = message.password || ''
          formError.confirmPasswordError = message.confirmPassword || ''
        }
        if (status == 404) {
          formError.statusError = data.Notfound
        }
      })
  }
</script>

<svelte:head>
  <title>Register</title>
</svelte:head>
<div class="hero my-16">
  <Card>
    <h1 slot="title">Registeration Form</h1>
    <div slot="body">
      <form on:submit|preventDefault={register}>
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
          <Label label="Password" />
          <Input
            type="password"
            placeholder="Password"
            bind:value={userData.password} />
          <InforText text={formError.paswordError} color="text-error" />
        </FormControl>
        <FormControl>
          <Label label="Confirm password" />
          <Input
            type="password"
            placeholder="Re-type your password"
            bind:value={userData.confirmPassword} />
          <InforText text={formError.confirmPasswordError} color="text-error" />
        </FormControl>
        <FormControl>
          <Details>
            <span class="label-text-alt mr-5">
              Already a student yet?
              <Navigate to="/login">
                <b class="text-primary mr-1">Login</b>
              </Navigate>
            </span>
          </Details>
        </FormControl>
        <FormControl>
          <Button label="submit" type="submit" color="btn-primary" />
        </FormControl>
      </form>
    </div>
  </Card>
</div>
