<script>
	import Button from '../components/Button.svelte';

	const login = () => {
		console.log('click');
	};
</script>

<div class="flex h-dvh w-dvw flex-col items-center justify-center gap-5">
	<h1 class="text-2xl">Creature Compendium</h1>
	<div class="flex h-60 w-96 flex-col justify-center gap-4 rounded-lg border border-black p-5">
		<div>
			<label for="username" class="text-sm">Username</label>
			<input
				type="text"
				id="username"
				class="border-1 peer w-full appearance-none self-center rounded-lg border-gray-300 bg-white px-2.5
                            pb-2.5 text-sm text-gray-900 focus:border-blue-600 focus:outline-none focus:ring-0"
			/>
		</div>
		<div>
			<label for="password" class="text-sm">Password</label>
			<input
				type="password"
				id="password"
				class="border-1 peer w-full appearance-none self-center rounded-lg border-gray-300 bg-white px-2.5
                            pb-2.5 text-sm text-gray-900 focus:border-blue-600 focus:outline-none focus:ring-0"
			/>
		</div>
		<Button value="Login" action={login} />
	</div>
</div>
