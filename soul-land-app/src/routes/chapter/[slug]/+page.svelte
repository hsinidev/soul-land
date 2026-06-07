<script lang="ts">
    import { page } from "$app/state";
    import chapters from "$lib/chapters.json";
    import { onMount, tick } from "svelte";
    import { fly, fade } from "svelte/transition";

    let slug = $derived(page.params.slug);
    let chapter = $derived(chapters.find(c => c.folder === slug));
    
    let currentIndex = $derived(chapters.findIndex(c => c.folder === slug));
    let nextChapter = $derived(chapters[currentIndex + 1]);
    let prevChapter = $derived(chapters[currentIndex - 1]);

    let scrollY = $state(0);
    let scrollHeight = $state(0);
    let clientHeight = $state(0);
    
    let progress = $derived(scrollHeight > clientHeight ? (scrollY / (scrollHeight - clientHeight)) * 100 : 0);
    let readingMode = $state('vertical'); // 'vertical' or 'horizontal'
    let showControls = $state(true);
    let lastScrollY = $state(0);
    let showDropdown = $state(false);
    let searchTerm = $state('');

    let filteredChapters = $derived(
        chapters.filter(ch => 
            ch.num.toString().includes(searchTerm) || 
            ch.title.toLowerCase().includes(searchTerm.toLowerCase())
        )
    );

    function toggleMode() {
        readingMode = readingMode === 'vertical' ? 'horizontal' : 'vertical';
        tick().then(updateDimensions);
    }

    function preloadNextChapter() {
        if (!nextChapter) return;
        const limit = 5; // Preload first 5 images of next chapter
        nextChapter.images.slice(0, limit).forEach(img => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'image';
            link.href = `/manga/Soul Land/${nextChapter.folder}/${img}`;
            document.head.appendChild(link);
        });
    }

    function handleScroll() {
        scrollY = window.scrollY;
        showControls = scrollY < lastScrollY || scrollY < 100;
        lastScrollY = scrollY;
    }

    function handleClickOutside(event: MouseEvent) {
        const dropdown = document.querySelector('.custom-dropdown');
        if (showDropdown && dropdown && !dropdown.contains(event.target as Node)) {
            showDropdown = false;
        }
    }

    onMount(() => {
        window.addEventListener('scroll', handleScroll);
        window.addEventListener('click', handleClickOutside);
        updateDimensions();
        preloadNextChapter();
        return () => {
            window.removeEventListener('scroll', handleScroll);
            window.removeEventListener('click', handleClickOutside);
        };
    });

    function updateDimensions() {
        scrollHeight = document.documentElement.scrollHeight;
        clientHeight = document.documentElement.clientHeight;
    }

    $effect(() => {
        if (slug) {
            window.scrollTo(0, 0);
            tick().then(updateDimensions);
        }
    });
</script>

