<script>
  import { onMount } from 'svelte'
  import { examEndpoint } from '../../../lib/config/urls'
  import request from '../../../lib/config/request'

  let examData = [{}]
  let error = ''
  onMount(() => {
    request
      .get(examEndpoint.exam)
      .then((res) => {
        const { data, status } = res
        if (status == 200) {
          examData = data
        }
      })
      .catch((err) => {
        const { status, data } = err
        if (status == 404 || 401 || 422) {
          error = data.message
          // alert(error)
        }
      })
  })

  const deleteexam = (id) => {
    request
      .delete(`${examEndpoint.exam}/${id}`)
      .then((data) => {
        if (data.status == 204) {
          alert('exam was deleted successfully')
          window.location.reload()
        }
      })
      .catch((error) => {
        alert('error deleting exam')
        window.location.href = '/admin/exam/'
      })
  }

  const downloadResult = (id) => {
    request
      .get(`${examEndpoint.exam}/${id}/result`, {
        responseType: 'arraybuffer',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then((res) => {
        if (res.status == 200) {
          const type = res.headers['content-type']
          const blob = new Blob([res.data], {
            type: type,
          })
          const link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = 'exam_result.csv'
          link.click()
          alert('result was dowloaded successfully')
        }
      })
      .catch((error) => {
        alert('error downloading result exam')
        window.location.href = '/admin/exam/'
      })
  }
</script>

<div class="overflow-x-auto">
  <table class="table w-full table-zebra">
    <thead>
      <tr>
        <th />
        <th>Title</th>
        <th>duration</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      {#if examData[0] === {}}
        <h1>No exam is found</h1>
      {:else}
        {#each examData as exam, index}
          <tr>
            <th>{index + 1}</th>
            <td>{exam.title}</td>
            <td>{exam.duration}</td>
            <td class="space-x-3">
              <a href="/admin/exam/edit/{exam.id}" class="text-primary">edit</a>
              <button
                class="link text-error"
                on:click={() => deleteexam(exam.id)}>
                delete
              </button>
              <button
                class="link text-success"
                on:click={() => downloadResult(exam.id)}>
                download result
              </button>
            </td>
          </tr>
        {/each}
      {/if}
    </tbody>
  </table>
</div>
