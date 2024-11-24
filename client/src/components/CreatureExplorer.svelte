<script lang="ts">
	import noImage from '../assets/image.svg';

	type CreatureAttributes = {
		'Armour Class': number;
		'Creature Type': string;
		Alive: string;
		Race: string;
		Subrace: string;
		Class: string;
		Subclass: string;
		'Walking Speed': number;
		'Swimming Speed': number;
		'Climbing Speed': number;
		'Flying Speed': number;
		Immunities: string[];
		Resistances: string[];
		Vulnerabilities: string[];
		Advantages: string[];
		Disadvantages: string[];
	};

	let creatureAttributes: CreatureAttributes = {
		'Armour Class': 15,
		'Creature Type': 'Humanoid',
		Alive: 'Yes',
		Race: 'Dwarf',
		Subrace: 'Duergar',
		Class: 'Fighter',
		Subclass: 'Champion',
		'Walking Speed': 30,
		'Swimming Speed': 15,
		'Climbing Speed': 15,
		'Flying Speed': 0,
		Immunities: ['Poison', 'Fire'],
		Resistances: ['Slashing'],
		Vulnerabilities: ['Piercing'],
		Advantages: ['Charmed'],
		Disadvantages: ['Dexterity']
	};

	type GeneralAttributes = Omit<
		CreatureAttributes,
		'Immunities' | 'Resistances' | 'Vulnerabilities' | 'Advantages' | 'Disadvantages'
	>;
	type SpecialAttributes = Pick<
		CreatureAttributes,
		'Immunities' | 'Resistances' | 'Vulnerabilities' | 'Advantages' | 'Disadvantages'
	>;

	const {
		Immunities,
		Resistances,
		Vulnerabilities,
		Advantages,
		Disadvantages,
		...generalAttributes
	} = creatureAttributes;

	// Create first and second halves of general attributes
	const generalAttributeKeys = Object.keys(generalAttributes) as (keyof GeneralAttributes)[];
	const halfLength = Math.ceil(generalAttributeKeys.length / 2);

	const generalAttributesFirstHalf = Object.fromEntries(
		generalAttributeKeys.slice(0, halfLength).map((key) => [key, generalAttributes[key]])
	);
	const generalAttributesSecondHalf = Object.fromEntries(
		generalAttributeKeys.slice(halfLength).map((key) => [key, generalAttributes[key]])
	);

	// Special Attributes
	const specialAttributes: SpecialAttributes = {
		Immunities,
		Resistances,
		Vulnerabilities,
		Advantages,
		Disadvantages
	};
</script>

<div class="bg-secondary col-span-4 flex flex-col items-center overflow-auto rounded-xl">
	<img src={noImage} alt="Creature" class="w-4/6 py-6" />
	<div class="mx-10 self-start py-2">
		<h2 class="text-xl">Creature Name</h2>
		<h2 class="text-textSecondary text-xl">Creature Type</h2>
	</div>
	<div class="mx-10 py-2">
		<p class="py-1">
			<strong>Description:</strong> Lorem ipsum dolor sit amet consectetur adipisicing elit. Laboriosam
			vero amet odit autem et excepturi, omnis harum, nihil aliquid necessitatibus quod similique voluptatibus.
			Inventore eligendi accusamus sit, consequuntur facilis, dolores iste officiis ex praesentium reprehenderit
			a debitis laudantium fugit magni! Accusantium laborum sit quis beatae in veniam architecto non
			placeat?
		</p>
		<p class="py-1">
			<strong>Information:</strong> Lorem ipsum dolor sit amet, consectetur adipisicing elit. Vitae quidem
			hic, sunt enim et ipsa reprehenderit beatae eos obcaecati officia suscipit corporis? Dolor hic
			animi libero minima veritatis eligendi in totam quo et odit. Consequatur consectetur cupiditate
			non mollitia adipisci dolorum architecto culpa, rerum eligendi doloremque illo nam sapiente commodi
			et nemo. Maxime voluptates necessitatibus temporibus quas nam natus corporis pariatur voluptatibus
			vitae corrupti! Sequi unde assumenda voluptatum a modi totam explicabo ducimus adipisci asperiores
			rerum, architecto dicta atque molestias aliquid delectus porro tempore sapiente iusto. Assumenda
			obcaecati repudiandae delectus neque nihil, alias quidem aliquid commodi et error dolorum dolore?
		</p>
	</div>
	<div class="w-full">
		<div class="mx-10 my-4 flex gap-24">
			<!-- General stats dived in two tables -->
			<table class="h-min">
				<tbody>
					{#each Object.entries(generalAttributesFirstHalf) as [key, value]}
						<tr>
							<td class="w-40"><strong>{key}</strong>:</td>
							<td>{value}</td>
						</tr>
					{/each}
				</tbody>
			</table>
			<table class="h-min">
				<tbody>
					{#each Object.entries(generalAttributesSecondHalf) as [key, value]}
						<tr>
							<td class="w-40"><strong>{key}</strong>:</td>
							<td>{value}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
		<!-- Advantages and vulnerabilities -->
		<table class="mx-10 my-4">
			<tbody>
				{#each Object.entries(specialAttributes) as [key, value]}
					<tr>
						<td class="w-40"><strong>{key}</strong>:</td>
						<td>{value}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
