<?php
/**
 * Plugin Name: Set Aurasoft site identity (logo + top-bar phone) in The7
 * Description: Points every logo slot The7 knows about (main header, mobile,
 *              bottom bar, transparent/floating/mixed header styles) at the
 *              uploaded Aurasoft logo instead of the theme's bundled skin
 *              placeholder images, and clears the demo phone number
 *              ("011 322 44 56") from the top bar.
 *
 * The7 stores both of these in a single options row named after the theme
 * ("the7") — the logo fields as [relative_url, attachment_id], the phone as
 * a plain caption string — confirmed by reading options-framework's
 * of_sanitize_upload() sanitizer and presscore_top_bar_contact_element() in
 * the theme source rather than guessed. presscore_top_bar_contact_element()
 * skips rendering entirely when the caption is empty, so clearing it removes
 * the top-bar phone element outright rather than leaving a blank slot.
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

	// Demo placeholder phone number in the top bar ("011 322 44 56"). An
	// empty caption makes presscore_top_bar_contact_element() skip the
	// element entirely rather than rendering an empty link.
	$phone_keys = array(
		'header-elements-contact-phone-caption',
		'header-elements-contact-phone-url',
	);
	foreach ( $phone_keys as $key ) {
		if ( ( $options[ $key ] ?? '' ) !== '' ) {
			$options[ $key ] = '';
			$changed         = true;
		}
	}

	// Footer credit line. bottom-bar.php echoes "Dream-Theme — truly premium
	// WordPress themes" whenever bottom_bar-credits is truthy, found by
	// reading template-parts/footer/bottom-bar.php directly. Turning it off
	// and filling bottom_bar-copyrights replaces it with our own line.
	$footer = array(
		'bottom_bar-credits'    => '',
		'bottom_bar-copyrights' => '&copy; ' . gmdate( 'Y' ) . ' Aurasoft. All rights reserved.',
	);
	foreach ( $footer as $key => $val ) {
		if ( ( $options[ $key ] ?? null ) !== $val ) {
			$options[ $key ] = $val;
			$changed         = true;
		}
	}

	if ( $changed ) {
		update_option( 'the7', $options );
	}
}, 5 );
