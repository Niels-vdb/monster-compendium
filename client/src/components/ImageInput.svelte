<script>
	// @ts-nocheck

	import cloudIcon from '../assets/cloud.svg';
	export let inputId;

	const show = (e) => {
		console.log(e.target.files);
	};
</script>

<div class="col-span-2 col-start-1 flex h-5/6 w-full items-center justify-center">
	<label
		for={inputId}
		class="flex h-32 w-full cursor-pointer flex-col items-center justify-center rounded-lg
                border-2 border-dashed border-gray-300 bg-white hover:bg-gray-100"
	>
		<div class="flex flex-col items-center justify-center pb-6 pt-5">
			<img src={cloudIcon} alt="" class="mb-2 h-7" />
			<p class="mb-2 text-sm text-gray-500 dark:text-gray-400">
				<span class="font-semibold">Click to upload</span> or drag and drop
			</p>
			<p class="text-xs text-gray-500 dark:text-gray-400">SVG, PNG, JPG or GIF (MAX. 800x400px)</p>
		</div>
		<input
			on:change={show}
			type="file"
			class="hidden"
			accept=".jpg, .jpeg, .png, .svg, .gif"
			id={inputId}
		/>
	</label>
</div>
