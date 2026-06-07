<script lang="ts">
    import "../app.css";
    let { children } = $props();
</script>

<svelte:head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- SEO Global -->
    <meta name="robots" content="index, follow" />
    <meta name="author" content="Soul Land Enthusiasts" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Soul Land Online" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta property="og:image" content="/hero.png" />
    <meta name="twitter:image" content="/hero.png" />
</svelte:head>

<div class="app-container">
    {@render children()}
</div>

<style>
    :global(:root) {
        --primary: #4f46e5;
        --spirit-blue: #00d2ff;
        --spirit-gold: #f5a623;
        --void: #0a0a0f;
        --surface: #12121a;
        --glass: rgba(10, 10, 15, 0.7);
        --text: #e2e8f0;
        --muted: #94a3b8;
        --border: rgba(79, 70, 229, 0.2);
        --glow-blue: 0 0 30px rgba(0, 210, 255, 0.3);
        --glow-gold: 0 0 30px rgba(245, 166, 35, 0.3);
    }

    :global(body) {
        background-color: var(--void);
        color: var(--text);
        font-family: 'Plus Jakarta Sans', sans-serif;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
        -webkit-font-smoothing: antialiased;
    }

    .app-container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }

    :global(::-webkit-scrollbar) {
        width: 8px;
    }

    :global(::-webkit-scrollbar-track) {
        background: var(--void);
    }

    :global(::-webkit-scrollbar-thumb) {
        background: linear-gradient(to bottom, var(--primary), var(--spirit-blue));
        border-radius: 4px;
    }
</style>
