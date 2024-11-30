<script lang="ts">
	import cloudIcon from '../assets/cloud.svg';
	import crossIcon from '../assets/cross.svg';
	export let inputId;

	let previewUrl: string | null = null;
	let fileInput: HTMLInputElement | null = null;

	const show = (e: any) => {
		const file = e.target.files[0];
		if (file) {
			const reader = new FileReader();
			reader.onload = () => {
				previewUrl = reader.result as string;
			};
			reader.readAsDataURL(file);
		}
	};

	const removeImage = () => {
		previewUrl = null;
		if (fileInput) {
			fileInput.value = '';
		}
	};
</script>

<div class="col-span-4 col-start-1 flex h-5/6 w-full items-center justify-center">
	<label
		for={inputId}
		class="relative flex h-32 w-full cursor-pointer flex-col items-center justify-center
                rounded-lg border-2 border-dashed border-gray-300 bg-white hover:bg-gray-100"
	>
		<div class="flex flex-col items-center justify-center pb-6 pt-5">
			{#if previewUrl}
				<img src={previewUrl} alt="Preview" class="mb-2 h-20 rounded" />
				<button type="button" on:click={removeImage} class="absolute right-2 top-2 z-50 px-2 py-1">
					<img src={crossIcon} alt="Remove" class="h-5" />
				</button>
			{:else}
				<img src={cloudIcon} alt="" class="mb-2 h-7" />
				<p class="mb-2 text-sm text-gray-500 dark:text-gray-400">
					<span class="font-semibold">Click to upload</span> or drag and drop
				</p>
				<p class="text-xs text-gray-500 dark:text-gray-400">SVG, PNG, JPG or GIF</p>
			{/if}
		</div>
		<input
			bind:this={fileInput}
			on:change={show}
			type="file"
			class="hidden"
			accept=".jpg, .jpeg, .png, .svg, .gif"
			id={inputId}
		/>
	</label>
</div>
