# aurasoft.co

WordPress site for **aurasoft.co**.

This repository contains the complete WordPress installation (core + theme),
so the deployable site is whatever is checked in here. `wp-config.php` is
**not** committed — it holds database credentials and auth salts, and is
generated per-environment by the setup script.

- WordPress core: **7.0.2**
- PHP: **8.4**
- Database: **MariaDB 10.11** (MySQL-compatible)

## Quick start

```bash
./scripts/dev-setup.sh      # start MariaDB, create the DB, install WordPress
./scripts/dev-server.sh     # serve on http://127.0.0.1:8080
```

Defaults: site at `http://localhost:8080`, admin `admin` / `admin_dev_pw`.
Override with environment variables (`WP_DB_NAME`, `WP_SITE_URL`,
`WP_ADMIN_PASS`, …) — see the top of `scripts/dev-setup.sh`.

These are **local development credentials only**. Production must use its own
`wp-config.php` with real secrets.

## Installing the theme

The theme is distributed as a zip. Install it from a local file:

```bash
wp theme install /path/to/aurasoft-theme.zip --activate
```

Then commit it, since the theme lives in this repo:

```bash
git add -f wp-content/themes/<theme-slug>
git commit -m "Add aurasoft theme"
```

## Repository layout

```
wp-admin/        WordPress core — do not edit
wp-includes/     WordPress core — do not edit
wp-content/
  themes/        our theme lives here (committed)
  plugins/       plugins (committed)
  uploads/       media — gitignored, not part of the codebase
scripts/         local dev helpers
```

## Environment notes

This project is developed in a sandboxed container with a restricted egress
policy. Two consequences matter day to day:

**wordpress.org is unreachable.** `wp plugin install <slug>` and
`wp theme install <slug>` — anything that pulls from the WordPress.org
repository — will fail, as will update checks in wp-admin. Install from local
zip files or a git checkout instead. WordPress core itself is tracked from the
official mirror at `github.com/WordPress/WordPress`.

**Docker images cannot be pulled.** The registry's blob storage is blocked, so
the official `wordpress` image and any compose-based stack are unavailable.
The environment runs PHP and MariaDB natively, which is what the scripts above
assume.

There is no systemd, so MariaDB is started as a plain background process by
`dev-setup.sh`. The container is ephemeral — commit and push anything worth
keeping.

## Deployment

The sandbox is not the host for aurasoft.co and cannot reach the domain.
Deployment is a separate step: get this repository onto the real host, provide
a production `wp-config.php`, point the document root at the repository root,
and import the database.

Before going live, replace the local admin credentials and generate fresh auth
salts (`wp config shuffle-salts`).
