<script lang="ts">
	// @ts-nocheck

	import FloatingInput from '../components/FloatingInput.svelte';
	import FloatingMultiSelect from '../components/FloatingMultiSelect.svelte';
	import FloatingSelect from '../components/FloatingSelect.svelte';
	import FloatingTextarea from '../components/FloatingTextarea.svelte';
	import ImageInput from '../components/ImageInput.svelte';
	import crossIcon from '../assets/cross.svg';
	import InputToggle from '../components/InputToggle.svelte';

	export let isModalOpen: boolean;
	export let creatureId;

	let creatureName;
	let creatureAlive;
	let creatureAC;
	let creatureSize;
	let creatureKind;
	let creatureType;
	let creatureWalkingSpeed;
	let creatureSwimmingSpeed;
	let creatureClimbingSpeed;
	let creatureFlyingSpeed;
	let creatureRace;
	let creatureSubrace;
	let creatureClass;
	let creatureSubclass;
	let creatureInformation;
	let creatureDescription;

	const closeModal = () => {
		isModalOpen = false;

		creatureId = undefined;
	};
	const saveCreature = () => {};

	document.addEventListener('keydown', (e) => {
		e = e || window.event;
		if (e.keyCode == 27) {
			closeModal();
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

	if (creatureId) {
		// Create fetch to get creature info.
		creatureName = 'Gold Dragon';
		creatureAlive = false;
		creatureAC = 17;
		creatureSize = 'Large';
		creatureKind = 'Enemy';
		creatureType = 'Dragon';
		creatureWalkingSpeed = 40;
		creatureSwimmingSpeed = 20;
		creatureClimbingSpeed = 20;
		creatureFlyingSpeed = 40;
		creatureRace = 'Dragon Hatched';
		creatureSubrace = 'Gold';
		creatureClass = 'Artificer';
		creatureSubclass = 'Armourer';
		creatureInformation =
			'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Voluptate numquam, dolore quasi, recusandae ducimus molestiae vero molestias tenetur laborum facilis repellat explicabo rem voluptatem consequuntur.';
		creatureDescription =
			'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Optio, perspiciatis.';
	}

	console.log(creatureAlive);
</script>

<dialog open={isModalOpen} class="h-5/6 w-5/6 overflow-scroll rounded-xl bg-[#f0ead6]">
	<div class="grid grid-cols-3">
		<h1 class="col-start-2 p-2 pt-4 text-center text-xl font-medium">
			{creatureId ? 'Editing Creature' : 'Adding New Creature'}
		</h1>
		<button on:click={closeModal} class="col-start-3 m-3 justify-self-end">
			<img src={crossIcon} alt="Close modal" class="h-6" />
		</button>
	</div>
	<div
		class="mx-auto my-0 grid w-full grid-cols-3 grid-rows-6 place-items-center justify-items-center gap-1 px-7"
	>
		<div class="col-span-2 col-start-1 row-start-1 flex w-full flex-col gap-2">
			<div class="grid grid-cols-6">
				<FloatingInput
					extraClass="col-span-5"
					inputType="text"
					inputId="name"
					labelName="Name"
					value={creatureName}
				/>
				<InputToggle aliveValue={creatureAlive} />
			</div>
			<div class="grid grid-cols-2 gap-2">
				<FloatingInput
					inputType="number"
					inputId="armour-class"
					labelName="Armour Class"
					value={creatureAC}
				/>
				<FloatingSelect
					selectId="size"
					selectOptions={sizes}
					labelName="Size"
					valueId="1"
					bind:valueOption={creatureSize}
				/>
			</div>
		</div>
		<ImageInput inputId="image" />
		<FloatingTextarea
			textareaId="information"
			textareaName="Information"
			value={creatureInformation}
		/>
		<FloatingTextarea
			textareaId="description"
			textareaName="Description"
			value={creatureDescription}
		/>

		<div class="col-start-3 row-start-1 flex w-full flex-col gap-2">
			<FloatingSelect
				selectId="creature"
				selectOptions={creatures}
				labelName="Creature"
				valueId="1"
				valueOption={creatureKind}
			/>
			<FloatingSelect
				selectId="creatureType"
				selectOptions={creatureTypes}
				labelName="Creature Type"
				valueId="1"
				valueOption={creatureType}
			/>
		</div>

		<div class="col-start-3 row-start-2 flex flex-col gap-2">
			<div class="flex gap-2">
				<FloatingInput
					inputType="number"
					inputId="walking-speed"
					labelName="Walking Speed"
					value={creatureWalkingSpeed}
				/>
				<FloatingInput
					inputType="number"
					inputId="swimming-speed"
					labelName="Swimming Speed"
					value={creatureSwimmingSpeed}
				/>
			</div>
			<div class="flex gap-2">
				<FloatingInput
					inputType="number"
					inputId="climbing-speed"
					labelName="Climbing Speed"
					value={creatureClimbingSpeed}
				/>
				<FloatingInput
					inputType="number"
					inputId="flying-speed"
					labelName="Flying Speed"
					value={creatureFlyingSpeed}
				/>
			</div>
		</div>

		<div class="col-start-3 row-start-3 flex w-full flex-col gap-2">
			<FloatingSelect
				selectId="race"
				selectOptions={races}
				labelName="Race"
				valueId="1"
				valueOption={creatureRace}
			/>
			<FloatingSelect
				selectId="subrace"
				selectOptions={subraces}
				labelName="Subrace"
				valueId="1"
				valueOption={creatureSubrace}
			/>
		</div>

		<div class="col-start-3 row-start-4 flex w-full flex-col gap-2">
			<FloatingSelect
				selectId="class"
				selectOptions={classes}
				labelName="Class"
				valueId="1"
				valueOption={creatureClass}
			/>
			<FloatingSelect
				selectId="subclass"
				selectOptions={subclasses}
				labelName="Subclass"
				valueId="1"
				valueOption={creatureSubclass}
			/>
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
