<?php

/**
 * 
 * Class responsable for converting a JSON-decoded object into some
 * markup that can later be included in an html page.
 * 
 * There is blasphemy here in the sense that separation between data and 
 * presentation is absent - this will do for now, we can think about adding
 * some templating logic later, or override it alltogether.
 * 
 * @author vredchenko
 */

class HTMLBuilder
{
	
	public function __construct()
	{}
	
	public function buildShopListHTML($data)
	{
		$markup = '<section id="shoplist">';
		foreach ($data as $k => $shop)
		{
			$markup .= '<article>';
				$markup .= '<h1>' . $shop->qualified_name . '</h1>';
				$markup .= '<div class="address">' . 
					nl2br( $shop->address ) . 
					'</div>';
			$markup .= '</article>';
		}
		$markup .= '</section>';
		
		return $markup;
	}
	
	public function buildShopInfoHTML($data)
	{
		$markup = '<article id="shop-info">';
			$markup .= '<h1>' . $data->qualified_name . '</h1>';
			$markup .= '<div class="address">' . 
					nl2br( $data->address ) . 
					'</div>';
		$markup .= '</article>';
		
		// @todo : add Google Maps plot
		// @todo : add ProductList when API implemented
		
		return $markup;
	}
	
	public function buildProductInfoHTML($data)
	{
		$markup = '<article id="product-info">';
			$markup .= '<h1>' . $data->name . '</h1>';
			if ( strlen($data->description) > 0 ) {
				$markup .= '<p class="description">' . $data->description . '</p>';
			}
			if ( strlen($data->url) > 0 ) {
				$markup .= '<a href="' . $data->url . '">' . $data->url . '</a>';
			}
		return $markup;
	}
	
	
}
