<script>
	export let action = undefined;
	export let value;
</script>

<button onclick={action} class="bg-secondary w-full items-center rounded-xl border p-3"
	>{value}</button
>
