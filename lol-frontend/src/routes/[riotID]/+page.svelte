<script lang="ts">
    import type { PageData } from './$types';

    let { data }: { data: PageData } = $props();

    function getRarityColor(rarity: number) {
        switch (rarity) {
            case 0: return 'border-gray-500 text-gray-300';
            case 1: return 'border-gray-300 text-white'; // Silver
            case 2: return 'border-yellow-500 text-yellow-400'; // Gold
            case 3: return 'border-purple-400 text-purple-400'; // Prismatic
            default: return 'border-blue-400 text-blue-400'; 
        }
    }
</script>

<div class="min-h-screen bg-gray-900 text-gray-100 p-8">
    <div class="max-w-7xl mx-auto">
        <h1 class="text-4xl font-bold mb-8 text-center bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            Arena Match History for {data.riotId}
        </h1>

        <div class="space-y-8">
            {#each data.games as game, i}
                <div class="bg-gray-800 rounded-xl shadow-xl overflow-hidden border border-gray-700">
                    <div class="bg-gray-700 px-6 py-4 border-b border-gray-600">
                        <h2 class="text-xl font-semibold text-white">Match #{i + 1}</h2>
                    </div>
                    
                    <div class="p-6 bg-gray-800">
                        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                            {#each game.players as player, j}
                                <div class="p-4 rounded-lg flex flex-col gap-3 transition-colors duration-200 {player.name.toLowerCase() === data.riotId.split('#')[0].toLowerCase() ? 'bg-blue-900/30 border border-blue-500 shadow-[0_0_15px_rgba(59,130,246,0.3)]' : 'bg-gray-750 border border-gray-600 hover:border-gray-500 hover:bg-gray-700/50'}">
                                    <div class="flex items-center gap-3">
                                        <div class="w-12 h-12 rounded-full overflow-hidden bg-gray-700 flex-shrink-0 border-2 border-gray-600">
                                            <img 
                                                src="https://ddragon.leagueoflegends.com/cdn/14.8.1/img/champion/{player.champion}.png" 
                                                alt={player.champion}
                                                class="w-full h-full object-cover"
                                                onerror={(e) => (e.currentTarget as HTMLImageElement).src='https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/-1.png'}
                                            />
                                        </div>
                                        <div class="overflow-hidden">
                                            <div class="font-bold text-gray-100 truncate">{player.name}</div>
                                            <div class="text-sm text-gray-400 truncate">{player.champion}</div>
                                        </div>
                                    </div>
                                    
                                    <div class="flex flex-wrap gap-2 mt-auto">
                                        {#each player.augments_data as aug}
                                            {#if aug}
                                                <div class="text-[10px] sm:text-xs px-2 py-1 rounded-full border bg-gray-900/50 {getRarityColor(aug.rarity)} whitespace-nowrap" title="Rarity {aug.rarity}">
                                                    {aug.name}
                                                </div>
                                            {/if}
                                        {/each}
                                    </div>
                                </div>
                            {/each}
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    </div>
</div>
