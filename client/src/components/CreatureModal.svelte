<script>
	// @ts-nocheck

	/**
	 * @type {boolean}
	 */
	export let isModalOpen;

	const closeModal = () => {
		isModalOpen = false;
	};
	const saveCreature = () => {};
</script>

<dialog {isModalOpen} open={isModalOpen}>
	<h1>Hello Modal</h1>

	<input type="text" name="" id="creature-name" />
	<label for="creature-name">Name</label>

	<input type="file" name="" id="image" />
	<label for="image">Image</label>

	<select name="" id="creature">
		<option value="Enemy">Enemy</option>
		<option value="non-player-char">Non-Player Character</option>
		<option value="player-char">Player Character</option>
	</select>
	<label for="creature">Creature</label>

	<input type="number" name="" id="armour-class" min="0" />
	<label for="armour-class">Armour Class</label>

	<div>
		<select name="" id="race">
			<option value="human">Human</option>
			<option value="orc">Orc</option>
			<option value="elf">Elf</option>
		</select>
		<label for="race">Race</label>

		<select name="" id="subrace">
			<option value="high">High</option>
			<option value="wood">Wood</option>
			<option value="shadar-kai">Shadar-Kai</option>
		</select>
		<label for="subrace">Subrace</label>
	</div>

	<div>
		<select name="" id="class">
			<option value="barbarian">Barbarian</option>
			<option value="fighter">Fighter</option>
			<option value="wizard">Wizard</option>
		</select>
		<label for="class">Class</label>

		<select name="" id="subclass">
			<option value="champion">Champion</option>
			<option value="eldrich-knight">Eldrich Knight</option>
			<option value="battle-master">Battle Master</option>
		</select>
		<label for="subclass">Subclass</label>
	</div>

	<input type="number" name="" id="walking-speed" min="0" />
	<label for="walking-speed">Walking Speed</label>

	<input type="number" name="" id="swimming-speed" min="0" />
	<label for="swimming-speed">Swimming Speed</label>

	<input type="number" name="" id="climbing-speed" min="0" />
	<label for="climbing-speed">Climbing Speed</label>

	<input type="number" name="" id="flying-speed" min="0" />
	<label for="flying-speed">Flying Speed</label>

	<select multiple name="" id="immunities">
		<option value="acid">Acid</option>
		<option value="bludgeoning">Bludgeoning</option>
		<option value="cold">Cold</option>
	</select>
	<label for="immunities">Immunities</label>

	<select multiple name="" id="resistances">
		<option value="acid">Acid</option>
		<option value="bludgeoning">Bludgeoning</option>
		<option value="cold">Cold</option>
	</select>
	<label for="resistances">Resistances</label>

	<select multiple name="" id="vulnerabilities">
		<option value="acid">Acid</option>
		<option value="bludgeoning">Bludgeoning</option>
		<option value="cold">Cold</option>
	</select>
	<label for="vulnerabilities">Vulnerabilities</label>

	<select multiple name="" id="advantages">
		<option value="arcana">Arcana</option>
		<option value="blinded">Blinded</option>
		<option value="constitution">Constitution</option>
	</select>
	<label for="advantages">Advantages</label>

	<select multiple name="" id="disadvantages">
		<option value="arcana">Arcana</option>
		<option value="blinded">Blinded</option>
		<option value="constitution">Constitution</option>
	</select>
	<label for="disadvantages">Disadvantages</label>

	<button on:click={closeModal}>Close</button>
	<button on:click={saveCreature}>Save</button>
</dialog>
