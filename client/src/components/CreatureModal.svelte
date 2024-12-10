<script lang="ts">
	// @ts-nocheck

	import FloatingInput from '../components/FloatingInput.svelte';
	import FloatingMultiSelect from '../components/FloatingMultiSelect.svelte';
	import FloatingSelect from '../components/FloatingSelect.svelte';
	import FloatingTextarea from '../components/FloatingTextarea.svelte';
	import ImageInput from '../components/ImageInput.svelte';
	import crossIcon from '../assets/cross.svg';
	import InputToggle from '../components/InputToggle.svelte';

	let {
		creatureId = $bindable(),
		modalOpen = $bindable()
	}: { creatureId: string | null; modalOpen: boolean } = $props();

	let creatureName: string | null = $state(null);
	let creatureInformation: string | null = $state(null);
	let creatureDescription: string | null = $state(null);
	let creatureAC: number | null = $state(null);
	let creatureSize: number | null = $state(null);
	let creatureKind: number | null = $state(null);
	let creatureType: number | null = $state(null);
	let creatureWalkingSpeed: number | null = $state(null);
	let creatureSwimmingSpeed: number | null = $state(null);
	let creatureClimbingSpeed: number | null = $state(null);
	let creatureFlyingSpeed: number | null = $state(null);
	let creatureRace: number | null = $state(null);
	let creatureSubrace: number | null = $state(null);
	let creatureAlive: boolean | null = $state(true);
	let creatureClass: number[] = $state([]);
	let creatureSubclass: number[] = $state([]);
	let creatureImmunities: number[] = $state([]);
	let creatureVulnerabilities: number[] = $state([]);
	let creatureResistances: number[] = $state([]);
	let creatureAdvantages: number[] = $state([]);
	let creatureDisadvantages: number[] = $state([]);

	const saveCreature = () => {
		const creatureData = {
			creatureName: creatureName,
			creatureAlive: creatureAlive,
			creatureAC: creatureAC,
			creatureSize: creatureSize,
			creatureKind: creatureKind,
			creatureType: creatureType,
			creatureWalkingSpeed: creatureWalkingSpeed,
			creatureSwimmingSpeed: creatureSwimmingSpeed,
			creatureClimbingSpeed: creatureClimbingSpeed,
			creatureFlyingSpeed: creatureFlyingSpeed,
			creatureRace: creatureRace,
			creatureSubrace: creatureSubrace,
			creatureClass: creatureClass,
			creatureSubclass: creatureSubclass,
			creatureInformation: creatureInformation,
			creatureDescription: creatureDescription,
			creatureImmunities: creatureImmunities,
			creatureVulnerabilities: creatureVulnerabilities,
			creatureResistances: creatureResistances,
			creatureAdvantages: creatureAdvantages,
			creatureDisadvantages: creatureDisadvantages
		};

		console.log(creatureData);
	};

	document.addEventListener('keydown', (e) => {
		e = e || window.event;
		if (e.keyCode == 27) {
			closeModal();
		}
	});

	const closeModal = () => {
		modalOpen = false;
	};

	// These values will be fetched dynamically
	const creatureKinds = [
		{ value: 1, name: 'Enemy' },
		{ value: 2, name: 'Non-Player Character' },
		{ value: 3, name: 'Player Character' }
	];
	const creatureTypes = [
		{ value: 1, name: 'Aberration' },
		{ value: 2, name: 'Beast' },
		{ value: 3, name: 'Celestial' },
		{ value: 4, name: 'Construct' },
		{ value: 5, name: 'Dragon' }
	];
	const sizes = [
		{ value: 1, name: 'Tiny' },
		{ value: 2, name: 'Small' },
		{ value: 3, name: 'Medium' },
		{ value: 4, name: 'Large' },
		{ value: 5, name: 'Gargantuan' }
	];
	const races = [
		{ value: 1, name: 'Human' },
		{ value: 2, name: 'Orc' },
		{ value: 3, name: 'Elf' }
	];
	const subraces = [
		{ value: 1, name: 'High' },
		{ value: 2, name: 'Wood' },
		{ value: 3, name: 'Sea' }
	];
	const classes = [
		{ value: 1, name: 'Barbarian' },
		{ value: 2, name: 'Wizard' },
		{ value: 3, name: 'Fighter' }
	];
	const subclasses = [
		{ value: 1, name: 'Champion' },
		{ value: 2, name: 'Eldrich Knight' },
		{ value: 3, name: 'Battle Master' }
	];
	const attributes = [
		{ value: 1, name: 'Acrobatics' },
		{ value: 2, name: 'Animal Handling' },
		{ value: 3, name: 'Arcana' },
		{ value: 4, name: 'Athletics' },
		{ value: 5, name: 'Attack rolls' }
	];
	const damageTypes = [
		{ value: 1, name: 'Acid' },
		{ value: 2, name: 'Bludgeoning' },
		{ value: 3, name: 'Cold' },
		{ value: 4, name: 'Fire' },
		{ value: 5, name: 'Force' }
	];

	if (creatureId) {
		// Create fetch to get creature info.
		creatureName = 'Gold Dragon';
		creatureAlive = false;
		creatureAC = 17;
		creatureSize = 1;
		creatureKind = 2;
		creatureType = 3;
		creatureWalkingSpeed = 40;
		creatureSwimmingSpeed = 20;
		creatureClimbingSpeed = 20;
		creatureFlyingSpeed = 40;
		creatureRace = 1;
		creatureSubrace = 2;
		creatureClass = [1, 2];
		creatureSubclass = [2, 3];
		creatureImmunities = [1, 2];
		creatureResistances = [3, 4];
		creatureVulnerabilities = [4, 5];
		creatureAdvantages = [1, 2];
		creatureDisadvantages = [3, 4];
		creatureInformation =
			'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Voluptate numquam, dolore quasi, recusandae ducimus molestiae vero molestias tenetur laborum facilis repellat explicabo rem voluptatem consequuntur.';
		creatureDescription =
			'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Optio, perspiciatis.';
	}
