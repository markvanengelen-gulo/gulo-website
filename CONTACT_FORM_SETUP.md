# Contact Form Email Setup

## Overview
The contact form submits messages **in the background** to [Web3Forms](https://web3forms.com/) and does **not** use `mailto:` or open the visitor's email client. This works on static hosting (GitHub Pages) without needing a backend server.

## Setup Instructions

### 1. Get Your Web3Forms Access Key

1. Visit [https://web3forms.com](https://web3forms.com/)
2. Click "Get Started" or "Create Access Key"
3. Enter the email address where you want to receive form submissions: `mark.vanengelen@gulo.ai`
4. Verify the email address (check your inbox for a verification email)
5. Copy the access key provided

### 2. Configure the Access Key (GitHub Pages / GitHub Actions)

**Do not commit a real key to the repository.** Instead, inject it at build time via a GitHub Actions secret:

1. Go to your repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `WEB3FORMS_ACCESS_KEY`
4. Value: paste your Web3Forms access key
5. Click **Add secret**

The deploy workflow (`deploy.yml`) passes this secret to the Astro build as `PUBLIC_WEB3FORMS_ACCESS_KEY`, and `src/pages/contact.astro` reads it via `import.meta.env.PUBLIC_WEB3FORMS_ACCESS_KEY`.

### 3. Deploy

Push to `main` — GitHub Actions will build and deploy with the access key injected.

## Features

✅ **Background submission** — no redirect, no email client popup  
✅ **Shows "Message Sent Successfully."** after successful submission  
✅ **Shows "Something went wrong. Please try again."** on failure  
✅ **Loading indicator** — button disabled and shows "Sending..." while submitting  
✅ **Form cleared** on success  
✅ **Required field validation** before submission  
✅ **Honeypot anti-spam** — hidden field checked client-side  
✅ **Appointment modal** also uses background submission (no `mailto:`)  
❌ **No `mailto:` fallback** — by design, the form never opens an email client

## Testing

### Development Testing
1. Run `npm run dev` to start the development server
2. Navigate to the contact page at `http://localhost:4321/contact`
3. Fill out the form and click "Send Message"
4. If `PUBLIC_WEB3FORMS_ACCESS_KEY` is not set locally, set it in a `.env` file (do not commit): `PUBLIC_WEB3FORMS_ACCESS_KEY=your_key_here`
5. Check the configured email address for the submission

### Production Testing
1. After deploying to GitHub Pages
2. Visit `https://gulo.ai/contact/`
3. Submit a test message
4. Verify the email is received at `mark.vanengelen@gulo.ai`

## Troubleshooting

### Form not sending emails
- Verify the `WEB3FORMS_ACCESS_KEY` GitHub Actions secret is set correctly
- Check that you verified the email address in Web3Forms
- Open browser DevTools → Network tab, look for the POST to `https://api.web3forms.com/submit`
- Check browser console for any JavaScript errors

## Web3Forms Benefits
- ✨ Free for up to 250 submissions/month
- 🔒 Privacy-focused (GDPR compliant)
- 🚀 No backend required
- 📧 Email notifications with all form data
- 🛡️ Spam protection included
- 📊 Optional dashboard for tracking submissions