<svelte:head>
    {#if chapter}
        <title>Read Soul Land: Legend of The Gods' Realm - {chapter.title} | Soul Land Online</title>
        <meta name="description" content="Read Soul Land Chapter: {chapter.title} online. Explore the legend of the gods' realm with our premium spirit-infused manga reader." />
        <meta property="og:title" content="Soul Land: Legend of The Gods' Realm - {chapter.title}" />
        <meta property="og:description" content="Continue the journey of Tang San in Chapter: {chapter.title}. High quality images and seamless reading." />
        <link rel="canonical" href="https://readsoulland.com/chapter/{encodeURIComponent(chapter.folder)}/" />
    {/if}
</svelte:head>

<svelte:window bind:scrollY on:resize={updateDimensions} />

{#if chapter}
    <div class="reader-container">
        <!-- Progress Bar -->
        <div class="progress-bar" style="width: {progress}%"></div>

        <!-- Sticky Header Controls -->
        <header class="reader-header" class:hidden={!showControls}>
            <div class="header-left">
                <a href="/" class="back-link" aria-label="Back to home">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
                </a>
                <div class="chapter-info">
                    <span class="series-name">Soul Land</span>
                    <h1 class="chapter-title">Ch.{chapter.num.toString().padStart(3, '0')} - {chapter.title}</h1>
                </div>
            </div>
            
            <div class="header-right">
                <button class="mode-toggle" onclick={toggleMode}>
                    {readingMode === 'vertical' ? '⇅ Strip' : '⇄ Page'}
                </button>
                <div class="custom-dropdown">
                    <button 
                        class="ch-select-btn" 
                        onclick={() => showDropdown = !showDropdown}
                        aria-label="Select chapter"
                        aria-expanded={showDropdown}
                    >
                        Ch.{chapter.num.toString().padStart(3, '0')}
                        <svg class:rotate={showDropdown} width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
                    </button>

                    {#if showDropdown}
                        <div class="dropdown-panel glass" transition:fade={{duration: 150}}>
                            <div class="search-box">
                                <input 
                                    type="text" 
                                    placeholder="Search chapter..." 
                                    bind:value={searchTerm}
                                    autofocus
                                />
                            </div>
                            <div class="chapter-list">
                                {#each filteredChapters as ch}
                                    <a 
                                        href="/chapter/{ch.folder}" 
                                        class="chapter-item" 
                                        class:active={ch.folder === slug}
                                        onclick={() => showDropdown = false}
                                    >
                                        <span class="ch-num">Ch.{ch.num.toString().padStart(3, '0')}</span>
                                        <span class="ch-name">{ch.title}</span>
                                    </a>
                                {/each}
                                {#if filteredChapters.length === 0}
                                    <div class="no-results">No chapters found</div>
                                {/if}
                            </div>
                        </div>
                    {/if}
                </div>
                
                <div class="nav-btns">
                    {#if prevChapter}
                        <a href="/chapter/{prevChapter.folder}" class="nav-btn">Prev</a>
                    {/if}
                    {#if nextChapter}
                        <a href="/chapter/{nextChapter.folder}" class="nav-btn next">Next</a>
                    {/if}
                </div>
            </div>
        </header>

        <!-- Manga Content -->
        <main class="images-strip {readingMode}">
            {#each chapter.images as img, i}
                <div class="image-wrapper">
                    <img 
                        src="/manga/Soul Land/{chapter.folder}/{img}" 
                        alt="Page {i + 1}" 
                        class="manga-page"
                        onload={updateDimensions}
                    />
                </div>
            {/each}
        </main>

        <!-- Bottom Navigation -->
        <footer class="reader-footer">
            <div class="footer-content">
                <p>You've reached the end of Chapter {chapter.num}</p>
                <div class="footer-actions">
                    {#if prevChapter}
                        <a href="/chapter/{prevChapter.folder}" class="btn-footer">Previous Chapter</a>
                    {/if}
                    <a href="/" class="btn-footer">Back to Home</a>
                    {#if nextChapter}
                        <a href="/chapter/{nextChapter.folder}" class="btn-footer highlighted">Next: Chapter {nextChapter.num}</a>
                    {/if}
                </div>
            </div>
        </footer>
    </div>
{/if}

<style>
    .reader-container {
        background: #000;
        min-height: 100vh;
    }

    .progress-bar {
        position: fixed;
        top: 0;
        left: 0;
        height: 4px;
        background: linear-gradient(to right, var(--primary), var(--spirit-blue));
        z-index: 2000;
        transition: width 0.1s linear;
        box-shadow: 0 0 10px var(--spirit-blue);
    }

    .reader-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 70px;
        background: var(--glass);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 1.5rem;
        z-index: 1000;
        transition: transform 0.3s ease;
    }

    .reader-header.hidden {
        transform: translateY(-100%);
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }

    .back-link {
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.05);
        transition: all 0.3s;
    }

    .back-link:hover {
        background: rgba(255, 255, 255, 0.1);
        color: var(--spirit-blue);
    }

    .chapter-info {
        display: flex;
        flex-direction: column;
    }

    .series-name {
        font-size: 0.75rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .chapter-title {
        font-size: 1rem;
        font-weight: 700;
        margin: 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 300px;
    }

    .header-right {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }

    .custom-dropdown {
        position: relative;
    }

    .ch-select-btn {
        background: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid var(--border);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
    }

    .ch-select-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: var(--spirit-blue);
    }

    .ch-select-btn svg {
        transition: transform 0.3s;
        color: var(--spirit-blue);
    }

    .ch-select-btn svg.rotate {
        transform: rotate(180deg);
    }

    .dropdown-panel {
        position: absolute;
        top: calc(100% + 10px);
        right: 0;
        width: 300px;
        max-height: 400px;
        border-radius: 12px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        z-index: 1100;
    }

    .search-box {
        padding: 0.75rem;
        border-bottom: 1px solid var(--border);
        background: rgba(255,255,255,0.03);
    }

    .search-box input {
        width: 100%;
        background: var(--void);
        border: 1px solid var(--border);
        color: white;
        padding: 0.5rem 0.75rem;
        border-radius: 6px;
        outline: none;
    }

    .search-box input:focus {
        border-color: var(--spirit-blue);
        box-shadow: 0 0 10px rgba(0,210,255,0.2);
    }

    .chapter-list {
        overflow-y: auto;
        padding: 0.5rem;
    }

    .chapter-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.75rem 1rem;
        color: var(--text);
        text-decoration: none;
        border-radius: 8px;
        transition: all 0.2s;
    }

    .chapter-item:hover {
        background: rgba(0, 210, 255, 0.1);
        color: var(--spirit-blue);
    }

    .chapter-item.active {
        background: var(--primary);
        color: white;
    }

    .ch-num {
        font-weight: 700;
        font-family: 'Cinzel', serif;
        font-size: 0.875rem;
    }

    .ch-name {
        font-size: 0.8rem;
        opacity: 0.8;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .no-results {
        padding: 2rem;
        text-align: center;
        color: var(--muted);
        font-size: 0.875rem;
    }

    .nav-btns {
        display: flex;
        gap: 0.75rem;
    }

    .nav-btn {
        padding: 0.5rem 1.25rem;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.05);
        color: white;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.875rem;
        transition: all 0.3s;
        border: 1px solid var(--border);
    }

    .nav-btn:hover {
        background: rgba(255, 255, 255, 0.1);
    }

    .nav-btn.next {
        background: var(--primary);
        border-color: var(--primary);
    }

    .images-strip {
        max-width: 900px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        padding-top: 70px;
    }

    .image-wrapper {
        width: 100%;
        line-height: 0;
    }

    .manga-page {
        width: 100%;
        height: auto;
        display: block;
    }

    .images-strip.horizontal {
        flex-direction: row;
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        padding-top: 0;
        height: 100vh;
    }

    .images-strip.horizontal .image-wrapper {
        min-width: 100vw;
        height: 100vh;
        scroll-snap-align: start;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #000;
    }

    .images-strip.horizontal .manga-page {
        width: auto;
        height: 100%;
        max-width: 100vw;
        object-fit: contain;
    }

    .mode-toggle {
        background: rgba(0, 210, 255, 0.1);
        color: var(--spirit-blue);
        border: 1px solid var(--spirit-blue);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s;
    }

    .mode-toggle:hover {
        background: var(--spirit-blue);
        color: black;
        box-shadow: var(--glow-blue);
    }

    .reader-footer {
        padding: 6rem 2rem;
        background: var(--void);
        text-align: center;
    }

    .footer-content p {
        font-size: 1.25rem;
        color: var(--muted);
        margin-bottom: 2rem;
    }

    .footer-actions {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        flex-wrap: wrap;
    }

    .btn-footer {
        padding: 1rem 2rem;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        color: white;
        text-decoration: none;
        font-weight: 700;
        transition: all 0.3s;
    }

    .btn-footer:hover {
        border-color: var(--spirit-blue);
        transform: translateY(-5px);
    }

    .btn-footer.highlighted {
        background: var(--primary);
        border-color: var(--primary);
        box-shadow: var(--glow-blue);
    }

    @media (max-width: 768px) {
        .chapter-title {
            max-width: 150px;
        }
        .header-right .nav-btns {
            display: none;
        }
    }
</style>
