import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			// Whenever Svelte makes a request to /api/...
			'/api': {
				// ...Vite forwards it to your FastAPI server
				target: 'http://127.0.0.1:8000', 
				changeOrigin: true,
				
				// OPTIONAL: If your FastAPI routes do NOT start with /api 
				// (e.g., your python route is just @app.get("/champions")),
				// uncomment the line below to strip "/api" before sending it to Python:
				// rewrite: (path) => path.replace(/^\/api/, '')
			}
		}
	}
});
