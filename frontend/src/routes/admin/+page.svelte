<script>
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { isAdmin, isAuthenticated, user } from "../../stores/userStore";
    import {
        Button,
        Card,
        Heading,
        Tabs,
        TabItem,
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell,
    } from "flowbite-svelte";
    import { fetchTournaments } from "../../stores/tournamentStore";
    import { tournaments, isLoading } from "../../stores/tournamentStore";

    // Redirect if not authenticated as admin
    onMount(() => {
        if (!$isAuthenticated || !$isAdmin) {
            goto("/login");
            return;
        }

        fetchTournaments();
    });

    // Active tab tracker
    let activeTab = "tournaments";
</script>

<!-- Admin panel layout -->
<div class="container mx-auto py-8">
    <div class="flex justify-between items-center mb-6">
        <Heading tag="h1" class="text-2xl font-bold">Admin Dashboard</Heading>
        <div>
            <span class="mr-2"
                >Logged in as: <strong>{$user?.username}</strong></span
            >
            <Button href="/admin/tournaments/new" size="sm" color="blue"
                >Add Tournament</Button
            >
        </div>
    </div>

    <!-- Admin tabs -->
    <Tabs style="pill" contentClass="p-4 bg-white rounded-lg shadow-sm mt-4">
        <TabItem bind:activeTab title="Tournaments" name="tournaments">
            <div class="mb-4 flex justify-between items-center">
                <h2 class="text-xl font-semibold">All Tournaments</h2>
            </div>

            {#if $isLoading}
                <div class="text-center py-8">
                    <div
                        class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"
                    ></div>
                    <p class="mt-4 text-gray-600">Loading tournaments...</p>
                </div>
            {:else if $tournaments.length === 0}
                <div class="bg-gray-50 rounded-lg p-8 text-center">
                    <p class="text-gray-500 mb-4">
                        No tournaments have been created yet.
                    </p>
                    <Button href="/admin/tournaments/new" color="blue"
                        >Create First Tournament</Button
                    >
                </div>
            {:else}
                <Table hoverable={true}>
                    <TableHead>
                        <TableHeadCell>Name</TableHeadCell>
                        <TableHeadCell>Sport</TableHeadCell>
                        <TableHeadCell>Date Range</TableHeadCell>
                        <TableHeadCell>Registration</TableHeadCell>
                        <TableHeadCell>Teams</TableHeadCell>
                        <TableHeadCell>Actions</TableHeadCell>
                    </TableHead>
                    <TableBody>
                        {#each $tournaments as tournament}
                            <TableBodyRow>
                                <TableBodyCell>{tournament.name}</TableBodyCell>
                                <TableBodyCell>{tournament.sport}</TableBodyCell
                                >
                                <TableBodyCell
                                    >{tournament.start_date} to {tournament.end_date}</TableBodyCell
                                >
                                <TableBodyCell
                                    >Deadline: {tournament.registration_deadline}</TableBodyCell
                                >
                                <TableBodyCell
                                    >{tournament.current_teams}/{tournament.max_teams}</TableBodyCell
                                >
                                <TableBodyCell class="space-x-2">
                                    <Button
                                        href={`/admin/tournaments/${tournament.id}`}
                                        size="xs"
                                        color="light">View</Button
                                    >
                                    <Button
                                        href={`/admin/tournaments/${tournament.id}/edit`}
                                        size="xs"
                                        color="blue">Edit</Button
                                    >
                                    <Button
                                        size="xs"
                                        color="red"
                                        on:click={() =>
                                            alert(
                                                "Delete functionality to be implemented",
                                            )}>Delete</Button
                                    >
                                </TableBodyCell>
                            </TableBodyRow>
                        {/each}
                    </TableBody>
                </Table>
            {/if}
        </TabItem>

        <TabItem bind:activeTab title="Registrations" name="registrations">
            <div class="mb-4">
                <h2 class="text-xl font-semibold">Tournament Registrations</h2>
                <p class="text-gray-600 mt-2">
                    Select a tournament to view its registrations:
                </p>
            </div>

            {#if $tournaments.length === 0}
                <div class="bg-gray-50 rounded-lg p-8 text-center">
                    <p class="text-gray-500">No tournaments available.</p>
                </div>
            {:else}
                <div
                    class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4"
                >
                    {#each $tournaments as tournament}
                        <Card>
                            <h5
                                class="text-xl font-bold tracking-tight text-gray-900 dark:text-white"
                            >
                                {tournament.name}
                            </h5>
                            <p
                                class="font-normal text-gray-700 dark:text-gray-400 leading-tight"
                            >
                                <span class="block mt-1"
                                    >Sport: {tournament.sport}</span
                                >
                                <span class="block mt-1"
                                    >Teams: {tournament.current_teams}/{tournament.max_teams}</span
                                >
                            </p>
                            <Button
                                href={`/admin/tournaments/${tournament.id}/registrations`}
                                color="blue"
                            >
                                View Registrations
                            </Button>
                        </Card>
                    {/each}
                </div>
            {/if}
        </TabItem>
    </Tabs>
</div>
