# EVERYTHING BOT

A fully modular, highly customizable Discord bot designed to adapt to any server environment.  
EVERYTHING BOT lets server owners enable or disable features on demand, keeping the bot lightweight, flexible, and tailored to each community.

---

## 📛 Badges

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-None-green)
![Modular](https://img.shields.io/badge/Architecture-Modular-orange)

---

## 🌟 Overview

EVERYTHING BOT is built around a powerful modular architecture that gives servers complete control over which features they want.  
Modules can be toggled per‑guild, reloaded instantly, and expanded without touching core code — making the bot ideal for communities of any size.

Whether you need moderation tools, fun commands, utilities, or custom server features, EVERYTHING BOT adapts to your needs.

---

## 🔧 Key Features

### 🧩 **Modular System**
- Enable or disable modules per server  
- Add new modules without modifying core logic  
- Reload modules instantly  
- Keep the bot lightweight by loading only what you need  

### ⚙️ **Dynamic Configuration**
- Live guild registration  
- Per‑guild settings stored and updated instantly  
- No restarts required for changes  

### 🏗️ **Clean, Scalable Architecture**
- Organized cog structure  
- Easy to maintain and expand  
- Built for long‑term development  

### 🛠️ **Developer‑Friendly**
- Clear folder structure  
- Simple module creation  
- Custom command grouping API  
- Full control over per‑guild command syncing  

---

# 🧩 Custom Command Group API  
*A lightweight, Discord.py‑compatible system for building slash command groups that sync per‑guild.*

Discord.py’s built‑in `app_commands.Group` and `GroupCog` automatically register commands globally, which conflicts with EVERYTHING BOT’s per‑guild modular sync engine.  
To solve this, the bot includes a **custom group API** that gives developers full control over how groups and subcommands are defined and synced.

This system allows you to create commands like:

`/module list /module enable /module disable`

without Discord.py auto‑registering anything globally.

---

# 📜 LICENSE
This project is licensed under the Proprietary License. See the `LICENSE.txt` file for details.

`LICENSE.txt` also includes detailes about who to contact for contributing to the project, which is currently closed to external contributions.
