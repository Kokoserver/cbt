<script>
// @ts-nocheck

  import { Navigate } from 'svelte-router-spa'
  import Card from '../../../lib/components/Card.svelte'
  import FormControl from '../../../lib/components/form/FormControl.svelte'
  import Input from '../../../lib/components/form/Input.svelte'
  import Label from '../../../lib/components/form/Label.svelte'
  import InforText from '../../../lib/components/form/InforText.svelte'
  import Button from '../../../lib/components/form/Button.svelte'
  import request from '../../../lib/config/request'
  import {examEndpoint} from "../../../lib/config/urls"
  let question = []
  let candidate = []
  let duration  = 0
  let title = ""
  let formError = ""
  const createExam = () => {
    const form = new FormData()
  form.append("candidate", candidate.files[0])
  form.append("question", question.files[0])
  form.append("duration", duration )
  form.append("title", title )
    request
      .post(examEndpoint.create, form, {headers:{'Content-Type':'multipart/form-data'}})
      .then((exam) => {
        const { status } = exam
        if (status === 201) {
          alert('exam created successfully')
            title = ""
            question = ''
            candidate = ''
            duration = ''
        }
      })
      .catch((error) => {
      const { data, status} = error.response
      if(status === 400){
        formError == data.ExamExist
      }
      alert("error creating new exam")
      })
  }
</script><svelte:head>
  <title>create new exam</title>
</svelte:head>

<div class=" hero flex justify-center content-center min-h-screen">
  <Card>
    <h1 slot="title">Add new course</h1>
    <div slot="body">
      <form on:submit|preventDefault={createExam}>
        <FormControl>
          <Label label="Title" />
          <Input
            type="text"
            placeholder="title"
            bind:value={title} />
          <InforText text={formError} color="text-error" />
        </FormControl>
        <FormControl>
          <Label label="duration" />
          <Input
            type="number"
            placeholder="duration" bind:value={duration} />
          <InforText text={formError} color="text-error" />
        </FormControl>

        <FormControl>
          <Label label="candidate" />
          <input type="file" accept=".csv" required class="input input" id="candidate" name="" bind:this={candidate}>
        </FormControl>

        <FormControl>
          <Label label="questions" />
          <input type="file" accept=".csv" required class="input input" id="questions" name="questions" bind:this={question}>
        </FormControl>
       
        <FormControl>
          <Button label="submit" type="submit" color="btn-primary" />
        </FormControl>
      </form>
    </div>
  </Card>
</div>
