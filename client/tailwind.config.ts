import forms from '@tailwindcss/forms';
import type { Config } from 'tailwindcss';

export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],

	theme: {
		extend: {
			colors: {
				primary: '#797d62',
				secondary: '#9B9B7A',
				textPrimary: '#000000',
				textSecondary: '#5A5A5A',
				textTertiary: '#B3B3B3'
			},
			transitionProperty: {
				'top-font-color': 'top, font-size, color'
			}
			// fontFamily: {
			// 	sans: ['Metamorphous', 'system-ui', 'sans-serif']
			// }
		}
	},

	plugins: [forms]
} satisfies Config;
