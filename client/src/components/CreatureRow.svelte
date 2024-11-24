<script>
	import editIcon from '../assets/edit.svg';

	export let creatureId;
	export let creatureName;
	export let openModal;
</script>

<div class="flex w-5/6 items-center justify-between">
	<span class="cursor-pointer text-lg">{creatureName}</span>
	<button on:click={() => openModal(creatureId)}>
		<img src={editIcon} alt="Edit creature" class="h-4" />
	</button>
</div>
