<script>
  export let placeholder = '',
    value,
    option = []
</script>

<select class="select input-bordered mt-3" bind:value>
  <option disabled selected>{placeholder}</option>
  {#each option as op}
    <option>{op}</option>
  {/each}
</select>
