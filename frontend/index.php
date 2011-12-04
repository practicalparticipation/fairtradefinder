<?php

/**
 * Main Controller
 * 
 * @author vredchenko
 * 
 */

require_once('configuration.php');
require_once('retriever.class.php');
require_once('htmlbuilder.class.php');

/**
 * URL conventions:
 * 
 * action = [ shoplist | shopinfo | productinfo ]
 * id = int
 * long = .float
 * lat = .float
 * radius = int, meters
 * 
 */

$QUERY = Array(
	'action' => 'home', // a sensible default
	'id' => 0,
	'long' => 0.00,
	'lat' => 0.00, 
	'radius' => 0 // default 20 meters
);

/**
 * @todo safeguard against injections and verify all mandatory params are present and valid
 */

if ( isset($_GET['action']) && strlen($_GET['action']) > 0 ) $QUERY['action'] = $_GET['action'];
if ( isset($_GET['id']) && $_GET['id'] > 0 ) $QUERY['id'] = (int)$_GET['id'];
if ( isset($_GET['long']) && strlen($_GET['long']) > 0 ) $QUERY['long'] = (float)$_GET['long'];
if ( isset($_GET['lat']) && strlen($_GET['lat']) > 0 ) $QUERY['lat'] = (float)$_GET['action'];

$retr = new Retriever();
$conf = new Configuration();
$out = new HTMLBuilder();

require_once("templates/header-mobile.php");

switch ($QUERY['action'])
{
	
	case 'home': 
	?>
	<div data-role="content">	
		<p>Welcome to Oxford Fair Trade Finder - helping you locate FAIRTRADE Mark and Fairly Traded products in Oxford City.</p>
	</div>

	<form action="index.php?action=keywordsearch" method="GET" data-ajax="false">
		<div data-role="fieldcontain">
	    <label for="KeywordSearch" class="ui-hidden-accessible">Search: </label>
	    <input type="search" name="KeywordSearch" id="KeywordSearch" value="" />
	    <input type="submit" value="Search" />
		</div>
	</form>
	
	<ul data-role="listview" data-inset="true" data-filter="false">
		<li><a href="index.php?action=shoplist">Browse Retailers</a></li>
		<li><a href="index.php?action=productlist">Browse Products</a></li>
	</ul>		
	
	
	
<?php	break;
	
	case 'shoplist':
		
		// @todo filtering to be added later - waiting on the API
		$data = $retr->getShopList($QUERY['long'], $QUERY['lat'], $QUERY['radius']);
		//echo '<pre>'.print_r($data, true).'</pre>';
		$htmlShopList = $out->buildShopListHTML($data);
		echo $htmlShopList;
		
		break;
	
	case 'shopinfo':
		
		$data = $retr->getShopInfo($QUERY['id']);
		//echo '<pre>'.print_r($data, true).'</pre>';
		$htmlShopInfo = $out->buildShopInfoHTML($data);
		echo $htmlShopInfo;
		
		break;
	
	/* products are included in shop information
	case 'productlist':
		
		$data = $retr->getProductList($QUERY['id']); // $QUERY['id'] is shop id
		//echo '<pre>'.print_r($data, true).'</pre>';
		$htmlProductList = $out->buildShopInfoHTML($data);
		echo $htmlProductList;
		
		break;
	*/
	
	case 'productinfo':
		
		$data = $retr->getProductInfo($QUERY['id']);
		//echo '<pre>'.print_r($data, true).'</pre>';
		$htmlProductInfo = $out->buildProductInfoHTML($data);
		echo $htmlProductInfo;
		
		break;
	
}

require_once("templates/footer-mobile.php");

// proving grounds
