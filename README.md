# Podcast Filter

Make a podcast feed that only has the episodes you want.

Some podcast channels mix several shows into one feed, so your podcast app downloads everything. Podcast Filter lets you search for a show, choose words that episode titles must or mustn't contain, and get a new feed URL with only the matching episodes. You subscribe to that URL in Apple Podcasts (or any podcast app), and it keeps updating on its own.

It runs entirely on a free GitHub account: GitHub Pages hosts the web page and the feeds, and a GitHub Action rebuilds the feeds every hour. There's no server to run and no coding needed.

## Set up your own copy

About 15 minutes, all in the browser. You need a free [GitHub account](https://github.com/signup).

### 1. Fork this repository

At the top of this page, click **Fork**, then **Create fork**. Keep the name `podcast-filter` if you can. The name becomes part of your web address, and the steps below assume it. Leave the copy **Public**, since free GitHub Pages only works on public repositories.

### 2. Turn on the feed builder

GitHub switches off automated workflows in forked repositories until you allow them.

1. In your fork, open the **Actions** tab.
2. Click **I understand my workflows, go ahead and enable them**.
3. Go to **Settings → Actions → General**, scroll to **Workflow permissions**, choose **Read and write permissions**, and click **Save**. This lets the builder save the feeds it makes.

### 3. Turn on GitHub Pages

1. Go to **Settings → Pages**.
2. Under **Build and deployment**, set Source to **Deploy from a branch**.
3. Set the branch to **main** and the folder to **/docs**. Not **/ (root)**, or your site will show this README instead of the app.
4. Click **Save**.

After a minute or two your app is live at:

`https://YOUR-USERNAME.github.io/podcast-filter/`

### 4. Make an access token

The app saves your feeds into your repository, so it needs a GitHub access token. You make it once and paste it into the app on each device you use.

1. Open [GitHub's new token page](https://github.com/settings/personal-access-tokens/new).
2. Name it something like "Podcast Filter" and choose an expiration date (up to a year).
3. Under **Repository access**, choose **Only select repositories** and pick your `podcast-filter` repository.
4. Under **Permissions → Repository permissions**, set **Contents** to **Read and write**. Leave everything else as it is.
5. Click **Generate token** and copy it. GitHub only shows it once.

### 5. Connect the app

Open your app, click **Settings**, paste the token into **Access token**, and click **Save settings**. Your username and repository fill in automatically when you open the app from your GitHub Pages address. The main page then shows **Connected**.

### 6. Clear out the example feed (optional)

Your fork comes with the original owner's feed for The Herd with Colin Cowherd. Keep it if you want it. Otherwise, open **Your feeds** in the app and click **Delete**.

## Make a filtered feed

1. Search for a show and pick it. Shows marked "Apple-only" are subscriber exclusives with no public feed, so they can't be filtered.
2. Type words under **Keep episodes whose title contains** and/or **Skip episodes whose title contains**, pressing Enter after each. The list on the right shows the latest episodes, with skipped ones struck through, so you can check the result before saving.
3. Click **Save feed**. You get the feed URL with a **Copy URL** button. The page says **Live** once GitHub has built it, usually within two minutes.

**Your feeds** lists everything you've made, with buttons to copy each URL, change its keywords, or delete it.

## Add a feed to Apple Podcasts

**iPhone or iPad:** open Podcasts, tap **Library**, tap **⋯** in the top-right corner, choose **Follow a Show by URL**, paste the feed URL and tap **Follow**. Then open the show, tap **⋯ → Settings**, and turn on automatic downloads.

**Mac:** open Podcasts, choose **File → Follow a Show by URL**, paste the URL and click **Follow**.

Then unfollow the original show so you stop getting the episodes you filtered out.

## If something isn't working

| What you see | What to do |
|---|---|
| Your web address shows this README instead of the app | **Settings → Pages**: set the folder to **/docs**, not **/ (root)**. |
| Your web address shows "404 There isn't a GitHub Pages site here" | Pages isn't on yet, or it's still starting. Do step 3, then wait two minutes. |
| The Actions tab has no runs, or says workflows are disabled | Do step 2: enable workflows in the Actions tab. |
| A run in the Actions tab is red with "Permission denied" or "403" on the push step | **Settings → Actions → General → Workflow permissions**: choose **Read and write permissions**. Then rerun it. |
| Saving says GitHub didn't accept the token | The token was mistyped, expired, or deleted. Make a new one (step 4) and paste it in Settings. |
| Saving says the token can't change this repository | The token is missing **Contents: Read and write**, or wasn't given access to this repository. Make a new one following step 4. |
| Saving says it couldn't find your repository | In Settings, check the username and repository name match your fork exactly. |
| The feed URL shows "404" after saving | GitHub is still building it. Check the Actions tab: wait for the run to turn green, then give Pages another minute. |
| A run has a yellow warning saying none of the episodes matched | The show changed how it names episodes. Edit that feed's keywords in **Your feeds**. The feed keeps its last good version until then. |
| The feed stopped getting new episodes after a couple of months | GitHub pauses scheduled workflows in quiet repositories. Open the Actions tab and click **Enable workflow**. |

## How it works

| File | What it does |
|---|---|
| `docs/index.html` | The web app, served by GitHub Pages. |
| `docs/feeds.json` | Your list of filtered feeds. The app edits this file when you save. |
| `docs/feeds/*.xml` | The filtered feeds your podcast app subscribes to. |
| `filter_feed.py` | Downloads each original feed, keeps the matching episodes, and writes the filtered feeds. |
| `.github/workflows/update-feeds.yml` | Runs `filter_feed.py` every hour, and right away whenever `feeds.json` changes. |

Search and the episode preview use Apple's public podcast directory. The audio itself still comes straight from the podcast's publisher; this only filters the list of episodes.

## Good to know

- **Matching:** an episode is kept if its title contains any keep word (or there are none), then dropped if it contains any skip word. Capital letters don't matter, and partial words count, so "cut" also matches "Prime Cuts".
- **Preview vs. real feed:** the preview shows up to the latest 200 episodes. The real feed is built from the publisher's full feed, so older matching episodes appear too, up to the **Newest** limit you set.
- **Pasted feeds:** you can paste any RSS feed address instead of searching, but there's no preview for those.
- **Timing:** the hourly update runs at about 17 minutes past each hour, sometimes a few minutes late. To change how often, edit the `cron` line in `.github/workflows/update-feeds.yml`.
- **Your token stays in your browser.** It's only sent to GitHub and can only change your `podcast-filter` repository. Don't share it or put it in a file. If a device is lost, delete the token on GitHub's [token settings page](https://github.com/settings/personal-access-tokens) and make a new one.
- **Everything else is public:** your repository, your app page and your feed URLs. They only contain public episode information, so don't use this for private or paid feeds.
- **Getting updates:** when this project is improved, GitHub shows a **Sync fork** button on your fork's main page. Click **Update branch** to pull in the changes. If GitHub says the update conflicts with your changes, don't choose **Discard commits**: that would erase your feed list. Skip that update instead.
