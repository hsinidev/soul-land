<script lang="ts">
    import chapters from "$lib/chapters.json";
    import { onMount } from "svelte";
    import { fade, fly, scale } from "svelte/transition";

    let limit = $state(30);
    let searchQuery = $state("");
    let mounted = $state(false);

    const filteredChapters = $derived(
        searchQuery 
        ? chapters.filter(c => 
            c.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
            c.num.toString().includes(searchQuery)
          )
        : chapters
    );
 
    let displayedChapters = $derived(filteredChapters.slice(0, limit));
    let hasMore = $derived(limit < filteredChapters.length);

    // Dynamic Bento Logic
    const latestChapters = $derived(chapters.slice(-6).reverse());
    const trendingChapters = $derived(chapters.slice(40, 46));

    onMount(() => {
        mounted = true;
    });

    function loadMore() {
        limit += 30;
    }
</script>

<svelte:head>
    <title>Soul Land: Legend of The Gods' Realm | Read Manga Online</title>
    <meta name="description" content="Read Soul Land: Legend of The Gods' Realm (Douluo Dalu) manga online. Join Tang San in a world of spirits, spirit rings, and divine power. High-quality images and fast reader." />
    <meta property="og:title" content="Soul Land: Legend of The Gods' Realm | Free Manga Reader" />
    <meta property="og:description" content="Dive into the epic legend of the gods' realm. Read all Soul Land chapters with our premium lightning-fast reader." />
    <link rel="canonical" href="https://readsoulland.com/" />
</svelte:head>

<nav class="nav">
    <div class="nav-content">
        <a href="/" class="logo">
            <span class="logo-icon">SL</span>
            <span class="logo-text">Soul Land</span>
        </a>
        <div class="search-container">
            <input 
                type="text" 
                placeholder="Search chapters..." 
                bind:value={searchQuery}
                class="search-input"
            />
        </div>
        <div class="nav-links">
            <a href="/characters" class="nav-link">Characters</a>
            <a href="/about" class="nav-link">About</a>
        </div>
    </div>
</nav>

