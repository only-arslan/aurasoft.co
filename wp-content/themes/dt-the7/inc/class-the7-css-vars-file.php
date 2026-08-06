<?php
/**
 * Class The7_CSS_Vars_File.
 *
 * @package The7
 */

defined( 'ABSPATH' ) || exit;

/**
 * Class The7_CSS_Vars_File
 */
class The7_CSS_Vars_File {

	/**
	 * CSS file path.
	 *
	 * @var string
	 */
	protected $file;

	/**
	 * The7_CSS_Vars_File constructor.
	 *
	 * @param string $file CSS file path.
	 */
	public function __construct( $file ) {
		$this->file = $file;
	}

	/**
	 * Create a file with css vars based on provided less vars.
	 *
	 * @param array              $less_vars Less vars list.
	 * @param The7_Less_Compiler $compiler  Less compiler.
	 */
	public function generate_based_on_less_vars( $less_vars, The7_Less_Compiler $compiler ) {
		$css_vars = [];
		foreach ( $less_vars as $less_var => $_ ) {
			$css_var_name = str_replace( [ '_', '-dt-' ], [ '-', '-' ], "--the7-{$less_var}" );
			$css_vars[]   = "{$css_var_name}: " . '@' . $less_var . ';';
		}

		$this->add_predefined_vars( $css_vars );

		sort( $css_vars );

		$css_vars = ':root {' . PHP_EOL . implode( PHP_EOL, $css_vars ) . '}' . PHP_EOL;

		$compiler->put_contents( $this->file, $compiler->compile( $css_vars ) );
	}

	/**
	 * Add predefined css vars for backward compatibility at most.
	 *
	 * @param array $css_vars CSS vars.
	 */
	protected function add_predefined_vars( &$css_vars ) {
		$css_vars = array_merge(
			$css_vars,
			[
				'--the7-base-border-radius: @border-radius-size;',
				'--the7-filter-pointer-border-width: @filter-decoration-line-size;',
				'--the7-filter-pointer-bg-radius: @filter-border-radius;',
				'--the7-general-border-radius: @border-radius-size;',
				'--the7-text-big-font-size: @text-big;',
				'--the7-big-button-border-radius: @dt-btn-l-border-radius;',
				'--the7-medium-button-border-radius: @dt-btn-m-border-radius;',
				'--the7-small-button-border-radius: @dt-btn-s-border-radius;',
			]
		);
	}
}
