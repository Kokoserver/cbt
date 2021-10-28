<script>
	export let value, placeholder, type, required=true;
	function typeAction(node) {
		node.type = type;
	}
</script>


{#if type=="textarea"}
<textarea class="textarea mt-3" placeholder="{placeholder}"  bind:value></textarea>
{:else}
  <input use:typeAction placeholder="{placeholder}"  bind:value class="input input-bordered" required={required}>
{/if}
