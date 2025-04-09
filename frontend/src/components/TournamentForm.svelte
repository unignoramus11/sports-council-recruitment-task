<script>
    import {
        Input,
        Label,
        Button,
        Textarea,
        Alert,
        Select,
    } from "flowbite-svelte";
    import {
        createTournament,
        updateTournament,
    } from "../stores/tournamentStore";
    import { isAdmin, isAuthenticated } from "../stores/userStore";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";

    // Props
    export let tournament = null; // If provided, we're in edit mode
    export let onComplete = () => {};

    // Determine if we're creating or editing
    $: isEditMode = !!tournament;

    // Form data
    let name = "";
    let description = "";
    let sport = "";
    let startDate = "";
    let endDate = "";
    let registrationDeadline = "";
    let maxTeams = 16;
    let loading = false;
    let error = null;
    let success = false;

    // List of available sports (could be fetched from API in a real implementation)
    const sportsList = [
        "Basketball",
        "Cricket",
        "Football",
        "Volleyball",
        "Badminton",
        "Table Tennis",
        "Chess",
        "Swimming",
        "Tennis",
        "Athletics",
    ];

    // Initialize form data from tournament if in edit mode
    onMount(() => {
        if (!$isAuthenticated || !$isAdmin) {
            goto("/login");
            return;
        }

        if (tournament) {
            name = tournament.name;
            description = tournament.description || "";
            sport = tournament.sport;
            startDate = tournament.start_date;
            endDate = tournament.end_date;
            registrationDeadline = tournament.registration_deadline;
            maxTeams = tournament.max_teams;
        }
    });

    // Validate form
    function validateForm() {
        if (!name.trim()) return "Tournament name is required";
        if (!sport) return "Sport is required";
        if (!startDate) return "Start date is required";
        if (!endDate) return "End date is required";
        if (!registrationDeadline) return "Registration deadline is required";
        if (maxTeams <= 0) return "Maximum teams must be greater than 0";

        // Date validation
        const start = new Date(startDate);
        const end = new Date(endDate);
        const deadline = new Date(registrationDeadline);

        if (end < start) return "End date cannot be before start date";
        if (deadline > start)
            return "Registration deadline should be before the tournament starts";

        return null;
    }

    // Submit form
    async function handleSubmit() {
        error = null;
        success = false;
        loading = true;

        // Validate form
        const validationError = validateForm();
        if (validationError) {
            error = validationError;
            loading = false;
            return;
        }

        try {
            // Prepare tournament data
            const tournamentData = {
                name,
                description,
                sport,
                start_date: startDate,
                end_date: endDate,
                registration_deadline: registrationDeadline,
                max_teams: parseInt(maxTeams),
            };

            // Add ID if in edit mode
            if (isEditMode && tournament.id) {
                tournamentData.id = tournament.id;
            }

            // Create or update tournament
            if (isEditMode) {
                await updateTournament(tournament.id, tournamentData);
            } else {
                await createTournament(tournamentData);
            }

            // Success!
            success = true;

            // Reset form or redirect after short delay
            setTimeout(() => {
                if (onComplete) onComplete();
            }, 2000);
        } catch (err) {
            error = err.message;
        } finally {
            loading = false;
        }
    }
</script>

{#if success}
    <Alert color="green" class="mb-4">
        <span class="font-medium">Success!</span> Tournament has been {isEditMode
            ? "updated"
            : "created"} successfully.
    </Alert>
{/if}

{#if error}
    <Alert color="red" class="mb-4">
        <span class="font-medium">Error:</span>
        {error}
    </Alert>
{/if}

<form on:submit|preventDefault={handleSubmit} class="space-y-6">
    <div>
        <Label for="name" class="mb-2">Tournament Name</Label>
        <Input
            id="name"
            bind:value={name}
            placeholder="Enter tournament name"
            required
        />
    </div>

    <div>
        <Label for="description" class="mb-2">Description</Label>
        <Textarea
            id="description"
            bind:value={description}
            placeholder="Enter tournament description"
            rows="3"
        />
    </div>

    <div>
        <Label for="sport" class="mb-2">Sport</Label>
        <Select id="sport" bind:value={sport} required>
            <option value="" disabled>Select a sport</option>
            {#each sportsList as sportOption}
                <option value={sportOption}>{sportOption}</option>
            {/each}
        </Select>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
            <Label for="start-date" class="mb-2">Start Date</Label>
            <Input
                id="start-date"
                type="date"
                bind:value={startDate}
                required
            />
        </div>

        <div>
            <Label for="end-date" class="mb-2">End Date</Label>
            <Input id="end-date" type="date" bind:value={endDate} required />
        </div>

        <div>
            <Label for="registration-deadline" class="mb-2"
                >Registration Deadline</Label
            >
            <Input
                id="registration-deadline"
                type="date"
                bind:value={registrationDeadline}
                required
            />
        </div>
    </div>

    <div>
        <Label for="max-teams" class="mb-2">Maximum Teams</Label>
        <Input
            id="max-teams"
            type="number"
            bind:value={maxTeams}
            min="1"
            max="100"
            required
        />
    </div>

    <div class="flex justify-end gap-4">
        <Button type="button" color="alternative" on:click={onComplete}
            >Cancel</Button
        >
        <Button type="submit" color="blue" disabled={loading}>
            {loading
                ? isEditMode
                    ? "Updating..."
                    : "Creating..."
                : isEditMode
                  ? "Update Tournament"
                  : "Create Tournament"}
        </Button>
    </div>
</form>
