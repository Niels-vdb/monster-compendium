<script>
	// @ts-nocheck

	import FloatingInput from './FloatingInput.svelte';
	import FloatingMultiSelect from './FloatingMultiSelect.svelte';
	import FloatingSelect from './FloatingSelect.svelte';
	import FloatingTextarea from './FloatingTextarea.svelte';
	import ImageInput from './ImageInput.svelte';
	import crossIcon from '../assets/cross.svg';
	import InputToggle from './inputToggle.svelte';

	/**
	 * @type {boolean}
	 */
	export let isModalOpen;

	const closeModal = () => {
		isModalOpen = false;
	};
	const saveCreature = () => {};

	document.addEventListener('keydown', (e) => {
		e = e || window.event;
		if (e.keyCode == 27) {
			isModalOpen = false;
		}
	});

	const creatures = ['Enemy', 'Non-Player Character', 'Player Character'];
	const creatureTypes = ['Aberration', 'Beast', 'Celestial', 'Construct', 'Dragon'];
	const sizes = ['Tiny', 'Small', 'Medium', 'Large'];
	const races = ['Human', 'Orc', 'Elf'];
	const subraces = ['High', 'Wood', 'Sea'];
	const classes = ['Barbarian', 'Wizard', 'Fighter'];
	const subclasses = ['Champion', 'Eldrich Knight', 'Battle Master'];

	const attributes = [
		'Acrobatics',
		'Animal Handling',
		'Arcana',
		'Athletics',
		'Attack rolls',
		'Blinded',
		'Charmed',
		'Charisma',
		'Constitution',
		'Deception',
		'Dexterity',
		'Exhaustion',
		'Frightened'
	];
	const damageTypes = [
		'Acid',
		'Bludgeoning',
		'Cold',
		'Fire',
		'Force',
		'Lightning',
		'Necrotic',
		'Piercing',
		'Poison',
		'Psychic',
		'Radiant',
		'Slashing',
		'Thunder'
	];
</script>

<dialog
	{isModalOpen}
	open={isModalOpen}
	class="h-5/6 w-5/6 overflow-scroll rounded-xl bg-[#f0ead6]"
>
	<div class="grid grid-cols-3">
		<h1 class="col-start-2 p-2 pt-4 text-center text-xl font-medium">Adding New Creature</h1>
		<button on:click={closeModal} class="col-start-3 m-3 justify-self-end">
			<img src={crossIcon} alt="" class="h-6" />
		</button>
	</div>
	<div
		class="mx-auto my-0 grid w-full grid-cols-3 grid-rows-6 place-items-center justify-items-center gap-1 px-7"
	>
		<div class="col-span-2 col-start-1 row-start-1 flex w-full flex-col gap-2">
			<FloatingInput inputType="text" inputId="name" labelName="Name" />
			<div class="col-span-2 grid grid-cols-2 gap-2">
				<FloatingInput inputType="number" inputId="armour-class" labelName="Armour Class" />
				<div class="grid grid-cols-2 gap-4">
					<FloatingSelect selectId="size" selectOptions={sizes} labelName="Size" />
					<InputToggle />
				</div>
			</div>
		</div>
		<ImageInput inputId="image" />
		<FloatingTextarea textareaId="information" textareaName="Information" />
		<FloatingTextarea textareaId="description" textareaName="Description" />

		<div class="col-start-3 row-start-1 flex w-full flex-col gap-2">
			<FloatingSelect selectId="creature" selectOptions={creatures} labelName="Creature" />
			<FloatingSelect
				selectId="creatureType"
				selectOptions={creatureTypes}
				labelName="Creature Type"
			/>
		</div>

		<div class="col-start-3 row-start-2 flex flex-col gap-2">
			<div class="flex gap-2">
				<FloatingInput inputType="number" inputId="walking-speed" labelName="Walking Speed" />
				<FloatingInput inputType="number" inputId="swimming-speed" labelName="Swimming Speed" />
			</div>
			<div class="flex gap-2">
				<FloatingInput inputType="number" inputId="climbing-speed" labelName="Climbing Speed" />
				<FloatingInput inputType="number" inputId="flying-speed" labelName="Flying Speed" />
			</div>
		</div>

		<div class="col-start-3 row-start-3 flex w-full flex-col gap-2">
			<FloatingSelect selectId="race" selectOptions={races} labelName="Race" />
			<FloatingSelect selectId="subrace" selectOptions={subraces} labelName="Subrace" />
		</div>

		<div class="col-start-3 row-start-4 flex w-full flex-col gap-2">
			<FloatingSelect selectId="class" selectOptions={classes} labelName="Class" />
			<FloatingSelect selectId="subclass" selectOptions={subclasses} labelName="Subclass" />
		</div>

		<div class="col-start-1 row-start-5 w-full">
			<FloatingMultiSelect
				selectId="immunities"
				selectOptions={damageTypes}
				labelName="Immunities"
			/>
		</div>
		<div class="col-start-2 row-start-5 w-full">
			<FloatingMultiSelect
				selectId="resistances"
				selectOptions={damageTypes}
				labelName="Resistances"
			/>
		</div>
		<div class="col-start-3 row-start-5 w-full">
			<FloatingMultiSelect
				selectId="vulnerabilities"
				selectOptions={damageTypes}
				labelName="Vulnerabilities"
			/>
		</div>
		<div class="col-start-1 row-start-6 w-full">
			<FloatingMultiSelect
				selectId="advantages"
				selectOptions={attributes}
				labelName="Advantages"
			/>
		</div>
		<div class="col-start-2 row-start-6 w-full">
			<FloatingMultiSelect
				selectId="disadvantages"
				selectOptions={attributes}
				labelName="Disadvantages"
			/>
		</div>
		<div class="col-start-3 row-start-6 mt-2 flex h-full w-full flex-col gap-2">
			<button on:click={closeModal} class="h-1/3 items-center rounded-xl border bg-white"
				>Close</button
			>
			<button on:click={saveCreature} class=" h-1/3 items-center rounded-xl border bg-white"
				>Save</button
			>
		</div>
	</div>
</dialog>