</script>

<dialog open={modalOpen} class="h-5/6 w-5/6 overflow-scroll rounded-xl bg-[#f0ead6]">
	<div class="grid grid-cols-3">
		<h1 class="col-start-2 p-2 pt-4 text-center text-xl font-medium">
			{creatureId ? 'Editing Creature' : 'Adding New Creature'}
		</h1>
		<button onclick={closeModal} class="col-start-3 m-3 justify-self-end">
			<img src={crossIcon} alt="Close modal" class="h-6" />
		</button>
	</div>
	<div
		class="mx-auto my-0 grid w-full grid-cols-6 grid-rows-6 place-items-center justify-items-center gap-2 px-7"
	>
		<div class="col-span-4 col-start-1 row-start-1 flex w-full flex-col gap-2">
			<div class="grid grid-cols-4">
				<FloatingInput
					bind:value={creatureName}
					inputType="text"
					inputId="name"
					labelName="Name"
					required={true}
					extraClass="col-span-3"
				/>
				<InputToggle bind:checked={creatureAlive} />
			</div>
			<div class="grid grid-cols-2 gap-2">
				<FloatingInput
					bind:value={creatureAC}
					inputType="number"
					inputId="armour-class"
					labelName="Armour Class"
				/>
				<FloatingSelect
					bind:value={creatureSize}
					selectId="size"
					selectOptions={sizes}
					labelName="Size"
				/>
			</div>
		</div>

		<div class="col-span-2 col-start-5 row-start-1 flex w-full flex-col gap-2">
			<FloatingSelect
				bind:value={creatureKind}
				selectId="creatureKind"
				selectOptions={creatureKinds}
				labelName="Creature Kind"
			/>
			<FloatingSelect
				bind:value={creatureType}
				selectId="creatureType"
				selectOptions={creatureTypes}
				labelName="Creature Type"
			/>
		</div>

		<ImageInput inputId="image" />

		<div class="col-span-2 col-start-5 row-start-2 flex flex-col gap-2">
			<div class="flex gap-2">
				<FloatingInput
					bind:value={creatureWalkingSpeed}
					inputType="number"
					inputId="walking-speed"
					labelName="Walking Speed"
				/>
				<FloatingInput
					bind:value={creatureSwimmingSpeed}
					inputType="number"
					inputId="swimming-speed"
					labelName="Swimming Speed"
				/>
			</div>
			<div class="flex gap-2">
				<FloatingInput
					bind:value={creatureClimbingSpeed}
					inputType="number"
					inputId="climbing-speed"
					labelName="Climbing Speed"
				/>
				<FloatingInput
					bind:value={creatureFlyingSpeed}
					inputType="number"
					inputId="flying-speed"
					labelName="Flying Speed"
				/>
			</div>
		</div>

		<div class="col-span-2 col-start-1 row-start-3 flex w-full flex-col gap-2">
			<FloatingMultiSelect
				bind:value={creatureClass}
				selectId="class"
				selectOptions={classes}
				labelName="Class"
			/>
		</div>
		<div class="col-span-2 col-start-3 row-start-3 flex w-full flex-col gap-2">
			<FloatingMultiSelect
				bind:value={creatureSubclass}
				selectId="subclass"
				selectOptions={subclasses}
				labelName="Subclass"
			/>
		</div>

		<div class="col-span-2 col-start-5 row-start-3 mb-7 flex w-full flex-col gap-2">
			<FloatingSelect
				bind:value={creatureRace}
				selectId="race"
				selectOptions={races}
				labelName="Race"
			/>
			<FloatingSelect
				bind:value={creatureSubrace}
				selectId="subrace"
				selectOptions={subraces}
				labelName="Subrace"
			/>
		</div>
		<FloatingTextarea
			bind:value={creatureInformation}
			textareaId="information"
			textareaName="Information"
		/>
		<FloatingTextarea
			bind:value={creatureDescription}
			textareaId="description"
			textareaName="Description"
		/>

		<div class="col-span-2 col-start-1 row-start-5 w-full">
			<FloatingMultiSelect
				bind:value={creatureImmunities}
				selectId="immunities"
				selectOptions={damageTypes}
				labelName="Immunities"
			/>
		</div>
		<div class="col-span-2 col-start-3 row-start-5 w-full">
			<FloatingMultiSelect
				bind:value={creatureResistances}
				selectId="resistances"
				selectOptions={damageTypes}
				labelName="Resistances"
			/>
		</div>
		<div class="col-span-2 col-start-5 row-start-5 w-full">
			<FloatingMultiSelect
				bind:value={creatureVulnerabilities}
				selectId="vulnerabilities"
				selectOptions={damageTypes}
				labelName="Vulnerabilities"
			/>
		</div>
		<div class="col-span-2 col-start-1 row-start-6 w-full">
			<FloatingMultiSelect
				bind:value={creatureAdvantages}
				selectId="advantages"
				selectOptions={attributes}
				labelName="Advantages"
			/>
		</div>
		<div class="col-span-2 col-start-3 row-start-6 w-full">
			<FloatingMultiSelect
				bind:value={creatureDisadvantages}
				selectId="disadvantages"
				selectOptions={attributes}
				labelName="Disadvantages"
			/>
		</div>
		<div class="col-span-2 col-start-5 row-start-6 mt-2 flex h-full w-full flex-col gap-2">
			<button onclick={closeModal} class="h-1/3 items-center rounded-xl border bg-white"
				>Close</button
			>
			<button onclick={saveCreature} class=" h-1/3 items-center rounded-xl border bg-white"
				>Save</button
			>
		</div>
	</div>
</dialog>
