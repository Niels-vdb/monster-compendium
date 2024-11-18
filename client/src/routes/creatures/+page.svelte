<script>
	import Navbar from '../../components/Navbar.svelte';
	import CreatureSelector from '../../components/CreatureSelector.svelte';
</script>

<div class="grid h-dvh grid-rows-8">
	<Navbar />

	<section class="row-span-7 mx-5 mb-5 grid grid-cols-6 gap-5">
		<CreatureSelector />

		<div class="col-span-4 rounded-xl bg-[#9B9B7A]"></div>
	</section>
</div>

<style lang="postcss">
</style>
