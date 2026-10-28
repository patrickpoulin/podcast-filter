# Podcast Filter: filtered podcast feeds on GitHub Pages

A small web app plus a GitHub Action. In the app you search for a podcast, choose words that episode titles must or mustn't contain, and get a feed URL to subscribe to in Apple Podcasts (or any app). GitHub rebuilds every filtered feed every hour.

It comes with one feed already set up: **The Herd with Colin Cowherd, Prime Cuts only**.

## How the pieces fit

| File | What it does |
|---|---|
| `docs/index.html` | The web app. GitHub Pages serves it at `https://YOUR-USERNAME.github.io/podcast-filter/`. |
| `docs/feeds.json` | Your list of filtered feeds. The app edits this file for you. |
| `filter_feed.py` | Downloads each original feed, keeps the matching episodes, writes `docs/feeds/<name>.xml`. |
| `.github/workflows/update-feeds.yml` | Runs the script every hour, and right away whenever you save a feed in the app. |

Searching and the episode preview use Apple's public podcast search, which needs no account. Saving needs a GitHub access token, because the app writes `feeds.json` into your repo.

## One-time setup (about 10 minutes, all in the browser)

1. **Create a repository.** On github.com click **+ → New repository**. Name it, for example, `podcast-filter`. Make it **Public** (free GitHub Pages requires that). Click **Create repository**.
2. **Upload the files.** On the new repo page click **uploading an existing file** and drag in everything inside the `podcast-filter` folder, including the hidden `.github` folder. Click **Commit changes**.
   - If your computer hides `.github`, use **Add file → Create new file**, type `.github/workflows/update-feeds.yml` as the name, and paste in that file's contents.
3. **Let the workflow save feeds.** **Settings → Actions → General → Workflow permissions** → choose **Read and write permissions** → **Save**.
4. **Build the first feed.** **Actions** tab → **Update filtered feeds** → **Run workflow**. When it turns green, `docs/feeds/the-herd-prime-cuts.xml` appears in the repo.
5. **Turn on Pages.** **Settings → Pages** → Source **Deploy from a branch**, branch **main**, folder **/docs** → **Save**. After a minute or two the app is live at `https://YOUR-USERNAME.github.io/podcast-filter/`.
6. **Make an access token for the app.** Open [GitHub's new token page](https://github.com/settings/personal-access-tokens/new):
   - Name it "Podcast Filter" and pick an expiration (up to a year).
   - **Repository access → Only select repositories →** pick this repo.
   - **Permissions → Repository permissions → Contents → Read and write.**
   - **Generate token**, copy it.
7. **Connect the app.** Open the app, click **Settings**, paste the token, and save. Username and repo fill in automatically when you open the app from GitHub Pages.

## Using it

1. Search for a show and pick it. Shows marked "Apple-only" are subscriber exclusives without a public feed, so they can't be filtered.
2. Add words under **Keep episodes whose title contains** and/or **Skip episodes whose title contains**. Press Enter after each. The list on the right shows the latest episodes, with skipped ones struck through, so you can check the result before saving.
3. Click **Save feed**. You get the feed URL with a **Copy URL** button and a link that opens it in Apple Podcasts on your iPhone. The page says "Live" once GitHub has built it, usually within two minutes.
4. In Apple Podcasts, turn on automatic downloads for the new feed and unfollow the original show.

**Your feeds** lists everything you've made, with buttons to copy each URL, change its keywords, or delete it.

## The Herd feed

Its URL is `https://YOUR-USERNAME.github.io/podcast-filter/feeds/the-herd-prime-cuts.xml`. If you already set up the earlier one-feed version, delete that repo's `.github/workflows/update-feed.yml` (or the whole repo) and subscribe to this URL instead, since the old feed stops updating.

## Good to know

- **Matching rule:** an episode is kept if its title contains any keep word (or there are none), and then dropped if it contains any skip word. Capital letters don't matter, and partial words match, so "cut" also matches "Prime Cuts".
- **Preview vs. feed:** the preview shows up to the latest 200 episodes from Apple. The real feed is built from the publisher's full feed, so older matching episodes also appear, up to your **Newest** limit.
- **Pasted feeds:** you can paste any RSS URL instead of searching, but there's no preview for those.
- **If a feed stops matching** (for example, the publisher renames a segment), that feed keeps its last good version and the run shows a warning in the Actions tab. Other feeds still update.
- **Timing:** GitHub runs the hourly job at about 17 minutes past each hour, sometimes a few minutes late. To change how often, edit the `cron` line in the workflow file.
- **Quiet repos pause:** GitHub turns off scheduled workflows in a public repo after 60 days with no activity. The workflow commits whenever a new matching episode appears, which normally keeps it active. If it ever stops, click **Enable workflow** in the Actions tab.
- **Your token stays in your browser.** With "Remember on this device" checked it's stored in that browser only, and it is only sent to GitHub. It can only change this one repo. If you lose a device, delete the token on GitHub's token settings page.
- **Everything here is public:** the repo, the app page and the feed URLs. They only contain public episode information, so don't use this for private or paid feeds.
