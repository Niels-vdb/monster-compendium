<script lang="ts">
	import { goto } from '$app/navigation';
	import Button from '../../components/Button.svelte';
	import Checkbox from '../../components/Checkbox.svelte';
	import FloatingInput from '../../components/FloatingInput.svelte';

	let username: string = $state('');
	let email: string = $state('');
	let emailConfirm: string = $state('');
	let password: string = $state('');
	let passwordConfirm: string = $state('');
	let termsChecked: boolean = $state(false);

	const register = () => {
		if (!username || !email || !password || !passwordConfirm || !termsChecked) {
			console.log('Please fill out the form');
		} else if (password !== passwordConfirm) {
			console.log('Passwords are not the same');
		} else if (email !== emailConfirm) {
			console.log('Email addresses are not the same');
		} else if (!termsChecked) {
			console.log('Accept Terms and Conditions');
		} else {
			const data = {
				username,
				email,
				password
			};

			goto('/');
		}
	};
</script>

<div class="flex h-dvh w-dvw flex-col items-center justify-center gap-5">
	<h1 class="text-2xl">Create an Account</h1>
	<div class="flex w-96 flex-col justify-center gap-4 rounded-lg border border-black p-5">
		<FloatingInput
			inputType="text"
			inputId="username-register"
			labelName="Username"
			bind:value={username}
		/>
		<FloatingInput
			inputType="email"
			inputId="email-register"
			labelName="Email"
			bind:value={email}
		/>
		<FloatingInput
			inputType="email"
			inputId="confirm-email"
			labelName="Email"
			bind:value={emailConfirm}
		/>
		<FloatingInput
			inputType="password"
			inputId="password-register"
			labelName="Password"
			bind:value={password}
		/>
		<FloatingInput
			inputType="password"
			inputId="confirm-password"
			labelName="Confirm password"
			bind:value={passwordConfirm}
		/>
		<Checkbox
			checkboxId="terms-services"
			checkboxLabel="I accept the <a href=# class='hover:underline'>Terms and Conditions</a>"
			bind:checked={termsChecked}
		/>
		<Button value="Register" action={register} />
		<p class="text-sm font-light">
			Already have an account? <a href="/" class="font-medium hover:underline">Login here</a>
		</p>
	</div>
</div>
