<script>
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { goto } from "$app/navigation";
    import {
        isAdmin,
        isAuthenticated,
        getToken,
    } from "../../../../../stores/userStore";
    import {
        Card,
        Heading,
        Spinner,
        Alert,
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell,
        Button,
    } from "flowbite-svelte";
    import { getTournament } from "../../../../../stores/tournamentStore";

    // Get tournament ID from route
    const tournamentId = $page.params.id;

    // State
    let tournament = null;
    let registrations = [];
    let loading = true;
    let error = null;

    // Fetch tournament and registrations on mount
    onMount(async () => {
        // Redirect if not authenticated
        if (!$isAuthenticated || !$isAdmin) {
            goto("/login");
            return;
        }

        try {
            // Fetch tournament details
            tournament = await getTournament(tournamentId);

            // Fetch registrations for this tournament
            const token = getToken();
            const response = await fetch(`/api/registrations/${tournamentId}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                throw new Error("Failed to load registrations");
            }

            registrations = await response.json();
            loading = false;
        } catch (err) {
            error = err.message || "Failed to load data";
            loading = false;
        }
    });
</script>

<div class="container mx-auto py-8">
    <div
        class="mb-6 flex flex-col md:flex-row md:justify-between md:items-center gap-4"
    >
        <div>
            <Heading tag="h1">Tournament Registrations</Heading>
            {#if tournament}
                <p class="text-gray-600">{tournament.name}</p>
            {/if}
        </div>
        <Button href="/admin" color="light">Back to Dashboard</Button>
    </div>

    {#if loading}
        <div class="flex items-center justify-center py-12">
            <Spinner size="xl" />
            <p class="ml-4 text-gray-600">Loading registrations...</p>
        </div>
    {:else if error}
        <Alert color="red">
            <span class="font-medium">Error:</span>
            {error}
        </Alert>
    {:else if registrations.length === 0}
        <Card padding="xl" class="text-center">
            <p class="mb-4 text-gray-600">
                No registrations found for this tournament.
            </p>
            <div class="flex justify-center">
                <Button href="/admin" color="light">Back to Dashboard</Button>
            </div>
        </Card>
    {:else}
        <Card padding="xl">
            <Table hoverable={true}>
                <TableHead>
                    <TableHeadCell>Team Name</TableHeadCell>
                    <TableHeadCell>Captain</TableHeadCell>
                    <TableHeadCell>Contact</TableHeadCell>
                    <TableHeadCell>Players</TableHeadCell>
                    <TableHeadCell>Registration Date</TableHeadCell>
                    <TableHeadCell>Actions</TableHeadCell>
                </TableHead>
                <TableBody>
                    {#each registrations as registration}
                        <TableBodyRow>
                            <TableBodyCell
                                >{registration.team_name}</TableBodyCell
                            >
                            <TableBodyCell
                                >{registration.captain_name}</TableBodyCell
                            >
                            <TableBodyCell
                                >{registration.captain_email}</TableBodyCell
                            >
                            <TableBodyCell
                                >{registration.player_names.length} players</TableBodyCell
                            >
                            <TableBodyCell
                                >{registration.registration_date}</TableBodyCell
                            >
                            <TableBodyCell>
                                <Button size="xs" color="blue"
                                    >View Details</Button
                                >
                            </TableBodyCell>
                        </TableBodyRow>
                    {/each}
                </TableBody>
            </Table>
        </Card>
    {/if}
</div>
