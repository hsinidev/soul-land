<script lang="ts">
    import { fade, fly } from 'svelte/transition';
</script>

<svelte:head>
    <title>Characters | Soul Land: Legend of The Gods' Realm</title>
    <meta name="description" content="Meet the Shrek Seven Devils, Tang San, and the powerful spirit masters of the Gods' Realm." />
</svelte:head>

<nav class="nav">
    <div class="nav-content">
        <a href="/" class="logo">
            <span class="logo-icon">SL</span>
            <span class="logo-text">Soul Land</span>
        </a>
        <div class="nav-links">
            <a href="/characters" class="nav-link active">Characters</a>
            <a href="/about" class="nav-link">About</a>
        </div>
    </div>
</nav>

<main class="container">
    <div class="hero-mini" in:fade={{ duration: 1000 }}>
        <h1 class="title">Spirit Masters</h1>
        <p class="subtitle">Witness the awakening of the Gods' Realm</p>
    </div>

    <div class="characters-grid">
        <div class="char-card" in:fly={{ y: 50, delay: 200, duration: 800 }}>
            <div class="char-image placeholder">TS</div>
            <div class="char-info">
                <h3>Tang San</h3>
                <span class="rank">Sea God / Asura God</span>
                <p>The leader of the Shrek Seven Devils and the most powerful soul master in history.</p>
            </div>
        </div>
        
        <div class="char-card" in:fly={{ y: 50, delay: 400, duration: 800 }}>
            <div class="char-image placeholder">XW</div>
            <div class="char-info">
                <h3>Xiao Wu</h3>
                <span class="rank">First Human-Spirit Hybrid</span>
                <p>The soul of Tang San's life and a powerhouse in her own right.</p>
            </div>
        </div>

        <div class="char-card coming-soon" in:fly={{ y: 50, delay: 600, duration: 800 }}>
            <div class="char-info">
                <h3>More Coming Soon</h3>
                <p>We are awakening more spirit profiles. Check back soon for the full Shrek Seven Devils roster.</p>
            </div>
        </div>
    </div>
</main>

<style>
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 100px 20px 60px;
    }

    .nav {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 70px;
        background: var(--glass);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid var(--border);
        z-index: 1000;
        display: flex;
        align-items: center;
    }

    .nav-content {
        max-width: 1400px;
        margin: 0 auto;
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 40px;
    }

    .logo {
        display: flex;
        align-items: center;
        gap: 12px;
        text-decoration: none;
        color: white;
    }

    .logo-icon {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, var(--primary), var(--spirit-blue));
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-family: 'Cinzel', serif;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
    }

    .logo-text {
        font-family: 'Cinzel', serif;
        font-weight: 700;
        font-size: 1.25rem;
        letter-spacing: 1px;
    }

    .nav-links {
        display: flex;
        gap: 30px;
    }

    .nav-link {
        color: var(--text);
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
        opacity: 0.7;
        transition: all 0.3s ease;
    }

    .nav-link:hover, .nav-link.active {
        opacity: 1;
        color: var(--spirit-blue);
    }

    .hero-mini {
        text-align: center;
        margin-bottom: 60px;
    }

    .title {
        font-family: 'Cinzel', serif;
        font-size: 3.5rem;
        margin: 0;
        background: linear-gradient(to bottom, #fff, var(--spirit-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0, 210, 255, 0.2);
    }

    .subtitle {
        color: var(--muted);
        font-size: 1.25rem;
        margin-top: 10px;
    }

    .characters-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 30px;
    }

    .char-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 20px;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: default;
    }

    .char-card:hover {
        transform: translateY(-10px);
        border-color: var(--primary);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }

    .char-image {
        height: 250px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 4rem;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.1);
        background: linear-gradient(45deg, #1a1a2e, #16213e);
        position: relative;
    }

    .char-image::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 100px;
        background: linear-gradient(to top, var(--surface), transparent);
    }

    .char-info {
        padding: 30px;
    }

    .char-info h3 {
        margin: 0;
        font-family: 'Cinzel', serif;
        font-size: 1.5rem;
        color: var(--spirit-blue);
    }

    .rank {
        display: block;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: var(--spirit-gold);
        margin: 5px 0 15px;
    }

    .char-info p {
        color: var(--muted);
        line-height: 1.6;
        margin: 0;
    }

    .coming-soon {
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        border-style: dashed;
        background: transparent;
    }

    @media (max-width: 768px) {
        .title { font-size: 2.5rem; }
        .nav-content { padding: 0 20px; }
        .nav-links { display: none; }
    }
</style>
