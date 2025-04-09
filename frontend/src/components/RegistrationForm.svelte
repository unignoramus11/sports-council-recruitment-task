<script>
    import {
        Input,
        Label,
        Button,
        Textarea,
        Alert,
        Checkbox,
    } from "flowbite-svelte";
    import { getToken } from "../stores/userStore";

    // Properties
    export let tournamentId;
    export let onComplete = () => {};

    // Form data
    let teamName = "";
    let captainName = "";
    let captainEmail = "";
    let playerNames = ["", ""]; // Start with two player fields
    let loading = false;
    let error = null;
    let success = false;
    let agreeToRules = false;

    // Add new player field
    function addPlayer() {
        playerNames = [...playerNames, ""];
    }

    // Remove player field
    function removePlayer(index) {
        playerNames = playerNames.filter((_, i) => i !== index);
    }

    // Validate form
    function validateForm() {
        if (!teamName.trim()) return "Team name is required";
        if (!captainName.trim()) return "Captain name is required";
        if (!captainEmail.trim()) return "Captain email is required";
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(captainEmail))
            return "Please enter a valid email";

        // Filter out empty player names
        const validPlayerNames = playerNames.filter(
            (name) => name.trim() !== "",
        );
        if (validPlayerNames.length < 1)
            return "At least one player is required";

        if (!agreeToRules) return "You must agree to the tournament rules";

        return null;
    }

    // Submit form
    async function submitRegistration() {
        // Reset state
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

        // Filter out empty player names
        const validPlayerNames = playerNames.filter(
            (name) => name.trim() !== "",
        );

        try {
            // Prepare registration data
            const registrationData = {
                tournament_id: tournamentId,
                team_name: teamName,
                captain_name: captainName,
                captain_email: captainEmail,
                player_names: validPlayerNames,
            };

            // Send registration to API
            const response = await fetch("/api/registrations", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(registrationData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(
                    errorData.detail || "Failed to register for tournament",
                );
            }

            // Success!
            success = true;

            // Reset form after short delay
            setTimeout(() => {
                if (onComplete) onComplete();
            }, 3000);
        } catch (err) {
            error = err.message;
        } finally {
            loading = false;
        }
    }
</script>

{#if success}
    <Alert color="green" class="mb-4">
        <span class="font-medium">Success!</span> Your team has been registered successfully.
    </Alert>
{:else}
    {#if error}
        <Alert color="red" class="mb-4">
            <span class="font-medium">Error:</span>
            {error}
        </Alert>
    {/if}

    <form on:submit|preventDefault={submitRegistration} class="space-y-6">
        <div>
            <Label for="team-name" class="mb-2">Team Name</Label>
            <Input
                id="team-name"
                bind:value={teamName}
                placeholder="Enter your team name"
                required
            />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
                <Label for="captain-name" class="mb-2">Captain Name</Label>
                <Input
                    id="captain-name"
                    bind:value={captainName}
                    placeholder="Enter captain name"
                    required
                />
            </div>

            <div>
                <Label for="captain-email" class="mb-2">Captain Email</Label>
                <Input
                    id="captain-email"
                    bind:value={captainEmail}
                    placeholder="Enter captain email"
                    type="email"
                    required
                />
            </div>
        </div>

        <div>
            <div class="flex justify-between items-center mb-2">
                <Label>Players</Label>
                <Button
                    size="xs"
                    color="light"
                    on:click={addPlayer}
                    type="button"
                >
                    + Add Player
                </Button>
            </div>

            <div class="space-y-3">
                {#each playerNames as playerName, index}
                    <div class="flex gap-2">
                        <Input
                            bind:value={playerNames[index]}
                            placeholder={`Player ${index + 1} name`}
                        />
                        {#if index > 0}
                            <Button
                                size="xs"
                                color="red"
                                on:click={() => removePlayer(index)}
                                type="button"
                            >
                                &times;
                            </Button>
                        {/if}
                    </div>
                {/each}
            </div>

            <p class="text-sm text-gray-500 mt-2">
                Add all players that will participate in the tournament.
            </p>
        </div>

        <div class="flex items-start">
            <Checkbox id="agree" bind:checked={agreeToRules} />
            <Label for="agree" class="ml-2">
                I agree to the tournament rules and regulations
            </Label>
        </div>

        <div class="flex justify-end gap-4">
            <Button type="button" color="alternative" on:click={onComplete}
                >Cancel</Button
            >
            <Button type="submit" color="blue" disabled={loading}>
                {loading ? "Submitting..." : "Register Team"}
            </Button>
        </div>
    </form>
{/if}
