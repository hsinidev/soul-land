import chapters from '$lib/chapters.json';

export const prerender = true;

const website = 'https://readsoulland.com';

export async function GET() {
    const pages = [
        '',
        'about',
        'characters',
        ...chapters.map(c => `chapter/${encodeURIComponent(c.folder)}`)
    ];

    const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages
    .map(page => `
    <url>
        <loc>${website}/${page}${page ? '/' : ''}</loc>
        <changefreq>${page.startsWith('chapter/') ? 'monthly' : 'weekly'}</changefreq>
        <priority>${page === '' ? '1.0' : page.startsWith('chapter/') ? '0.8' : '0.5'}</priority>
    </url>
`).join('')}
</urlset>`.trim();

    return new Response(sitemap, {
        headers: {
            'Content-Type': 'application/xml'
        }
    });
}
