<script lang="ts">
	import plusIcon from '../assets/plus.svg';
	import CreatureModal from './CreatureModal.svelte';
	import CreatureRow from './CreatureRow.svelte';

	let isModalOpen = false;
	let creatureId: any = null;

	const openModal = (id = null) => {
		creatureId = id;
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
			<CreatureRow creatureName="Gold Dragon" creatureId="1" {openModal} />
			<CreatureRow creatureName="Red Dragon" creatureId="2" {openModal} />
			<CreatureRow creatureName="Blue Dragon" creatureId="3" {openModal} />
		</div>
	</div>

	<button
		on:click={() => (isModalOpen = true)}
		class="bg-secondary row-start-10 grid grid-cols-10 items-center rounded-xl"
	>
		<p class="col-start-2 col-end-9 overflow-visible text-center text-lg">Add a new creature</p>
		<img src={plusIcon} alt="Add a new creature" class="col-start-10 h-8" />
	</button>

	{#if isModalOpen}
		<CreatureModal bind:isModalOpen bind:creatureId />
	{/if}
</div>
