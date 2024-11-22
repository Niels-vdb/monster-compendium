<script>
	export let textareaId;
	export let textareaName;
	export let extraClass;
</script>

<div class="relative col-span-2 col-start-1 w-full">
	<textarea
		id={textareaId}
		name="description"
		rows="4"
		class="{extraClass} border-1 peer block w-full rounded-lg border-gray-300 bg-white
                px-2.5 pb-2.5 pt-4 text-sm text-gray-900 focus:border-blue-600
                focus:outline-none focus:ring-0"
		placeholder=" "
	></textarea>
	<label
		for={textareaId}
		class="absolute start-2 top-3 z-10 origin-[0] -translate-y-4 scale-75 transform
            px-2 text-sm duration-300 peer-placeholder-shown:top-1/2
            peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-100
            peer-focus:top-3 peer-focus:-translate-y-4 peer-focus:scale-75 peer-focus:px-2
            peer-focus:text-blue-600"
	>
		{textareaName}
	</label>
</div>
