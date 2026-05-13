<script lang="ts">
    import { goto } from '$app/navigation';

    // Svelte 5 state rune to track the input box
    let searchInput = $state('');

    function handleSearch(event: Event) {
        event.preventDefault(); 
        
        if (searchInput.trim() !== '') {
            // Safely encode the '#' so "Faker#KR1" becomes "Faker%23KR1"
            const safeRiotId = encodeURIComponent(searchInput.trim());
            
            // Use SvelteKit's router to navigate to our new dynamic page
            goto(`/${safeRiotId}`);
        }
    }
</script>

<div class="max-w-md mx-auto mt-20 p-6 bg-white rounded-lg shadow-md">
    <h1 class="text-2xl font-bold mb-4 text-gray-800">Lookup Arena Player</h1>
    
    <form onsubmit={handleSearch} class="flex gap-2">
        <input 
            type="text" 
            bind:value={searchInput} 
            placeholder="Riot ID (e.g. Player#NA1)" 
            class="flex-1 px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
        />
        <button 
            type="submit" 
            class="px-6 py-2 bg-blue-600 text-white font-semibold rounded hover:bg-blue-700 transition"
        >
            Search
        </button>
    </form>
</div>