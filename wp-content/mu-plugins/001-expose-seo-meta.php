<?php
/**
 * Plugin Name: Expose SEO Framework fields to REST
 * Description: Registers The SEO Framework's per-page title/description fields
 *              for REST so they can be set the same way page content is.
 *
 * The SEO Framework does not register its own meta keys with show_in_rest, so
 * the block editor's REST API silently drops writes to them — a request can
 * succeed with 200 and change nothing. This exposes exactly the two fields
 * needed to fix that, scoped to pages only.
 *
 * @package Aurasoft
 */

defined( 'ABSPATH' ) || exit;

add_action( 'init', function () {
	foreach ( array( '_genesis_title', '_genesis_description' ) as $key ) {
		register_post_meta( 'page', $key, array(
			'show_in_rest'      => true,
			'single'            => true,
			'type'              => 'string',
			'auth_callback'     => function () {
				return current_user_can( 'edit_posts' );
			},
		) );
	}
} );