<main class="container">
    <section class="hero">
        <div class="hero-content" in:fly={{ y: 50, duration: 1000 }}>
            <span class="badge">EPIC MANGA SERIES</span>
            <h1 class="hero-title">
                LEGEND OF THE<br/>
                <span class="text-glow animate-flicker">GODS' REALM</span>
            </h1>
            <div class="title-flare"></div>
            <p class="hero-desc">
                Follow Tang San's journey in a world where martial spirits determine one's fate. 
                Experience the peak of cultivation and spirit power.
            </p>
            <div class="hero-actions">
                <a href="/chapter/{chapters[0].folder}" class="btn btn-primary">Start Reading</a>
                <a href="#chapters" class="btn btn-outline">Browse Archive</a>
            </div>
        </div>
        <div class="hero-visual" in:scale={{ start: 0.9, duration: 1200 }}>
            <div class="art-card">
                <img src="/hero.png" alt="Soul Land Art" class="hero-image" />
                <div class="art-overlay"></div>
                <div class="electric-arcs">
                    <div class="arc arc-1"></div>
                    <div class="arc arc-2"></div>
                </div>
            </div>
        </div>

        <!-- Electric Background Elements -->
        <div class="hero-bg-effects">
            <div class="spirit-grid"></div>
            <div class="lightning-container">
                {#each Array(5) as _, i}
                    <svg class="lightning bolt-{i}" viewBox="0 0 100 100" preserveAspectRatio="none">
                        <path d="M50,0 L40,40 L60,30 L45,100" stroke="var(--spirit-blue)" stroke-width="0.5" fill="none" />
                    </svg>
                {/each}
            </div>
        </div>
    </section>

    <section id="chapters" class="chapters-section">
        <div class="section-header">
            <h2 class="section-title">Chapter <span class="text-blue">Archive</span></h2>
            <div class="controls">
                <!-- Add sorting/filter controls here -->
            </div>
        </div>

        <div class="bento-grid">
            {#each displayedChapters as chapter, i (chapter.folder)}
                <a 
                    href="/chapter/{chapter.folder}" 
                    class="chapter-card"
                    in:fly={{ y: 20, delay: (i % 30) * 20, duration: 500 }}
                >
                    <div class="card-thumb">
                        <img 
                            src="/manga/Soul Land/{chapter.folder}/{chapter.thumb}" 
                            alt={chapter.title} 
                            loading="lazy"
                        />
                        <div class="card-overlay">
                            <span class="ch-num">CH.{chapter.num.toString().padStart(3, '0')}</span>
                        </div>
                    </div>
                    <div class="card-info">
                        <h3 class="ch-title">{chapter.title || `Chapter ${chapter.num}`}</h3>
                        <span class="read-btn">Read Now</span>
                    </div>
                </a>
            {/each}
        </div>

        {#if hasMore}
            <div class="load-more-container">
                <button class="btn-load-more" onclick={loadMore}>
                    <span>Load More Chapters</span>
                    <small>Showing {limit} of {filteredChapters.length}</small>
                </button>
            </div>
        {/if}
    </section>
</main>

<style>
    .container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 2rem;
    }

    /* Navigation */
    .nav {
        position: sticky;
        top: 0;
        z-index: 1000;
        background: var(--glass);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid var(--border);
    }

    .nav-content {
        max-width: 1400px;
        margin: 0 auto;
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 2rem;
    }

    .logo {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        text-decoration: none;
    }

    .logo-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, var(--primary), var(--spirit-blue));
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Cinzel', serif;
        font-weight: 900;
        color: white;
        box-shadow: var(--glow-blue);
    }

    .logo-text {
        font-family: 'Cinzel', serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
    }

    .search-container {
        flex: 1;
        max-width: 500px;
    }

    .search-input {
        width: 100%;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        color: white;
        outline: none;
        transition: all 0.3s;
    }

    .search-input:focus {
        border-color: var(--spirit-blue);
        background: rgba(255, 255, 255, 0.08);
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.1);
    }

    .nav-links {
        display: flex;
        gap: 2rem;
    }

    .nav-link {
        color: var(--muted);
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s;
    }

    .nav-link:hover {
        color: var(--spirit-blue);
    }

    /* Hero Section */
    .hero {
        position: relative;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 4rem;
        padding: 6rem 0;
        align-items: center;
    }

    .hero-title {
        font-family: 'Cinzel', serif;
        font-size: 4.5rem;
        font-weight: 900;
        line-height: 1;
        margin: 1.5rem 0;
    }

    .text-glow {
        background: linear-gradient(to right, #fff, var(--spirit-blue), #fff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0, 210, 255, 0.5), 0 0 40px rgba(0, 210, 255, 0.3);
        animation: shine 3s linear infinite;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    .animate-flicker {
        animation: flicker 4s infinite alternate;
    }

    @keyframes flicker {
        0%, 19.999%, 22%, 62.999%, 64%, 64.919%, 70%, 100% {
            opacity: 1;
            text-shadow: 0 0 20px rgba(0, 210, 255, 0.5), 0 0 40px rgba(0, 210, 255, 0.3);
        }
        20%, 21.999%, 63%, 63.919%, 65%, 69.999% {
            opacity: 0.8;
            text-shadow: none;
        }
    }

    .title-flare {
        position: absolute;
        top: 50%;
        left: 200px;
        width: 400px;
        height: 200px;
        background: radial-gradient(ellipse at center, rgba(0, 210, 255, 0.15) 0%, transparent 70%);
        filter: blur(40px);
        z-index: -1;
        pointer-events: none;
    }

    /* Electric Background Styles */
    .hero-bg-effects {
        position: absolute;
        inset: 0;
        z-index: -2;
        overflow: hidden;
        pointer-events: none;
    }

    .spirit-grid {
        position: absolute;
        inset: 0;
        background-image: 
            linear-gradient(rgba(79, 70, 229, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(79, 70, 229, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
        transform: perspective(1000px) rotateX(60deg) translateY(-100px);
        mask-image: linear-gradient(to bottom, transparent, black, transparent);
    }

    .lightning-container {
        position: absolute;
        inset: 0;
    }

    .lightning {
        position: absolute;
        height: 200px;
        width: 100px;
        filter: drop-shadow(0 0 10px var(--spirit-blue));
        opacity: 0;
    }

    .bolt-0 { top: 10%; left: 15%; animation: bolt-flicker 5s infinite 1s; }
    .bolt-1 { top: 40%; left: 80%; animation: bolt-flicker 7s infinite 3s; rotate: 180deg; }
    .bolt-2 { top: 70%; left: 10%; animation: bolt-flicker 6s infinite 0.5s; }
    .bolt-3 { top: 20%; left: 85%; animation: bolt-flicker 8s infinite 2s; }
    .bolt-4 { top: 60%; left: 75%; animation: bolt-flicker 5s infinite 4s; }

    @keyframes bolt-flicker {
        0%, 9%, 11%, 19%, 21%, 100% { opacity: 0; }
        10%, 20% { opacity: 0.6; }
    }

    .electric-arcs {
        position: absolute;
        inset: 0;
        pointer-events: none;
    }

    .arc {
        position: absolute;
        background: var(--spirit-blue);
        filter: blur(2px);
        box-shadow: 0 0 15px var(--spirit-blue);
    }

    .arc-1 {
        width: 2px;
        height: 100px;
        top: 20%;
        left: -1px;
        animation: arc-move 3s infinite linear;
    }

    .arc-2 {
        height: 2px;
        width: 100px;
        bottom: 20%;
        right: -1px;
        animation: arc-move-h 4s infinite linear;
    }

    @keyframes arc-move {
        0% { transform: translateY(-100%); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateY(200%); opacity: 0; }
    }

    @keyframes arc-move-h {
        0% { transform: translateX(100%); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateX(-200%); opacity: 0; }
    }

    .badge {
        display: inline-block;
        padding: 0.5rem 1.25rem;
        background: rgba(79, 70, 229, 0.2);
        border: 1px solid var(--border);
        border-radius: 99px;
        color: var(--spirit-blue);
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 2px;
    }

    .hero-desc {
        font-size: 1.125rem;
        color: var(--muted);
        line-height: 1.8;
        max-width: 500px;
        margin-bottom: 2.5rem;
    }

    .hero-actions {
        display: flex;
        gap: 1.5rem;
    }

    .btn {
        padding: 1rem 2.5rem;
        border-radius: 12px;
        font-weight: 700;
        text-decoration: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .btn-primary {
        background: linear-gradient(135deg, var(--primary), var(--spirit-blue));
        color: white;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.3);
    }

    .btn-primary:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(79, 70, 229, 0.5);
    }

    .btn-outline {
        border: 2px solid var(--border);
        color: white;
    }

    .btn-outline:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: var(--spirit-blue);
    }

    .hero-visual {
        display: flex;
        justify-content: center;
    }

    .art-card {
        width: 100%;
        max-width: 450px;
        aspect-ratio: 3/4;
        border-radius: 30px;
        overflow: hidden;
        position: relative;
        border: 1px solid var(--border);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5), var(--glow-blue);
    }

    .hero-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .art-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(to top, var(--void) 0%, transparent 50%);
    }

    /* Bento Grid */
    .chapters-section {
        padding: 4rem 0;
    }

    .section-header {
        margin-bottom: 3rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .section-title {
        font-family: 'Cinzel', serif;
        font-size: 2.5rem;
        font-weight: 700;
    }

    .text-blue {
        color: var(--spirit-blue);
    }

    .bento-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1.5rem;
    }

    .chapter-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 20px;
        overflow: hidden;
        text-decoration: none;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .chapter-card:hover {
        transform: translateY(-10px) scale(1.02);
        border-color: var(--spirit-blue);
        box-shadow: 0 15px 45px rgba(0, 210, 255, 0.15);
    }

    .card-thumb {
        position: relative;
        aspect-ratio: 16/9;
        overflow: hidden;
    }

    .card-thumb img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.6s;
    }

    .chapter-card:hover .card-thumb img {
        transform: scale(1.1);
    }

    .card-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
        display: flex;
        align-items: flex-end;
        padding: 1rem;
    }

    .ch-num {
        font-family: 'Cinzel', serif;
        font-weight: 700;
        color: var(--spirit-gold);
        font-size: 1.25rem;
    }

    .card-info {
        padding: 1.5rem;
    }

    .ch-title {
        font-size: 1rem;
        color: white;
        margin-bottom: 1rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .read-btn {
        font-size: 0.875rem;
        font-weight: 700;
        color: var(--spirit-blue);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .load-more-container {
        display: flex;
        justify-content: center;
        padding: 4rem 0;
    }

    .btn-load-more {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--border);
        color: white;
        padding: 1.5rem 4rem;
        border-radius: 20px;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        min-width: 300px;
    }

    .btn-load-more:hover {
        background: rgba(0, 210, 255, 0.05);
        border-color: var(--spirit-blue);
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 210, 255, 0.1);
    }

    .btn-load-more span {
        font-size: 1.25rem;
        font-weight: 800;
        font-family: 'Cinzel', serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .btn-load-more small {
        color: var(--muted);
        font-size: 0.8rem;
    }

    @media (max-width: 1024px) {
        .hero {
            grid-template-columns: 1fr;
            text-align: center;
            gap: 3rem;
        }
        .hero-desc {
            margin-left: auto;
            margin-right: auto;
        }
        .hero-actions {
            justify-content: center;
        }
        .hero-title {
            font-size: 3rem;
        }
    }
</style>
