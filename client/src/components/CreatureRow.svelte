<script lang="ts">
	import editIcon from '../assets/edit.svg';

	export let creatureId: string;
	export let creatureName: string;
	export let openModal: (id: string) => void;
</script>

<div class="flex w-5/6 items-center justify-between">
	<span class="cursor-pointer text-lg">{creatureName}</span>
	<button on:click={() => openModal(creatureId)}>
		<img src={editIcon} alt="Edit creature" class="h-4" />
	</button>
</div>
