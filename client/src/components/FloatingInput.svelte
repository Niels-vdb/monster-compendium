<script>
	export let inputType;
	export let inputId = undefined;
	export let labelName;
	export let value = undefined;
	export let extraClass = undefined;
</script>

<div class="relative {extraClass}">
	<input
		type={inputType}
		name=""
		{value}
		id={inputId}
		min={inputType === 'number' ? '0' : undefined}
		class="border-1 peer block w-full appearance-none self-center rounded-lg border-gray-300 bg-white px-2.5
                pb-2.5 pt-4 text-sm text-gray-900 focus:border-blue-600 focus:outline-none focus:ring-0"
		placeholder=" "
	/>
	<label
		for={inputId}
		class="absolute start-1 top-4 z-10 origin-[0] -translate-y-4 scale-75 transform px-2 text-sm
                duration-300 peer-placeholder-shown:top-1/2 peer-placeholder-shown:-translate-y-1/2
                peer-placeholder-shown:scale-100 peer-focus:top-4 peer-focus:-translate-y-4 peer-focus:scale-75
                peer-focus:px-2 peer-focus:text-blue-600 rtl:peer-focus:left-auto rtl:peer-focus:translate-x-1/4"
		>{labelName}</label
	>
</div>
