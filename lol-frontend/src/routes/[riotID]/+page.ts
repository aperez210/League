import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
    console.log(params.riotID);
    const decodedId = decodeURIComponent(params.riotID);
    console.log(decodedId);
    const safeUrlParam = encodeURIComponent(params.riotID);
    // 1. We use the 'fetch' provided by SvelteKit, pointing at your Vite proxy
    const response = await fetch(`/api/games/${safeUrlParam}`);
    
    if (!response.ok) {
        throw new Error('Failed to fetch games from FastAPI');
    }

    // 2. We parse the raw JSON
    const data = await response.json();

    // 3. We return the object. SvelteKit automatically turns this shape into "PageData"
    return {
        riotId: decodedId,
        games: data
    };
};