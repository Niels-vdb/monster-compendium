<script lang="ts">
	import { redirect } from '@sveltejs/kit';
	import Button from '../components/Button.svelte';
	import FloatingInput from '../components/FloatingInput.svelte';
	import { goto } from '$app/navigation';

	let username: string = $state('');
	let password: string = $state('');

	const login = () => {
		if (!username || !password) {
			console.log('Please fill out username and password');
		} else {
			const data = {
				username: username,
				password: password
			};

			goto('/creatures');
		}
	};
</script>

<div class="flex h-dvh w-dvw flex-col items-center justify-center gap-5">
	<h1 class="text-2xl">Creature Compendium</h1>
	<div class="flex w-96 flex-col justify-center gap-4 rounded-lg border border-black p-5">
		<FloatingInput
			bind:value={username}
			inputType="text"
			inputId="username-login"
			labelName="Username"
			required={true}
		/>
		<FloatingInput
			bind:value={password}
			inputType="password"
			inputId="password-login"
			labelName="Password"
			required={true}
		/>
		<Button value="Login" action={login} />
		<div class="flex justify-between">
			<a href="/register" class="text-sm font-light hover:underline">Register</a>
			<a href="/recover" class="text-sm font-light hover:underline">Recover password</a>
		</div>
	</div>
</div>
