# Creating a Reddit App for API Access

To use the Reddit Stock Sentiment Analyzer, you’ll need to create a Reddit Application to obtain your API credentials (client ID and client secret). Follow the steps below:

---

## 1. Go to Reddit App Preferences

- Visit [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) (make sure you’re logged into your Reddit account).

---

## 2. Create a New App

1. Scroll down to the **Developed Applications** section.
2. Click the **"Create App"** or **"Create Another App"** button.

---

## 3. Fill Out the App Form

- **Name**: Choose a name for your app (e.g., `StockAnalyzer`).
- **Description**: Briefly describe your app (e.g., "Analyses Reddit comments for stock sentiment").
- **Application Type**: Select **"script"** (for personal use and scripts).
- **About URL**: (Optional) You can leave this blank.
- **Redirect URI**: Enter `http://localhost:8080` (or the URI your app will use).
- **Permissions**: No action needed for scripts.

Check the "I'm not a robot" box and click **"Create app"**.

---

## 4. Get Your Credentials

After creating the app, you’ll see:
- **Client ID:** (under the app name, a string of letters/numbers)
- **Client Secret:** (labeled "secret")

---

## 5. Add Your Credentials to the Project

Create a `.env` file in your project directory and add:

```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=StockAnalyzer:v1.0
```

Replace `your_client_id` and `your_client_secret` with your actual values.

---

## Example Screenshot
**1) Create an app** 

<img width="1682" height="986" alt="Image" src="https://github.com/user-attachments/assets/d9ce64a8-4e76-4de2-8d71-51bb4c057950" />

**2) Reddit IDs after app creation**

<img width="2171" height="1143" alt="Image" src="https://github.com/user-attachments/assets/e4fb3ece-42cb-40f1-aaaf-1671f99f3f1d" />

---

## Troubleshooting

- Make sure you select **"script"** as the application type.
- The **redirect URI** must match what you enter in your `.env` or script.
- If you have issues, try regenerating your secret or double-checking your credentials.

---

For more details, see the [Reddit API documentation](https://github.com/reddit-archive/reddit/wiki/OAuth2).
