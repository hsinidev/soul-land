<script lang="ts">
    import { fade, fly } from 'svelte/transition';
</script>

<svelte:head>
    <title>About Soul Land | Legend of The Gods' Realm</title>
    <meta name="description" content="Discover the story behind Soul Land: Legend of The Gods' Realm and the continuation of the Shrek Seven Devils' epic journey." />
</svelte:head>

<nav class="nav">
    <div class="nav-content">
        <a href="/" class="logo">
            <span class="logo-icon">SL</span>
            <span class="logo-text">Soul Land</span>
        </a>
        <div class="nav-links">
            <a href="/characters" class="nav-link">Characters</a>
            <a href="/about" class="nav-link active">About</a>
        </div>
    </div>
</nav>

<main class="container">
    <div class="about-card" in:fade={{ duration: 1000 }}>
        <h1 class="title">Legacy of the Gods</h1>
        
        <div class="section" in:fly={{ y: 20, delay: 200 }}>
            <h2>The Story</h2>
            <p>
                Soul Land: Legend of the Gods' Realm (Douluo Dalu: Shenjie Waizhuan) is a spin-off of the original Soul Land series. 
                It takes place millions of years after the events of the first story, where our favorite characters have ascended 
                to the God Realm.
            </p>
        </div>

        <div class="section" in:fly={{ y: 20, delay: 400 }}>
            <h2>The Conflict</h2>
            <p>
                Even in the Realm of Gods, peace is fragile. Confronted by external threats and internal divisions among the 
                Gods, Tang San must lead the others to protect the very foundation of their existence. New spirits, new powers, 
                and divine-level battles await.
            </p>
        </div>

        <div class="section" in:fly={{ y: 20, delay: 600 }}>
            <h2>Our Mission</h2>
            <p>
                We aim to provide the best reading experience for Soul Land fans. Our reader is optimized for high-quality 
                visuals, lightning-fast loads, and an immersive spirit-infused design.
            </p>
        </div>
    </div>
</main>

<style>
    .container {
        max-width: 900px;
        margin: 0 auto;
        padding: 120px 20px 80px;
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

    .about-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 30px;
        padding: 60px;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
    }

    .title {
        font-family: 'Cinzel', serif;
        font-size: 3rem;
        text-align: center;
        margin: 0 0 50px;
        background: linear-gradient(to right, #fff, var(--spirit-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .section {
        margin-bottom: 40px;
    }

    .section h2 {
        font-family: 'Cinzel', serif;
        color: var(--spirit-gold);
        font-size: 1.5rem;
        margin-bottom: 15px;
    }

    .section p {
        color: var(--muted);
        line-height: 1.8;
        font-size: 1.1rem;
        margin: 0;
    }

    @media (max-width: 768px) {
        .about-card { padding: 40px 20px; }
        .title { font-size: 2rem; }
        .nav-content { padding: 0 20px; }
        .nav-links { display: none; }
    }
</style>
