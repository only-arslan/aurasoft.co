<?php
/**
 * Plugin Name: Dev error reporting
 * Description: Keeps E_DEPRECATED out of the debug log while WP_DEBUG is on.
 *
 * The7 9.13 predates PHP 8 and its bundled LESS compiler emits well over
 * 200,000 deprecation notices every time the dynamic stylesheet is rebuilt —
 * around 50 MB of debug.log per rebuild, which happens on any theme-option
 * change. That noise buries real errors and fills the disk.
 *
 * WordPress forces error_reporting( E_ALL ) in wp_debug_mode() during
 * wp-settings.php, so this cannot be set from wp-config.php; a must-use
 * plugin loads afterwards and gets the last word.
 *
 * Warnings, notices and fatals are all still reported — only the deprecation
 * classes are dropped. This is a no-op when WP_DEBUG is off, so it is inert
 * in production.
 *
 * @package Aurasoft
 */

defined( 'ABSPATH' ) || exit;

if ( defined( 'WP_DEBUG' ) && WP_DEBUG ) {
	error_reporting( error_reporting() & ~E_DEPRECATED & ~E_USER_DEPRECATED );
}
