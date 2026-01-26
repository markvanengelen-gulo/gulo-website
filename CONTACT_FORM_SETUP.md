# Contact Form Email Setup

## Overview
The contact form uses [Web3Forms](https://web3forms.com/) to send emails directly to `mark.vanengelen@gulo.ai` without requiring a backend server. This is ideal for static sites hosted on GitHub Pages.

## Setup Instructions

### 1. Get Your Web3Forms Access Key

1. Visit [https://web3forms.com](https://web3forms.com/)
2. Click "Get Started" or "Create Access Key"
3. Enter the email address where you want to receive form submissions: `mark.vanengelen@gulo.ai`
4. Verify the email address (check your inbox for a verification email)
5. Copy the access key provided

### 2. Configure the Contact Form

1. Open `src/pages/contact.astro`
2. Find the line with `<input type="hidden" name="access_key" value="YOUR_ACCESS_KEY_HERE">`
3. Replace `YOUR_ACCESS_KEY_HERE` with your actual Web3Forms access key
4. Save the file

### 3. Deploy

Once you've updated the access key:
- Commit and push your changes to the main branch
- GitHub Actions will automatically build and deploy the site
- The contact form will now send emails to `mark.vanengelen@gulo.ai`

## Features

✅ **Email Notifications**: Form submissions are sent directly to `mark.vanengelen@gulo.ai`
✅ **Loading Indicator**: Shows "Sending..." while the form is being submitted
✅ **Success/Error Messages**: Users receive clear feedback after submission
✅ **Form Validation**: All required fields are validated before submission
✅ **Fallback Support**: If Web3Forms is not configured, the form falls back to mailto links

## Testing

### Development Testing
1. Run `npm run dev` to start the development server
2. Navigate to the contact page at `http://localhost:4321/gulo-website/contact`
3. Fill out the form and click "Send Message"
4. Check the configured email address for the submission

### Production Testing
1. After deploying to GitHub Pages
2. Visit the live site contact page
3. Submit a test form
4. Verify the email is received at `mark.vanengelen@gulo.ai`

## Troubleshooting

### Form not sending emails
- Verify the access key is correctly configured
- Check that you verified the email address in Web3Forms
- Check browser console for any JavaScript errors
- Ensure the email address `mark.vanengelen@gulo.ai` is correct

### Fallback to mailto
If the access key is not configured or is set to `YOUR_ACCESS_KEY_HERE`, the form will fall back to opening the user's default email client with a pre-filled message.

## Web3Forms Benefits
- ✨ Free for up to 250 submissions/month
- 🔒 Privacy-focused (GDPR compliant)
- 🚀 No backend required
- 📧 Email notifications with all form data
- 🛡️ Spam protection included
- 📊 Optional dashboard for tracking submissions

## Alternative: mailto Fallback
If Web3Forms is not configured, the form automatically falls back to using `mailto:` links. This opens the user's default email client with a pre-filled message, which provides a seamless experience even without the Web3Forms setup.
