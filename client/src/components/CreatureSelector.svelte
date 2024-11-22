<script>
	import plusIcon from '../assets/plus.svg';
	import editIcon from '../assets/edit.svg';
	import CreatureModal from './CreatureModal.svelte';

	let isModalOpen = false;

	const openModal = () => {
		isModalOpen = true;
	};
</script>

<div class="col-span-2 grid grid-rows-10 gap-4">
	<div class="bg-secondary row-span-9 flex flex-col items-center overflow-scroll rounded-xl">
		<input
			type="search"
			name="creature-search"
			id="creature-search"
			class="bg-primary m-5 w-10/12 rounded-full text-black placeholder-black"
			placeholder="Search for creature..."
		/>
		<div class="flex w-10/12 flex-col items-center">
			<h2 class="mb-2 w-5/6 border-b-2 border-black text-center text-xl">Dragons</h2>
			<div class="flex w-5/6 items-center justify-between">
				<span class="cursor-pointer text-lg">Gold Dragon</span>
				<img src={editIcon} alt="Edit creature" class="h-4 cursor-pointer" />
			</div>
			<div class="flex w-5/6 items-center justify-between">
				<span class="cursor-pointer text-lg">Red Dragon</span>
				<img src={editIcon} alt="Edit creature" class="h-4 cursor-pointer" />
			</div>
			<div class="flex w-5/6 items-center justify-between">
				<span class="cursor-pointer text-lg">Blue Dragon</span>
				<img src={editIcon} alt="Edit creature" class="h-4 cursor-pointer" />
			</div>
		</div>
	</div>

	<button
		on:click={openModal}
		class="bg-secondary row-start-10 grid grid-cols-10 items-center rounded-xl"
	>
		<p class="col-start-2 col-end-9 overflow-visible text-center text-lg">Add a new creature</p>
		<img src={plusIcon} alt="Add a new creature" class="col-start-10 h-8" />
	</button>

	{#if isModalOpen}
		<CreatureModal bind:isModalOpen />
	{/if}
</div>
