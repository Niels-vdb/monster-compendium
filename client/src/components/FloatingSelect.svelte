<script>
	export let selectId;
	export let selectOptions;
	export let labelName;
	export let rowStart;
	export let colStart;
</script>

<div class="relative w-full col-start-{colStart} row-start-{rowStart}">
	<select
		id={selectId}
		name=""
		class="border-1 peer block w-full appearance-none rounded-lg border-gray-300 bg-white px-2.5
    pb-2.5 pt-4 text-sm text-gray-900 focus:border-blue-600 focus:outline-none focus:ring-0"
	>
		<option value="" disabled selected>Choose {labelName}</option>
		{#each selectOptions as creature}
			<option value="option1">{creature}</option>
		{/each}
	</select>
	<label
		for={selectId}
		class="peer-placeholder-shown:top-1/5 absolute start-1 top-4 z-10 origin-[0] -translate-y-4 scale-75 transform px-2
        text-sm text-gray-500 duration-300 peer-placeholder-shown:-translate-y-1/2
        peer-placeholder-shown:scale-100 peer-focus:top-4 peer-focus:-translate-y-4 peer-focus:scale-75
        peer-focus:px-2 peer-focus:text-blue-600 rtl:peer-focus:left-auto rtl:peer-focus:translate-x-1/4"
	>
		{labelName}
	</label>
</div>
