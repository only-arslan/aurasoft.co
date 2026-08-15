<?php
/**
 * Plugin Name: Google Tag Manager
 * Description: Installs GTM-5K5GGSML in <head> and immediately after the
 *              opening <body> tag, per Google's own installation
 *              instructions — via wp_head/wp_body_open rather than editing
 *              theme files, so it survives theme updates.
 *
 * The7's header.php delegates to header-single.php, which calls both hooks
 * in the correct order on every page (confirmed by reading the theme source,
 * not assumed) — wp_head() inside <head>, then <body>, then
 * wp_body_open() immediately after.
 */

defined( 'ABSPATH' ) || exit;

define( 'AURASOFT_GTM_ID', 'GTM-5K5GGSML' );

add_action( 'wp_head', function () {
	?>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','<?php echo esc_js( AURASOFT_GTM_ID ); ?>');</script>
<!-- End Google Tag Manager -->
	<?php
}, 1 );

add_action( 'wp_body_open', function () {
	?>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=<?php echo esc_attr( AURASOFT_GTM_ID ); ?>"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
	<?php
}, 1 );
