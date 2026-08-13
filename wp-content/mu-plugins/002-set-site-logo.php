<?php
/**
 * Plugin Name: Set Aurasoft logo across every The7 header variant
 * Description: Points every logo slot The7 knows about (main header, mobile,
 *              bottom bar, transparent/floating/mixed header styles) at the
 *              uploaded Aurasoft logo, instead of the theme's bundled skin
 *              placeholder images.
 *
 * The7 stores its logo fields in a single options row named after the theme
 * ("the7"), each as [relative_url, attachment_id] — confirmed by reading the
 * options-framework's own of_sanitize_upload() sanitizer rather than guessed.
 * No admin-facing "logo" setting exists in wp-admin for this theme separate
 * from Theme Options screens the account using this site could not locate, so
 * this writes the same value the UI would have written.
 *
 * Idempotent: only writes to the database when a value actually differs, so
 * it is cheap to leave in place and safe to run on every page load.
 */

defined( 'ABSPATH' ) || exit;

add_action( 'init', function () {
	$attachment_id = 51; // "Aurasoft Logo", uploaded via wp media import.

	$url = wp_get_attachment_url( $attachment_id );
	if ( ! $url ) {
		return;
	}

	$relative = str_replace( site_url(), '', $url );
	$value    = array( $relative, $attachment_id );

	$options = get_option( 'the7' );
	if ( ! is_array( $options ) ) {
		return;
	}

	// Every logo-image slot The7's header/footer templates can read from,
	// across every header style (regular, transparent, floating, mixed,
	// mobile) so the logo is correct no matter which style is active now
	// or gets switched to later.
	$keys = array(
		'header-logo_regular',
		'header-logo_hd',
		'header-style-mobile-logo_regular',
		'header-style-mobile-logo_hd',
		'header-style-transparent-logo_regular',
		'header-style-transparent-logo_hd',
		'header-style-floating-logo_regular',
		'header-style-floating-logo_hd',
		'header-style-mixed-transparent-top_line-logo_regular',
		'header-style-mixed-transparent-top_line-logo_hd',
		'bottom_bar-logo_regular',
		'bottom_bar-logo_hd',
	);

	$changed = false;
	foreach ( $keys as $key ) {
		if ( ( $options[ $key ] ?? null ) !== $value ) {
			$options[ $key ] = $value;
			$changed         = true;
		}
	}

	if ( $changed ) {
		update_option( 'the7', $options );
	}
}, 5 );
