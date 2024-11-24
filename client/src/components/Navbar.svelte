<script lang="ts">
	import userIcon from '../assets/user.svg';
	import UserDropdown from './UserDropdown.svelte';

	let dropdownIsOpen = false;

	// Function to toggle the dropdown
	const toggleDropdown = () => {
		dropdownIsOpen = !dropdownIsOpen;
	};

	const creatureSwitch = (event: any) => {
		for (let child of event.target.parentElement.children) {
			child.classList.remove('border-black');
			child.classList.remove('text-black');
			child.classList.add('text-textTertiary');
		}
		event.target.classList.remove('text-textTertiary');
		event.target.classList.add('border-black');
		event.target.classList.add('text-black');
	};
</script>

<nav class="row-span-1 grid h-24 grid-cols-6 items-center justify-items-stretch">
	<div class="col-span-4 col-start-2 flex justify-center">
		<button on:click={creatureSwitch} class="border-b border-black px-5 text-xl text-black"
			>Enemies</button
		>
		<button on:click={creatureSwitch} class="text-textTertiary border-b px-5 text-xl"
			>Non-Player Characters</button
		>
		<button on:click={creatureSwitch} class="text-textTertiary border-b px-5 text-xl"
			>Player Characters</button
		>
	</div>
	<div
		class="bg-secondary mr-5 grid w-60 grid-cols-8 items-center gap-5 justify-self-end rounded-xl p-2"
	>
		<button
			on:click={toggleDropdown}
			class="col-span-2 rounded-full"
			aria-haspopup="true"
			aria-expanded={dropdownIsOpen}
		>
			<img src={userIcon} alt="User profile" class=" h-10" />
		</button>
		<div class="col-span-3 col-start-3">
			<p class="text-sm">Name</p>
			<p class="text-text-secondary text-sm">Role</p>
		</div>
		<button class="bg-primary col-span-3 col-start-6 rounded-lg p-2">Logout</button>
	</div>
</nav>

<UserDropdown {dropdownIsOpen} {toggleDropdown} />
