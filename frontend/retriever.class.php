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
	private $conf;
	
	public function __construct()
	{
		$this->conf = new Configuration();
	}
	
	/**
	 * Gets info from specified URL, returns decoded JSON
	 */
	private function request($url)
	{
		// @todo enchanced error reporting and graceful error handling
		$result = Array('Unspecified error');
		
		if ( $response = file_get_contents($url) )
		{
			$result = json_decode($response);
		}
		
		return $result;
	}
	
	public function getShopList($Long, $Lat, $Radius)
	{
		$resultset = $this->request($this->conf->api_url . $this->conf->api_locale . '/locations/');
		return $resultset;
	}
	
	public function getShopInfo($ShopID)
	{
		$resultset = $this->request($this->conf->api_url . $this->conf->api_locale . '/location/' . $ShopID . '/');
		return $resultset;
	}
	
	public function getProductInfo($ProductID)
	{
		$resultset = $this->request($this->conf->api_url . $this->conf->api_locale . '/product/' . $ProductID . '/');
		return $resultset;
	}
}