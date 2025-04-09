<script>
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { goto } from "$app/navigation";
    import { isAdmin, isAuthenticated } from "../../../../../stores/userStore";
    import { Card, Heading, Spinner, Alert } from "flowbite-svelte";
    import TournamentForm from "../../../../../components/TournamentForm.svelte";
    import { getTournament } from "../../../../../stores/tournamentStore";

    // Get tournament ID from route
    const tournamentId = $page.params.id;

    // State
    let tournament = null;
    let loading = true;
    let error = null;

    // Fetch tournament on mount
    onMount(async () => {
        // Redirect if not authenticated
        if (!$isAuthenticated || !$isAdmin) {
            goto("/login");
            return;
        }

        try {
            tournament = await getTournament(tournamentId);
            loading = false;
        } catch (err) {
            error = err.message || "Failed to load tournament";
            loading = false;
        }
    });

    // Handle completion of form
    function handleComplete() {
        goto("/admin");
    }
</script>

<div class="container mx-auto py-8">
    <Heading tag="h1" class="mb-6">Edit Tournament</Heading>

    {#if loading}
        <div class="flex items-center justify-center py-12">
            <Spinner size="xl" />
            <p class="ml-4 text-gray-600">Loading tournament details...</p>
        </div>
    {:else if error}
        <Alert color="red">
            <span class="font-medium">Error:</span>
            {error}
        </Alert>
    {:else}
        <Card padding="xl">
            <TournamentForm {tournament} onComplete={handleComplete} />
        </Card>
    {/if}
</div>
