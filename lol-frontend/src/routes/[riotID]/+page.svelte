<script lang="ts">
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();

  function getRarityColor(rarity: number) {
    switch (rarity) {
      case 0:
        return 'border-gray-500 text-gray-300';
      case 1:
        return 'border-gray-300 text-white'; // Silver
      case 2:
        return 'border-yellow-500 text-yellow-400'; // Gold
      case 3:
        return 'border-purple-400 text-purple-400'; // Prismatic
      default:
        return 'border-blue-400 text-blue-400';
    }
  }

  function getRelativeTime(timestamp: number) {
    if (!timestamp) return '';
    const seconds = Math.floor((Date.now() - timestamp) / 1000);
    if (seconds < 60) return 'Just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)} minutes ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
    if (seconds < 604800) return `${Math.floor(seconds / 86400)} days ago`;
    if (seconds < 2592000) return `${Math.floor(seconds / 604800)} weeks ago`;
    if (seconds < 31536000) return `${Math.floor(seconds / 2592000)} months ago`;
    return `${Math.floor(seconds / 31536000)} years ago`;
  }

  function getExactTime(timestamp: number) {
    if (!timestamp) return '';
    return new Date(timestamp).toLocaleString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    });
  }
</script>

<div class="min-h-screen bg-gray-900 p-8 text-gray-100">
  <div class="mx-auto max-w-7xl">
    <h1
      class="mb-8 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-center text-4xl font-bold text-transparent"
    >
      Arena Match History for {data.riotId}
    </h1>

    <div class="space-y-8">
      {#each data.games as game, i}
        <div class="overflow-hidden rounded-xl border border-gray-700 bg-gray-800 shadow-xl">
          <div
            class="flex items-center justify-between border-b border-gray-600 bg-gray-700 px-6 py-4"
          >
            <h2 class="text-xl font-semibold text-white">Match #{i + 1}</h2>
            <span class="cursor-help text-sm text-gray-400" title={getExactTime(game.gameCreation)}>
              {getRelativeTime(game.gameCreation)}
            </span>
          </div>

          <div class="bg-gray-800 p-6">
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
              {#each game.players as player, j}
                <div
                  class="flex flex-col gap-3 rounded-lg p-4 transition-colors duration-200 {player.name.toLowerCase() ===
                  data.riotId.split('#')[0].toLowerCase()
                    ? 'border border-blue-500 bg-blue-900/30 shadow-[0_0_15px_rgba(59,130,246,0.3)]'
                    : 'bg-gray-750 border border-gray-600 hover:border-gray-500 hover:bg-gray-700/50'}"
                >
                  <div class="flex items-center gap-3">
                    <div
                      class="h-12 w-12 flex-shrink-0 overflow-hidden rounded-full border-2 border-gray-600 bg-gray-700"
                    >
                      <img
                        src="https://ddragon.leagueoflegends.com/cdn/14.8.1/img/champion/{player.champion}.png"
                        alt={player.champion}
                        class="h-full w-full object-cover"
                        onerror={(e) =>
                          ((e.currentTarget as HTMLImageElement).src =
                            'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/-1.png')}
                      />
                    </div>
                    <div class="overflow-hidden">
                      <div class="truncate font-bold text-gray-100">{player.name}</div>
                      <div class="truncate text-sm text-gray-400">{player.champion}</div>
                    </div>
                  </div>

                  <div class="mt-auto flex flex-wrap gap-2">
                    {#each player.augments_data as aug}
                      {#if aug}
                        <div
                          class="rounded-full border bg-gray-900/50 px-2 py-1 text-[10px] sm:text-xs {getRarityColor(
                            aug.rarity
                          )} whitespace-nowrap"
                          title="Rarity {aug.rarity}"
                        >
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
