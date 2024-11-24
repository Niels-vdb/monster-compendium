<script>
	import Navbar from '../../components/Navbar.svelte';
	import CreatureSelector from '../../components/CreatureSelector.svelte';
	import CreatureExplorer from '../../components/CreatureExplorer.svelte';
</script>

<div class="grid h-dvh grid-rows-8">
	<Navbar />

	<section class="row-span-7 mx-5 mb-5 grid grid-cols-6 gap-5">
		<CreatureSelector />
		<CreatureExplorer />
	</section>
</div>

<style lang="postcss">
</style>
