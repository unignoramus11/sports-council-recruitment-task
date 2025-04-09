<script>
    import { onMount } from "svelte";
    import { Card, Button, Input, Select, Badge } from "flowbite-svelte";
    import { fetchTournaments } from "../../stores/tournamentStore";
    import { tournaments, isLoading } from "../../stores/tournamentStore";

    // Search and filter state
    let searchQuery = "";
    let sportFilter = "";
    let statusFilter = "all"; // all, upcoming, past

    // Mount component
    onMount(() => {
        fetchTournaments();
    });

    // Filtered tournaments based on search query and filters
    $: filteredTournaments = $tournaments.filter((tournament) => {
        // Search filter
        if (
            searchQuery &&
            !tournament.name
                .toLowerCase()
                .includes(searchQuery.toLowerCase()) &&
            !tournament.description
                ?.toLowerCase()
                .includes(searchQuery.toLowerCase()) &&
            !tournament.sport.toLowerCase().includes(searchQuery.toLowerCase())
        ) {
            return false;
        }

        // Sport filter
        if (sportFilter && tournament.sport !== sportFilter) {
            return false;
        }

        // Status filter
        if (statusFilter !== "all") {
            const today = new Date();
            const startDate = new Date(tournament.start_date);

            if (statusFilter === "upcoming" && startDate < today) {
                return false;
            }

            if (statusFilter === "past" && startDate >= today) {
                return false;
            }
        }

        return true;
    });

    // Get unique sports for filter dropdown
    $: uniqueSports = [...new Set($tournaments.map((t) => t.sport))];

    // Get status of tournament (upcoming, ongoing, completed)
    function getTournamentStatus(tournament) {
        const today = new Date();
        const startDate = new Date(tournament.start_date);
        const endDate = new Date(tournament.end_date);

        if (startDate > today) {
            return { text: "Upcoming", color: "blue" };
        } else if (today >= startDate && today <= endDate) {
            return { text: "Ongoing", color: "green" };
        } else {
            return { text: "Completed", color: "gray" };
        }
    }
</script>

<div class="container mx-auto py-8">
    <h1 class="text-3xl font-bold mb-8">Tournaments</h1>

    <!-- Search and Filter -->
    <div class="mb-8 bg-white p-6 rounded-lg shadow-sm">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
                <Input
                    bind:value={searchQuery}
                    placeholder="Search tournaments..."
                />
            </div>

            <div>
                <Select bind:value={sportFilter} class="w-full">
                    <option value="">All Sports</option>
                    {#each uniqueSports as sport}
                        <option value={sport}>{sport}</option>
                    {/each}
                </Select>
            </div>

            <div>
                <Select bind:value={statusFilter} class="w-full">
                    <option value="all">All Status</option>
                    <option value="upcoming">Upcoming</option>
                    <option value="past">Past</option>
                </Select>
            </div>
        </div>
    </div>

    <!-- Tournaments List -->
    {#if $isLoading}
        <div class="text-center py-12">
            <div
                class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"
            ></div>
            <p class="mt-4 text-gray-600">Loading tournaments...</p>
        </div>
    {:else if filteredTournaments.length === 0}
        <div class="text-center py-12 bg-white rounded-lg shadow-sm">
            <p class="text-gray-500">
                No tournaments found matching your criteria.
            </p>
            {#if searchQuery || sportFilter || statusFilter !== "all"}
                <Button
                    color="light"
                    class="mt-4"
                    on:click={() => {
                        searchQuery = "";
                        sportFilter = "";
                        statusFilter = "all";
                    }}>Clear Filters</Button
                >
            {/if}
        </div>
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each filteredTournaments as tournament}
                {@const status = getTournamentStatus(tournament)}
                <Card padding="xl">
                    <div class="flex justify-between items-start">
                        <h5 class="mb-2 text-2xl font-bold tracking-tight">
                            {tournament.name}
                        </h5>
                        <Badge color={status.color}>{status.text}</Badge>
                    </div>

                    <p
                        class="font-normal text-gray-700 dark:text-gray-400 mb-4"
                    >
                        {tournament.description ||
                            "Join this exciting tournament!"}
                    </p>

                    <div class="mb-3">
                        <Badge color="indigo">{tournament.sport}</Badge>
                        <span class="text-sm ml-2">
                            {tournament.current_teams}/{tournament.max_teams} teams
                            registered
                        </span>
                    </div>

                    <div class="text-sm mb-4">
                        <p>
                            <strong>Registration Deadline:</strong>
                            {tournament.registration_deadline}
                        </p>
                        <p>
                            <strong>Tournament Dates:</strong>
                            {tournament.start_date} to {tournament.end_date}
                        </p>
                    </div>

                    <Button href={`/tournaments/${tournament.id}`} color="blue">
                        View Details
                    </Button>
                </Card>
            {/each}
        </div>
    {/if}
</div>
