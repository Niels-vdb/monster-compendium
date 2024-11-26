<script lang="ts">
	export let checkboxId: string;
	export let checkboxLabel: string;
	export let checked: boolean;
</script>

<label class="text-sm" for={checkboxId}>
	<input id={checkboxId} type="checkbox" bind:checked class="h-4 w-4 rounded" />
	{@html checkboxLabel}
</label>
