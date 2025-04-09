<script>
    import { Card, Button } from "flowbite-svelte";
    import { onMount } from "svelte";
    import { fetchTournaments } from "../stores/tournamentStore";
    import { tournaments, isLoading } from "../stores/tournamentStore";

    // Fetch tournaments when the component mounts
    onMount(() => {
        fetchTournaments();
    });

    // Helper function to get the most recent tournaments
    $: recentTournaments =
        $tournaments.length > 0 ? $tournaments.slice(0, 3) : [];
</script>

<div class="hero py-12 bg-blue-50">
    <div class="container mx-auto text-center">
        <h1 class="text-4xl font-bold mb-4">
            IIIT Hyderabad Sports Tournament System
        </h1>
        <p class="text-lg mb-6">
            Register for upcoming tournaments and track your participation
        </p>
        <div class="flex justify-center gap-4">
            <Button href="/tournaments" color="blue">Browse Tournaments</Button>
            <Button href="/login" color="alternative">Admin Login</Button>
        </div>
    </div>
</div>

<div class="py-12">
    <div class="container mx-auto">
        <h2 class="text-2xl font-bold mb-6">Recent Tournaments</h2>

        {#if $isLoading}
            <div class="text-center py-8">
                <p class="text-gray-500">Loading tournaments...</p>
            </div>
        {:else if recentTournaments.length === 0}
            <div class="text-center py-8">
                <p class="text-gray-500">
                    No tournaments available at the moment.
                </p>
            </div>
        {:else}
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {#each recentTournaments as tournament}
                    <Card padding="xl">
                        <h5 class="mb-2 text-2xl font-bold tracking-tight">
                            {tournament.name}
                        </h5>
                        <p
                            class="font-normal text-gray-700 dark:text-gray-400 mb-4"
                        >
                            {tournament.description ||
                                "Join this exciting tournament!"}
                        </p>
                        <div class="mb-3">
                            <span
                                class="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded"
                            >
                                {tournament.sport}
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
                        <Button
                            href={`/tournaments/${tournament.id}`}
                            color="blue"
                        >
                            View Details
                        </Button>
                    </Card>
                {/each}
            </div>
        {/if}

        <div class="text-center mt-8">
            <Button href="/tournaments" color="light"
                >View All Tournaments</Button
            >
        </div>
    </div>
</div>

<div class="py-12 bg-gray-50">
    <div class="container mx-auto">
        <h2 class="text-2xl font-bold mb-6 text-center">How It Works</h2>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="text-center p-4">
                <div class="bg-blue-100 inline-block p-4 rounded-full mb-4">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="w-8 h-8 text-blue-800"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                        />
                    </svg>
                </div>
                <h3 class="text-xl font-bold mb-2">Find Tournaments</h3>
                <p class="text-gray-600">
                    Browse through available tournaments and find the one that
                    interests you.
                </p>
            </div>

            <div class="text-center p-4">
                <div class="bg-blue-100 inline-block p-4 rounded-full mb-4">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="w-8 h-8 text-blue-800"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                        />
                    </svg>
                </div>
                <h3 class="text-xl font-bold mb-2">Register Your Team</h3>
                <p class="text-gray-600">
                    Complete the registration form with your team details before
                    the deadline.
                </p>
            </div>

            <div class="text-center p-4">
                <div class="bg-blue-100 inline-block p-4 rounded-full mb-4">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="w-8 h-8 text-blue-800"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                    </svg>
                </div>
                <h3 class="text-xl font-bold mb-2">Participate & Compete</h3>
                <p class="text-gray-600">
                    Show up on tournament day and compete to win amazing prizes!
                </p>
            </div>
        </div>
    </div>
</div>
