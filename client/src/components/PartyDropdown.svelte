<script>
	/**
	 * @type {boolean}
	 */
	export let partyDropdownIsOpen;
	export let togglePartyDropdown;

	const closeDropdown = () => {
		partyDropdownIsOpen = false;
	};
</script>

<div
	class="dropdown-content {partyDropdownIsOpen ? 'open' : ''}  
            z-1000 absolute right-24 top-24 hidden rounded-md
            border border-[#CCC] bg-white shadow-md
    "
	role="menu"
	aria-hidden={!partyDropdownIsOpen}
	on:mouseleave={closeDropdown}
>
	<button class="flex items-center justify-between px-5 py-2.5 hover:bg-[#F0F0F0]">
		<p>Party 1</p>
	</button>
	<button class="flex items-center justify-between px-5 py-2.5 hover:bg-[#F0F0F0]">
		<p>Party 2</p>
	</button>
	<button class="flex items-center justify-between px-5 py-2.5 hover:bg-[#F0F0F0]">
		<p>Party 3</p>
	</button>
	<button class="flex items-center justify-between px-5 py-2.5 hover:bg-[#F0F0F0]">
		<p>Party 4</p>
	</button>
</div>

<style>
	.dropdown-content.open {
		display: block;
	}
</style>
