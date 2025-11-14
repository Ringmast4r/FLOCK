# Quick Deployment Guide

## 🚀 Deploy to GitHub Pages in 5 Minutes

### Prerequisites
- GitHub account
- Git installed on your computer

### Step-by-Step Deployment

#### 1. Create GitHub Repository (2 minutes)

1. Go to https://github.com/new
2. Repository name: `discord-flock` (or anything you want)
3. Description: "FLOCK surveillance network map with 178K+ cameras"
4. **Public** repository (required for free GitHub Pages)
5. **Do NOT** check "Add README" (we already have one)
6. Click **Create repository**

#### 2. Initialize and Push (3 minutes)

Open terminal/command prompt in this folder and run:

```bash
# Navigate to this folder
cd C:\Users\Squir\Desktop\discord-flock

# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: FLOCK surveillance map"

# Add your GitHub repository as remote (REPLACE WITH YOUR URL)
git remote add origin https://github.com/YOUR_USERNAME/discord-flock.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: Replace `YOUR_USERNAME` with your actual GitHub username!

#### 3. Enable GitHub Pages (1 minute)

1. Go to your repository on GitHub
2. Click **Settings** (top menu)
3. Scroll to **Pages** in left sidebar
4. Under **Source**:
   - Branch: select `main`
   - Folder: select `/ (root)`
5. Click **Save**
6. GitHub will show: "Your site is ready to be published at..."

#### 4. Wait for Deployment (2-5 minutes)

- Click **Actions** tab to see deployment progress
- Green checkmark = deployment successful
- Red X = deployment failed (check errors)

#### 5. Visit Your Live Map! 🎉

Your map will be live at:
```
https://YOUR_USERNAME.github.io/discord-flock/
```

Or if you named it differently:
```
https://YOUR_USERNAME.github.io/REPOSITORY_NAME/
```

---

## 🔄 Updating the Map

To update camera data or make changes:

```bash
# Make your changes to files

# Add changes
git add .

# Commit with message
git commit -m "Update camera data - December 2025"

# Push to GitHub
git push

# GitHub Pages will automatically redeploy (takes 2-5 minutes)
```

---

## ⚙️ Custom Domain (Optional)

Want to use your own domain like `flocksurveillance.com`?

1. Buy domain from registrar (Namecheap, Google Domains, etc.)

2. Create file named `CNAME` in this folder:
   ```
   echo "yourdomain.com" > CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

3. Configure DNS at your registrar:
   ```
   Type: A
   Name: @
   Value: 185.199.108.153

   Type: A
   Name: @
   Value: 185.199.109.153

   Type: A
   Name: @
   Value: 185.199.110.153

   Type: A
   Name: @
   Value: 185.199.111.153
   ```

4. Wait for DNS propagation (up to 24 hours, usually ~1 hour)

5. In GitHub repository Settings > Pages, add your custom domain

---

## 🐛 Troubleshooting

### "Failed to push"
- Make sure you replaced `YOUR_USERNAME` with your actual GitHub username
- Check that you have permission to push to the repository
- Try: `git remote -v` to verify remote URL

### "404 Page Not Found"
- Wait 5 minutes after enabling GitHub Pages
- Check that index.html is in the root directory
- Verify GitHub Pages is enabled in Settings > Pages
- Try force refresh: Ctrl + Shift + R

### "Data not loading"
- Check browser console (F12) for errors
- Verify all .geojson and .json files are pushed to GitHub
- Check file sizes didn't exceed 100MB
- Try clearing browser cache

### Map loads but no markers
- Wait for data to finish loading (check loading indicator)
- Check browser console for JavaScript errors
- Verify geojson files are valid JSON
- Try on different browser

### "This site can't provide a secure connection"
- GitHub Pages automatically provides HTTPS
- Make sure you're using https:// not http://
- If using custom domain, wait for SSL certificate provisioning (can take 24 hours)

---

## 📊 Monitoring Your Site

### GitHub Actions
- Go to **Actions** tab in your repository
- See all deployments and their status
- Click any deployment to see detailed logs

### Analytics (Optional)

Add Google Analytics or Plausible:

1. Sign up for analytics service
2. Get tracking code
3. Add to `index.html` before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

4. Commit and push

---

## ✅ Deployment Checklist

Before going live, verify:

- [ ] All files committed and pushed to GitHub
- [ ] GitHub Pages enabled in repository settings
- [ ] Deployment successful (green checkmark in Actions)
- [ ] Map loads at GitHub Pages URL
- [ ] All 178K+ cameras visible (may take time to load)
- [ ] Network lines draw when clicking cameras
- [ ] Legend toggles work
- [ ] Mobile responsive (test on phone)
- [ ] README.md updated with correct URLs

---

## 🎯 What's Next?

After deployment:

1. **Share your map**:
   - Twitter/X with #Surveillance #Privacy
   - Reddit (r/privacy, r/dataisbeautiful)
   - Privacy advocacy groups
   - Local news outlets

2. **Update regularly**:
   - Re-download data monthly
   - Add new camera sources
   - Update statistics

3. **Customize**:
   - Change colors/styles
   - Add more data layers
   - Improve performance
   - Add new features

---

## 💬 Need Help?

- **GitHub Issues**: Open an issue in your repository
- **DeFlock Community**: https://deflock.me/
- **Reddit**: r/privacy, r/github

---

**Your map is ready to go live! Follow the steps above and you'll be deployed in minutes. 🚀**
