<?php

/**
 * The prupose of this class is to query the API for data
 * and return the resulting JSON
 *
 * @author vredchenko
 * 
 */

class Retriever
{
	
	public function __construct()
	{
		
	}
	
	/**
	 * Gets info from specified URL, returns decoded JSON
	 */
	private function request($url)
	{
		$result = Array('Unspecified error');
		
		if ( $response = file_get_contents($url) )
		{
			$result = json_decode($response);
		}
		
		return $result;
	}
	
	public function getShopList($Long, $Lat, $Radius)
	{}
	
	public function getShopInfo($ShopID)
	{}
	
	public function getProductList($ShopID)
	{}
	
	public function getProductInfo($ProductID)
	{}
	
}