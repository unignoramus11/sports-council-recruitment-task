<script>
    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import {
        Button,
        Card,
        Badge,
        Alert,
        Spinner,
        Heading,
        Hr,
    } from "flowbite-svelte";
    import { getTournament } from "../../../stores/tournamentStore";
    import RegistrationForm from "../../../components/RegistrationForm.svelte";

    // Get tournament ID from the route
    const tournamentId = $page.params.id;

    // State variables
    let tournament = null;
    let loading = true;
    let error = null;
    let showRegistrationForm = false;

    // Fetch tournament data on mount
    onMount(async () => {
        try {
            tournament = await getTournament(tournamentId);
            loading = false;
        } catch (err) {
            error = err.message || "Failed to load tournament details";
            loading = false;
        }
    });

    // Get tournament status
    function getTournamentStatus(tournament) {
        const today = new Date();
        const startDate = new Date(tournament.start_date);
        const endDate = new Date(tournament.end_date);
        const deadlineDate = new Date(tournament.registration_deadline);

        if (startDate > today) {
            return {
                text: "Upcoming",
                color: "blue",
                canRegister:
                    today <= deadlineDate &&
                    tournament.current_teams < tournament.max_teams,
            };
        } else if (today >= startDate && today <= endDate) {
            return {
                text: "Ongoing",
                color: "green",
                canRegister:
                    today <= deadlineDate &&
                    tournament.current_teams < tournament.max_teams,
            };
        } else {
            return {
                text: "Completed",
                color: "gray",
                canRegister: false,
            };
        }
    }

    // Toggle registration form
    function toggleRegistrationForm() {
        showRegistrationForm = !showRegistrationForm;
    }
</script>

<div class="container mx-auto py-8">
    {#if loading}
        <div class="flex flex-col items-center justify-center py-12">
            <Spinner size="xl" />
            <p class="mt-4 text-gray-600">Loading tournament details...</p>
        </div>
    {:else if error}
        <Alert color="red">
            <span class="font-medium">Error:</span>
            {error}
            <div class="mt-2">
                <Button href="/tournaments" color="blue" size="xs"
                    >Back to Tournaments</Button
                >
            </div>
        </Alert>
    {:else if tournament}
        {@const status = getTournamentStatus(tournament)}

        <!-- Tournament header -->
        <div class="mb-8">
            <div
                class="flex flex-col md:flex-row justify-between md:items-center gap-4 mb-4"
            >
                <div>
                    <h1 class="text-3xl font-bold">{tournament.name}</h1>
                    <div class="flex items-center mt-2">
                        <Badge color={status.color} class="mr-2"
                            >{status.text}</Badge
                        >
                        <Badge color="indigo">{tournament.sport}</Badge>
                    </div>
                </div>

                {#if status.canRegister}
                    <Button color="blue" on:click={toggleRegistrationForm}>
                        Register for Tournament
                    </Button>
                {/if}
            </div>

            <!-- Status message -->
            {#if !status.canRegister}
                {#if tournament.current_teams >= tournament.max_teams}
                    <Alert color="yellow" class="mt-4">
                        <span class="font-medium">Registration closed:</span> This
                        tournament has reached its maximum capacity.
                    </Alert>
                {:else if new Date() > new Date(tournament.registration_deadline)}
                    <Alert color="yellow" class="mt-4">
                        <span class="font-medium">Registration closed:</span> The
                        deadline for registration has passed.
                    </Alert>
                {/if}
            {/if}
        </div>

        <!-- Tournament details -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <Card padding="xl" class="md:col-span-2">
                <Heading tag="h2" class="mb-4">Tournament Details</Heading>

                <p class="text-gray-700 mb-6">
                    {tournament.description ||
                        "No description available for this tournament."}
                </p>

                <Hr class="my-4" />

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <h3 class="font-semibold text-gray-900">Dates</h3>
                        <p class="text-sm text-gray-600">
                            Start: {tournament.start_date}
                        </p>
                        <p class="text-sm text-gray-600">
                            End: {tournament.end_date}
                        </p>
                    </div>

                    <div>
                        <h3 class="font-semibold text-gray-900">
                            Registration
                        </h3>
                        <p class="text-sm text-gray-600">
                            Deadline: {tournament.registration_deadline}
                        </p>
                        <p class="text-sm text-gray-600">
                            Teams: {tournament.current_teams}/{tournament.max_teams}
                        </p>
                    </div>
                </div>
            </Card>

            <Card padding="xl">
                <Heading tag="h2" class="mb-4">Tournament Stats</Heading>

                <div class="space-y-4">
                    <div>
                        <h3 class="font-semibold text-gray-900">Sport</h3>
                        <p>{tournament.sport}</p>
                    </div>

                    <div class="w-full bg-gray-200 rounded-full h-2.5">
                        <div
                            class="bg-blue-600 h-2.5 rounded-full"
                            style="width: {(tournament.current_teams /
                                tournament.max_teams) *
                                100}%"
                        ></div>
                    </div>
                    <p class="text-sm text-gray-600 text-center">
                        {tournament.current_teams} of {tournament.max_teams} teams
                        registered
                    </p>

                    {#if status.canRegister}
                        <Button
                            color="blue"
                            class="w-full"
                            on:click={toggleRegistrationForm}
                        >
                            Register Now
                        </Button>
                    {/if}
                </div>
            </Card>
        </div>

        <!-- Registration form -->
        {#if showRegistrationForm}
            <Card padding="xl" class="mb-8">
                <Heading tag="h2" class="mb-4">Tournament Registration</Heading>
                <RegistrationForm
                    {tournamentId}
                    onComplete={toggleRegistrationForm}
                />
            </Card>
        {/if}

        <!-- Related info - can be implemented by candidates -->
        <Card padding="xl">
            <Heading tag="h2" class="mb-4">Additional Information</Heading>
            <p class="text-gray-600">
                This section can be used to display additional tournament
                information such as rules, venue details, prizes, etc. This is a
                placeholder for candidates to implement.
            </p>
        </Card>
    {/if}
</div>
