<script lang="ts">
	import userIcon from '../assets/user.svg';

	const creatureSwitch = (event: any) => {
		for (let child of event.target.parentElement.children) {
			child.classList.remove('border-black');
			child.classList.remove('text-black');
			child.classList.add('text-[#B3B3B3]');
		}
		event.target.classList.add('border-black');
		event.target.classList.add('text-black');
	};
</script>

<nav class=" grid h-24 grid-cols-6 items-center justify-items-stretch">
	<div class="col-span-4 col-start-2 flex justify-center">
		<button onclick={creatureSwitch} class="border-b border-black px-5 text-2xl text-black"
			>Enemies</button
		>
		<button onclick={creatureSwitch} class="border-b px-5 text-2xl text-[#B3B3B3]"
			>Non Player Characters</button
		>
		<button onclick={creatureSwitch} class="border-b px-5 text-2xl text-[#B3B3B3]"
			>Player Characters</button
		>
	</div>
	<div
		class="mr-5 grid w-60 grid-cols-8 items-center gap-5 justify-self-end rounded-xl bg-[#9B9B7A] p-2"
	>
		<img src={userIcon} alt="User profile" class="col-span-2 h-10 rounded-full border-black" />
		<div class="col-span-3 col-start-3">
			<p class="text-sm">Name</p>
			<p class="text-sm text-[#5A5A5A]">Role</p>
		</div>
		<button class="col-span-3 col-start-6 rounded-lg bg-[#2C2C2C] p-2 text-white">Logout</button>
	</div>
</nav>
