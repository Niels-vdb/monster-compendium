<script lang="ts">
	import Button from '../../components/Button.svelte';
	import FloatingInput from '../../components/FloatingInput.svelte';

	let email: string = $state('');

	const recover = () => {
		if (!email) {
			console.log('Please fill out email address');
		} else {
			const data = {
				email: email
			};
		}
	};
</script>

<div class="flex h-dvh w-dvw flex-col items-center justify-center gap-5">
	<h1 class="text-2xl">Recover Your Password</h1>
	<div class="flex w-96 flex-col justify-center gap-4 rounded-lg border border-black p-5">
		<FloatingInput
			inputType="email"
			inputId="email-register"
			labelName="Email"
			bind:value={email}
		/>
		<Button value="Send Recovery Email" action={recover} disabled={!email} />
	</div>
</div>
