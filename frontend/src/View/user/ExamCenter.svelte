<script>
  // @ts-nocheck
  import { navigateTo } from 'svelte-router-spa'
  import request from '../../lib/config/request'
  import { examEndpoint } from '../../lib/config/urls'
  import { Carousel } from 'renderless-svelte'
  import { currectuser, logout } from '../../../stores/candidate'
  const { user, question } = currectuser.user
  let selected = ''
  let results = []

  function add(accumulator, a) {
    return accumulator + a
  }

  const SubmitExam = () => {
    alert('are you sure you want to submit')
    const sum = results.reduce(add, 0)
    request
      .post(`${examEndpoint.score}`, {
        score: sum,
        candidateId: user.matric_no,
      })
      .then((res) => {
        if (res.status == 200) {
          alert('exam has been saved successfully')
          logout()
          window.location.href = '/'
          navigateTo('/')
        }
      })
      .catch((error) => {
        const { data, status } = error.response
        console.log(data)
        if (status == 401) {
          formError.matricError = data.message.Notfound || ''
        }
      })
  }

  function onChange(event) {
    selected = event.target.value
    let index = event.target.dataset.indexNumber
    let ques = question[index]
    if (ques.answer === selected) {
      results[index] = 2
    } else if (ques.answer !== selected) {
      results[index] = 0
    }
  }
</script>

<style>
  #label {
    display: flex;
    align-items: center;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    padding: 0.5rem 0.25rem;
  }
</style>

<svelte:head>
  <title>Examination center</title>
</svelte:head>

<Carousel items={question} let:payload let:controls let:currentIndex>
  <div class="min-h-screen bg-base-200">
    <div class="form-control mb-4 ">
      <p class="font-semibold mb-2 ml-1">
        {currentIndex + 1}. {payload.question}
      </p>
      <label class="cursor-pointer space-x-3" id="label">
        <input
          data-index-number={currentIndex}
          checked={selected === payload.option1}
          on:change={onChange}
          type="radio"
          name={currentIndex}
          value={payload.option1} />
        <span class="label-text">{payload.option1}</span>
      </label>
      <label class="cursor-pointer space-x-3" id="label">
        <input
          data-index-number={currentIndex}
          on:change={onChange}
          type="radio"
          checked={selected === payload.option2}
          name={currentIndex}
          value={payload.option2} />
        <span class="label-text">{payload.option2}</span>
      </label>
      <label class="cursor-pointer space-x-3" id="label">
        <input
          data-index-number={currentIndex}
          checked={selected === payload.option3}
          on:change={onChange}
          type="radio"
          name={currentIndex}
          value={payload.option3} />
        <span class="label-text">{payload.option3}</span>
      </label>
      <label class="cursor-pointer space-x-3" id="label">
        <input
          data-index-number={currentIndex}
          checked={selected === payload.option4}
          on:change|preventDefault={onChange}
          type="radio"
          name={currentIndex}
          value={payload.option4} />
        <span class="label-text">{payload.option4}</span>
      </label>
    </div>
    <div class="flex">
      <button
        disabled={'disabled' && currentIndex == 0}
        class="btn btn-outline btn-wide"
        on:click={controls.previous}>
        Previous
      </button>
      <button class="btn btn-wide" on:click={controls.next}>Next</button>

    </div>
    <button class="btn btn-wide mt-10" on:click={SubmitExam}>Submit</button>
  </div>

</Carousel>
{selected}
