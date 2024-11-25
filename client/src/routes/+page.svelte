<script>
	import Button from '../components/Button.svelte';
	import FloatingInput from '../components/FloatingInput.svelte';

	const login = () => {
		console.log('click');
	};
</script>

<div class="flex h-dvh w-dvw flex-col items-center justify-center gap-5">
	<h1 class="text-2xl">Creature Compendium</h1>
	<div class="flex h-64 w-96 flex-col justify-center gap-4 rounded-lg border border-black p-5">
		<FloatingInput inputType="text" inputId="username-login" labelName="Username" />
		<FloatingInput inputType="password" inputId="password-login" labelName="Password" />
		<Button value="Login" action={login} />
		<div class="flex justify-between">
			<a href="#" class="hover:text-[#9E7682]">Register</a>
			<a href="#" class="hover:text-[#9E7682]">Recover password</a>
		</div>
	</div>
</div>
