<script>
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { isAdmin, isAuthenticated } from "../../../../stores/userStore";
    import { Card, Heading } from "flowbite-svelte";
    import TournamentForm from "../../../../components/TournamentForm.svelte";

    // Redirect if not authenticated
    onMount(() => {
        if (!$isAuthenticated || !$isAdmin) {
            goto("/login");
        }
    });

    // Handle completion of form
    function handleComplete() {
        goto("/admin");
    }
</script>

<div class="container mx-auto py-8">
    <Heading tag="h1" class="mb-6">Create New Tournament</Heading>

    <Card padding="xl">
        <TournamentForm onComplete={handleComplete} />
    </Card>
</div>
