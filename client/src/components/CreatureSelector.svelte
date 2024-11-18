<script>
	import plusIcon from '../assets/plus.svg';
</script>

<div class="col-span-2 grid grid-rows-10 gap-4">
	<div class="row-span-9 flex flex-col items-center overflow-scroll rounded-xl bg-[#9B9B7A]">
		<input
			type="text"
			name="creature-search"
			id="creature-search"
			class="m-5 w-10/12 rounded-full bg-[#797D62] text-[#000] placeholder-black"
			placeholder="Search for creature..."
		/>
		<div class="flex w-10/12 flex-col items-center">
			<h2 class="mb-2 w-5/6 border-b-2 border-black text-center text-xl">Dragons</h2>
			<span class="w-5/6 cursor-pointer text-left text-lg">Gold Dragon</span>
			<span class="w-5/6 cursor-pointer text-left text-lg">Red Dragon</span>
			<span class="w-5/6 cursor-pointer text-left text-lg">Blue Dragon</span>
		</div>
	</div>

	<div class="row-start-10 flex cursor-pointer items-center justify-evenly rounded-xl bg-[#9B9B7A]">
		<p class="text-lg">Add a new creature</p>
		<img src={plusIcon} alt="Add a new creature" class="h-8" />
	</div>
</div>
