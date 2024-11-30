<script lang="ts">
	import plusIcon from '../assets/plus.svg';
	import CreatureModal from './CreatureModal.svelte';
	import CreatureRow from './CreatureRow.svelte';

	import { creatureKind } from '../stores/creatureKind';

	let modalOpen: boolean = false;
	let creatureId: string | null = null;

	const openModal = (id: string | null = null) => {
		creatureId = id;
		modalOpen = true;
	};
</script>

<div class="col-span-2 grid grid-rows-10 gap-4">
	<div class="bg-secondary row-span-10 flex flex-col items-center overflow-scroll rounded-xl">
		<input
			type="search"
			name="creature-search"
			id="creature-search"
			class="bg-primary m-5 w-11/12 rounded-full text-black placeholder-black"
			placeholder="Search for {$creatureKind}..."
		/>
		<div class="flex w-10/12 flex-col items-center">
			<h2 class="mb-2 w-5/6 border-b-2 border-black text-center text-xl">Dragons</h2>
			<CreatureRow creatureName="Gold Dragon" creatureId="1" {openModal} />
			<CreatureRow creatureName="Red Dragon" creatureId="2" {openModal} />
			<CreatureRow creatureName="Blue Dragon" creatureId="3" {openModal} />
		</div>
	</div>

	<button
		on:click={() => openModal()}
		class="bg-secondary row-start-11 grid grid-cols-10 items-center rounded-xl p-2"
	>
		<p class="col-start-2 col-end-10 overflow-visible text-center text-base">
			Add a new {#if $creatureKind == 'Enemies'}
				enemy
			{:else}
				{$creatureKind.substring(0, $creatureKind.length - 1)}
			{/if}
		</p>
		<img src={plusIcon} alt="Add a new {$creatureKind}" class="col-start-10 h-8" />
	</button>

	{#if modalOpen}
		<CreatureModal bind:modalOpen bind:creatureId />
	{/if}
</div>
