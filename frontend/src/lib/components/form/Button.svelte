<script>
	export let label, width = 'block', type = 'button', color = 'primary';
</script>

<button {type} class="btn btn-{width} {color}" on:click>{label}</button>
