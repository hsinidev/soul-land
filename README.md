# Celestial Cultivation Portal

> **Vibe Focus:** Celestial Cultivation / Soul Ring HUD Style  
> **Tech Stack:** SvelteKit + Vite + Tailwind CSS (App) // Static HTML/JS (Root)

Welcome to the **Celestial Cultivation Portal** web portal. This is a high-performance, immersive manga reader site designed specifically for fans of the series. The project leverages modern web optimization techniques to deliver a fast, localized, and beautiful experience.

---

## 🌟 Key Features

- Spirit beast soul ring glow effects on UI components.
- Next-gen SvelteKit layout with file-based routing and fast load times.
- Offline service worker caching for seamless reading sessions.
- Python automation scripts to generate backing database files.

---

## 🛠️ Getting Started

### 📋 Prerequisites
- **For Web Server:** Python 3.10+ (to serve static files or run generators) or Node.js 18+ (if package dependencies are needed).
- **GitHub CLI (`gh`)**: Recommended for pushing updates.

### 🔑 API Key Configuration
This project includes automated content generation and SEO optimization scripts that use the **Zhipu AI / BigModel API**. 

To utilize these scripts:
1. Copy the `.env.example` file to create a `.env` file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your API key:
   ```env
   BIGMODEL_API_KEY=your_actual_api_key_here
   ```
   *Note: If you have multiple keys, you can specify them as a comma-separated list.*

---

## 🚀 Local Development

To launch the modern SvelteKit web application, navigate and run:
```bash
cd soul-land-app && npm install
npm run dev
```

Then open your browser and navigate to the local server URL (usually `http://localhost:8000` or `http://localhost:5173`).

---

## 🤖 Content Generation & Automation
The project is equipped with local AI-powered generation scripts to build and update the site content dynamically.

You can run these scripts to regenerate and optimize the portal content:

- **`python build.py`**: Builds the root static HTML portal.
- **`python generate_data.py`**: Compiles character spirit matrices and chapter details.


---

## 📦 Production Deployment

Compile the SvelteKit app:
```bash
cd soul-land-app
npm run build
```
Deploy static assets from the build directory.

- **Ignored Assets:** Large `manga/` chapter image directories and local archives are excluded from this repository (configured in `.gitignore`) for performance and size constraints. Ensure image files are uploaded directly to your hosting server's path structure.
- **SEO Ready:** Sitemap (`sitemap.xml`) and `.htaccess` file rules are fully configured to rewrite paths and provide Google-friendly crawler access.
