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
		$markup = '<ul data-role="listview">';
		foreach ($data as $k => $shop)
		{
			$markup .= '<li>';
				$markup .= '<a href="index.php?action=shopinfo&id='.$shop->id . '"><h3>' . $shop->qualified_name . '</h3>';
				$markup .= '<p>' . 
					nl2br( $shop->address ) . 
					'</p></a></li>';
		}
		$markup .= '</ul>';
		
		return $markup;
	}
	
	public function buildShopInfoHTML($data)
	{
		$markup = '<article id="shop-info">';
		$markup .= '<img src="http://maps.googleapis.com/maps/api/staticmap?center='.$data->lat.','.$data->lng.'&zoom=14&size=200x200&sensor=false&markers=color:blue%7C'.$data->lat.','.$data->lng.'" align="right"/>';
			$markup .= '<h1>' . $data->qualified_name . '</h1>';
			$markup .= '<div class="address">' . 
					nl2br($data->address).", ". $data->postcode .  
					'</div>';
		$markup .= '</article>';
		
		$markup .= '<br clear="all"><h3>Products available here</h3>';
		$markup .= '<div data-role="collapsible-set">';
			$products = $this->sortProductsBySection($data->products);
			foreach($products as $section) {
				$markup .= '<div data-role="collapsible" data-theme="c" data-content-theme="d" data-collapsed="true">';
				$markup .= '<h3>'.$section['name'].'</h3><ul>';
				foreach($section['product'] as $product) {
					$markup .= '<li><a href="index.php?action=productinfo&id='.$product->id .'">'.$product->name."</a></li>";
				}
				$markup .= "</ul></div>";
				
			}
		$markup .= '</div>';		
		
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
	
	public function sortProductsBySection($products) {
		foreach($products as $product) {
			$sections[$product->category->id]['name'] = $product->category->name;
			$sections[$product->category->id]['product'][] = $product;
		}
		return $sections;
	}
	
}
