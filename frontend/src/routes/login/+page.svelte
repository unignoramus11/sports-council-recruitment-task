<script>
    import { Card, Label, Input, Button, Alert } from "flowbite-svelte";
    import { login } from "../../stores/userStore";
    import { goto } from "$app/navigation";

    // Form data and state
    let username = "";
    let password = "";
    let error = null;
    let loading = false;

    // Handle login form submission
    async function handleSubmit() {
        error = null;
        loading = true;

        if (!username || !password) {
            error = "Please enter both username and password";
            loading = false;
            return;
        }

        try {
            const result = await login(username, password);

            if (result === true) {
                goto("/admin");
            } else if (result.error) {
                error = result.error;
            }
        } catch (err) {
            error = err.message || "Login failed. Please try again.";
        } finally {
            loading = false;
        }
    }
</script>

<div class="flex justify-center items-center min-h-[80vh]">
    <Card padding="xl" class="w-full max-w-md">
        <h2 class="text-2xl font-bold mb-6 text-center">Admin Login</h2>

        {#if error}
            <Alert color="red" class="mb-4">
                <span class="font-medium">{error}</span>
            </Alert>
        {/if}

        <form on:submit|preventDefault={handleSubmit} class="space-y-4">
            <div>
                <Label for="username" class="mb-2">Username</Label>
                <Input
                    id="username"
                    bind:value={username}
                    placeholder="Enter username"
                    required
                />
            </div>

            <div>
                <Label for="password" class="mb-2">Password</Label>
                <Input
                    id="password"
                    type="password"
                    bind:value={password}
                    placeholder="••••••••"
                    required
                />
            </div>

            <Button
                type="submit"
                class="w-full"
                color="blue"
                disabled={loading}
            >
                {loading ? "Logging in..." : "Login"}
            </Button>
        </form>

        <div class="mt-4 text-center text-sm text-gray-500">
            <p>For testing purposes:</p>
            <p class="font-semibold">Username: admin / Password: password</p>
        </div>
    </Card>
</div>
