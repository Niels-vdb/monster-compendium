<script>
	import caret from '../assets/caret.svg';
	import PartyDropdown from './PartyDropdown.svelte';
	/**
	 * @type {boolean}
	 */
	export let dropdownIsOpen;
	export let toggleDropdown;

	const closeDropdown = () => {
		dropdownIsOpen = false;
	};

	let partyDropdownIsOpen = false;
	const togglePartyDropdown = () => {
		partyDropdownIsOpen = !partyDropdownIsOpen;
	};
</script>

<div
	class="dropdown-content {dropdownIsOpen ? 'open' : ''}  
            z-1000 absolute right-44 top-20 hidden rounded-md
            border border-[#CCC] bg-white shadow-md
    "
	role="menu"
	aria-hidden={!dropdownIsOpen}
	on:mouseleave={closeDropdown}
>
	<button
		on:click={togglePartyDropdown}
		class="flex items-center justify-between px-5 py-2.5 hover:bg-[#F0F0F0]"
		aria-haspopup="true"
		aria-expanded={partyDropdownIsOpen}
	>
		<p>Parties</p>
		<img src={caret} alt="Expand to show parties" class="h-4" />
	</button>
	<a href="#" class="flex px-5 py-2.5 no-underline hover:bg-[#F0F0F0]">Settings</a>
</div>

<PartyDropdown {partyDropdownIsOpen} {togglePartyDropdown} />

<style>
	.dropdown-content.open {
		display: block;
	}
</style>
