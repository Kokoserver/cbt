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
import { onMount } from 'svelte';
import { logout } from '../../../../stores/AdminStore';
    let question
    let candidate
    let duration 
    let title = ""
    let formError = ""
    export let currentRoute = {}
    let id = currentRoute.namedParams.id
    let ExamData = {}
    onMount(()=>{
      request
        .get(`${examEndpoint.exam}/${id}`)
        .then((exam) => {
          const { status } = exam
          if (status === 200) {
            ExamData= exam.data
          }
        })
        .catch((error) => {
        const { data, status} = error.response
        if(status === 400){
          formError == data.ExamExist
        }
        if(status === 404){
         alert("exam not found")
         navigateTo("/admin/exam/")
        }
        alert("error creating new exam")
        navigateTo("/admin/exam/")
        })
    })
    const createExam = () => {
      const form = new FormData()
    form.append("candidate", candidate.files[0])
    form.append("question", question.files[0])
    form.append("duration", ExamData.duration )
    form.append("title", ExamData.title )
      request
        .put(`${examEndpoint.exam}/${id}`, form, {headers:{'Content-Type':'multipart/form-data'}})
        .then((exam) => {
          const { status } = exam
          if (status === 200) {
            alert('exam was updated successfully')
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
        if(status === 401){
          alert("session expire")
          logout()
          navigateTo("/admin")
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
              bind:value={ExamData.title} />
            <InforText text={formError} color="text-error" />
          </FormControl>
          <FormControl>
            <Label label="duration" />
            <Input
              type="number"
              placeholder="duration" bind:value={ExamData.duration} />
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
  