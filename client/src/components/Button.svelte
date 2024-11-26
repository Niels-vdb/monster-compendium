<script lang="ts">
	// Props with types and default values
	export let action: (() => void) | undefined = undefined;
	export let value: string = 'Button';
	export let disabled: boolean = false;
</script>

<button
	onclick={action}
	class="bg-secondary hover:bg-primary w-full items-center rounded-xl border p-3"
	{disabled}
>
	{value}
</button>
