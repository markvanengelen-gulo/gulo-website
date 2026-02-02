# Gulo AI Website

Official website for Gulo AI - Advanced AI Solutions for Business.

## 🌐 Live Site

The website is deployed at: https://gulo.ai

## 🚀 Technology Stack

- **Framework:** [Astro](https://astro.build/) v5.15.8
- **Language:** TypeScript
- **Hosting:** GitHub Pages with Custom Domain (gulo.ai)
- **Deployment:** Automated via GitHub Actions

## 📁 Project Structure

```
gulo-website/
├── src/
│   ├── pages/              # Routable pages
│   │   ├── index.astro    # Home page
│   │   ├── about.astro    # About page
│   │   ├── services.astro # Services page
│   │   ├── contact.astro  # Contact page
│   │   └── blog/          # Blog posts
│   ├── layouts/           # Layout components
│   │   └── BaseLayout.astro
│   └── styles/            # CSS files
│       └── global.css
├── public/                # Static assets
│   └── .nojekyll         # Required for GitHub Pages
├── .github/
│   └── workflows/
│       └── deploy.yml    # Deployment workflow
└── astro.config.mjs      # Astro configuration
```

## 🛠️ Development

### Prerequisites

- Node.js 20 or higher
- npm

### Setup

1. Clone the repository:
```bash
git clone https://github.com/markvanengelen-gulo/gulo-website.git
cd gulo-website
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The site will be available at `http://localhost:4321`

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run astro` - Run Astro CLI commands

## 📦 Building

To build the site for production:

```bash
npm run build
```

The built site will be in the `dist/` directory.

## 🚢 Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch.

### Deployment Workflow

1. Push changes to `main` branch
2. GitHub Actions workflow builds the site using Astro
3. Built files from `dist/` directory are deployed to GitHub Pages
4. Site is accessible at https://gulo.ai

### Manual Deployment

You can also trigger a deployment manually:
1. Go to the "Actions" tab in GitHub
2. Select the "Deploy to GitHub Pages" workflow
3. Click "Run workflow"

## 📝 Content Management

### Adding New Pages

1. Create a new `.astro` file in `src/pages/`
2. Use the `BaseLayout` component for consistent styling
3. The page will automatically be available at `/{filename}`

Example:
```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
const base = import.meta.env.BASE_URL;
---

<BaseLayout title="Page Title" description="Page description">
  <!-- Your content here -->
</BaseLayout>
```

### Adding Blog Posts

1. Create a new `.astro` file in `src/pages/blog/`
2. Add a link to the post in `src/pages/blog/index.astro`
3. Use the `base` variable for all internal links

### Internal Links

Always use the `base` variable for internal links to ensure compatibility:

```astro
---
const base = import.meta.env.BASE_URL;
---

<a href={`${base}about`}>About</a>
<a href={`${base}blog`}>Blog</a>
```

## 🔧 Configuration

### Custom Domain Setup

The site is configured for custom domain deployment (gulo.ai):
- **Site URL:** `https://gulo.ai`
- **Base Path:** `/`

These are configured in `astro.config.mjs`.

The `public/CNAME` file contains the custom domain and is automatically deployed with the site.

### Switching Between Custom Domain and GitHub Pages Subdirectory

**For custom domain (current setup):**
1. Update `astro.config.mjs`:
   ```js
   export default defineConfig({
     site: 'https://gulo.ai',
     base: '/',
   });
   ```
2. Add a `CNAME` file to `public/` directory with your domain
3. Configure your DNS settings to point to GitHub Pages

**For GitHub Pages subdirectory deployment:**
1. Update `astro.config.mjs`:
   ```js
   export default defineConfig({
     site: 'https://markvanengelen-gulo.github.io',
     base: '/gulo-website/',
   });
   ```
2. Remove the `CNAME` file from `public/` directory

After changing the configuration, rebuild the site with `npm run build` before deploying.

## 🎨 Styling

Global styles are in `src/styles/global.css`. The site uses:
- CSS custom properties for theming
- Responsive design with mobile-first approach
- Gradient backgrounds and modern UI components

## 📄 Pages

- **Home** (`/`) - Main landing page with services overview
- **About** (`/about`) - Company information and mission
- **Services** (`/services`) - Detailed service offerings
- **Blog** (`/blog`) - Technical articles and insights
- **Contact** (`/contact`) - Contact information and form

## 🔍 SEO

The site includes:
- Meta descriptions on all pages
- Semantic HTML structure
- Responsive viewport settings
- Proper heading hierarchy

## 📞 Contact

For questions or issues with the website, please contact info@gulo.ai

## 📄 License

All rights reserved © 2026 Gulo AI