# 🚀 Deployment Guide - MicDrop

This guide will help you deploy MicDrop to the cloud so it's accessible online, not just locally.

## 📋 Deployment Options

### Option 1: Streamlit Cloud (Recommended - FREE & Easiest) ⭐
- **Free tier**: Unlimited public apps
- **Easy setup**: Connect GitHub repo, auto-deploys
- **Automatic updates**: Redeploys on every push
- **URL**: `https://your-app-name.streamlit.app`

### Option 2: Heroku
- **Free tier**: Limited (may require credit card)
- **More setup**: Requires Procfile, more configuration
- **Good for**: Production apps with custom domains

### Option 3: AWS/Azure/GCP
- **Cost**: Pay-as-you-go
- **Complexity**: High, requires cloud expertise
- **Good for**: Enterprise deployments

---

## 🎯 Recommended: Streamlit Cloud Deployment

### Prerequisites
1. ✅ GitHub account (free)
2. ✅ Your code pushed to a GitHub repository
3. ✅ Streamlit Cloud account (free at https://share.streamlit.io)

### Step-by-Step Instructions

#### Step 1: Prepare Your Repository

1. **Make sure your code is on GitHub:**
   ```bash
   # If not already on GitHub, create a new repo and push:
   git remote add origin https://github.com/YOUR_USERNAME/MicDropP.git
   git add .
   git commit -m "Prepare for deployment"
   git push -u origin main
   ```

2. **Verify these files exist in your repo:**
   - ✅ `app.py` (main entry point)
   - ✅ `requirements.txt` (dependencies)
   - ✅ `page_modules/` directory
   - ✅ `utils/` directory
   - ✅ `assets/` directory (if you have background images)

#### Step 2: Create Streamlit Cloud Account

1. Go to https://share.streamlit.io
2. Click "Sign in with GitHub"
3. Authorize Streamlit Cloud to access your GitHub account

#### Step 3: Deploy Your App

1. **Click "New app"** in Streamlit Cloud dashboard

2. **Fill in the deployment form:**
   - **Repository**: Select `YOUR_USERNAME/MicDropP`
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom name (e.g., `micdrop-ai-coach`)
   - **Python version**: Select `3.11` or `3.12` (recommended, as some packages don't support 3.13)

3. **Click "Deploy"**

4. **Wait for deployment** (5-10 minutes first time):
   - Streamlit Cloud will:
     - Install all dependencies from `requirements.txt`
     - Download Whisper model (~150MB) on first use
     - Build and launch your app

#### Step 4: Access Your App

Once deployed, you'll get a URL like:
```
https://micdrop-ai-coach.streamlit.app
```

Share this URL with anyone! 🎉

---

## ⚙️ Configuration Files

### `.streamlit/config.toml` (Optional)
This file can customize Streamlit settings. It's already created for you.

### `requirements.txt`
Make sure this includes all dependencies. It's already set up correctly.

---

## 🔧 Troubleshooting

### Issue: "Module not found" errors
**Solution**: Check that all dependencies are in `requirements.txt`

### Issue: "Whisper model download fails"
**Solution**: This is normal on first run. The model downloads automatically when first used.

### Issue: "File not found" errors for assets
**Solution**: Make sure `assets/` folder is committed to GitHub

### Issue: "Memory limit exceeded"
**Solution**: 
- Streamlit Cloud free tier has memory limits
- Large audio files may cause issues
- Consider adding file size limits in your app

### Issue: "Deployment takes too long"
**Solution**: 
- First deployment takes 5-10 minutes (installing packages)
- Subsequent deployments are faster (2-3 minutes)
- Check deployment logs for specific errors

---

## 📝 Post-Deployment Checklist

- [ ] App loads successfully
- [ ] Can upload audio files
- [ ] Voice analysis works
- [ ] Visualizations display correctly
- [ ] Background image loads (if you added one)
- [ ] All pages accessible from sidebar

---

## 🔄 Updating Your App

1. **Make changes locally**
2. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Update app"
   git push
   ```
3. **Streamlit Cloud automatically redeploys** (watch the dashboard)

---

## 💡 Tips for Cloud Deployment

1. **File Size Limits**: 
   - Streamlit Cloud has upload limits
   - Consider adding file size validation in your app

2. **Performance**:
   - First Whisper transcription is slow (model download)
   - Subsequent transcriptions are faster (model cached)

3. **Memory**:
   - Large audio files consume memory
   - Consider processing in chunks for very long files

4. **Secrets** (if needed later):
   - Use Streamlit Cloud's "Secrets" feature for API keys
   - Access via `st.secrets["api_key"]`

---

## 🆘 Need Help?

- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Streamlit Forum**: https://discuss.streamlit.io
- **Check deployment logs** in Streamlit Cloud dashboard

---

## 🎉 Success!

Once deployed, your app will be:
- ✅ Accessible 24/7
- ✅ Shareable with anyone via URL
- ✅ Automatically updated on every GitHub push
- ✅ Free (on Streamlit Cloud free tier)

Enjoy your deployed MicDrop app! 🎤

