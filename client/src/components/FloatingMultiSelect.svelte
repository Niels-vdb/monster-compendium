<script>
	export let selectId;
	export let selectOptions;
	export let labelName;
</script>

<div class="relative row-span-2 w-full">
	<select
		multiple
		name=""
		id={selectId}
		class="border-1 peer block w-full rounded-lg border-gray-300
                bg-white px-2.5 pb-2.5 pt-4 text-sm text-gray-900
                focus:border-blue-600 focus:outline-none focus:ring-0"
	>
		{#each selectOptions as option}
			<option value="option1">{option}</option>
		{/each}
	</select>
	<label
		for={selectId}
		class="absolute start-2 top-3 z-10 origin-[0] -translate-y-4 scale-75
        transform px-2 text-sm text-gray-500 duration-300
        peer-placeholder-shown:top-3 peer-placeholder-shown:translate-y-0
        peer-placeholder-shown:scale-100 peer-focus:top-3 peer-focus:-translate-y-4
        peer-focus:scale-75 peer-focus:px-2 peer-focus:text-blue-600"
	>
		{labelName}
	</label>
</div>
<p id="floating_helper_text" class="mt-2 text-xs text-gray-500 dark:text-gray-400">
	ctrl/cmd + click for multiple
</p>
