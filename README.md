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

## Theme

**The7** (`dt-the7`) **9.13.0.1** — commercial theme by Dream-Theme, purchased
via ThemeForest. Installed and active; it is committed to this repository.

To reinstall from a zip:

```bash
wp theme install /path/to/the7.zip --activate
```

### Version caveat

This build of The7 is from June 2021 and declares `Tested up to: 5.7.2` and
`Requires PHP: 5.6.20`. It is running on WordPress 7.0.2 and PHP 8.4, well
outside its supported range.

It does work — front end, wp-admin, the theme dashboard, the customizer and
the REST API were all verified with no fatal errors — but it carries a lot of
PHP 8.4 deprecation debt. A ThemeForest purchase includes lifetime updates, so
**downloading the current release from your ThemeForest account is strongly
recommended** over building on this 2021 build.

The bundled LESS compiler emits ~238,000 deprecation notices per stylesheet
rebuild. `wp-content/mu-plugins/000-dev-error-reporting.php` filters
`E_DEPRECATED` out of the log so real errors stay visible; without it a single
theme-option change writes ~50 MB to `debug.log`.

### Companion plugins

The7 leans heavily on plugins that are **not** bundled with the theme:

| Plugin | Source | Available here? |
|---|---|---|
| Elementor | wordpress.org | ❌ blocked |
| WooCommerce | wordpress.org | ❌ blocked |
| Contact Form 7 | wordpress.org | ❌ blocked |
| The7 Elements (`dt-the7-core`) | repo.the7.io | ❌ blocked |
| Slider Revolution | repo.the7.io | ❌ blocked |
| WPBakery (`js_composer`) | repo.the7.io | ❌ blocked |

The theme renders correctly without them, but page building, sliders, demo
content and The7's custom post types all depend on them. Install them from
local zips, or do that part of the work on the real host.

### Licensing

Theme registration calls `repo.the7.io`, which is blocked here, so the purchase
code cannot be activated in this sandbox — that also disables theme updates and
demo-content import. Registration works normally on the production host.

The auto-deactivation notice only fires on an explicit remote de-registration
response, so an unreachable licence server does not disable the theme.

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
