<!-- 
  Main layout component that provides consistent structure across all pages
  Includes navigation, footer, and authentication state management
-->
<script>
    import { onMount } from "svelte";
    import {
        Navbar,
        NavBrand,
        NavLi,
        NavUl,
        NavHamburger,
        Button,
        Footer,
    } from "flowbite-svelte";
    import {
        isAuthenticated,
        isAdmin,
        user,
        logout,
    } from "../stores/userStore";

    // Handle logout action
    function handleLogout() {
        logout();
        window.location.href = "/";
    }
</script>

<!-- Global styles -->
<svelte:head>
    <title>Sports Council - Tournament System</title>
</svelte:head>

<div class="app min-h-screen flex flex-col">
    <!-- Navigation header -->
    <Navbar class="px-4 lg:px-6 py-3 bg-blue-800 text-white">
        <NavBrand href="/">
            <span class="self-center whitespace-nowrap text-xl font-semibold"
                >Sports Council</span
            >
        </NavBrand>

        <NavHamburger />

        <NavUl>
            <NavLi href="/">Home</NavLi>
            <NavLi href="/tournaments">Tournaments</NavLi>

            {#if $isAuthenticated}
                {#if $isAdmin}
                    <NavLi href="/admin">Admin</NavLi>
                {/if}
                <li>
                    <span class="px-3 py-2 text-sm"
                        >Welcome, {$user?.username}</span
                    >
                </li>
                <li>
                    <Button
                        size="sm"
                        outline
                        color="light"
                        on:click={handleLogout}>Logout</Button
                    >
                </li>
            {:else}
                <NavLi href="/login">Login</NavLi>
            {/if}
        </NavUl>
    </Navbar>

    <!-- Main content -->
    <main class="flex-1 container mx-auto px-4 py-8">
        <slot />
    </main>

    <!-- Footer -->
    <Footer class="p-4 bg-gray-800 text-white">
        <div class="flex justify-center items-center">
            <span class="text-sm"
                >© 2025 IIIT Hyderabad Sports Council - Recruitment Task</span
            >
        </div>
    </Footer>
</div>

<style>
    /* Add any global styles here */
    :global(body) {
        font-family: "Poppins", sans-serif;
    }
</style>
