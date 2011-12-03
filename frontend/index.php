<?php

/**
 * Main Controller
 */

require_once('configuration.php');
require_once('retriever.class.php');

/**
 * URL conventions:
 * 
 * action = [ shopinfo | productinfo | shoplist | productlist ]
 * id = int
 * long = .float
 * lat = .float
 * radius = int, meters
 * 
 */

$QUERY = Array(
	'action' => '',
	'id' => 0,
	'long' => 0.00,
	'lat' => 0.00, 
	'radius' => 0 // default 20 meters
);

/**
 * @todo safeguard against injections
 */

if ( isset($_GET['action']) && strlen($_GET['action']) > 0 ) $QUERY['action'] = $_GET['action'];
if ( isset($_GET['id']) && $_GET['id'] > 0 ) $QUERY['id'] = (int)$_GET['id'];
if ( isset($_GET['long']) && strlen($_GET['long']) > 0 ) $QUERY['long'] = (float)$_GET['long'];
if ( isset($_GET['lat']) && strlen($_GET['lat']) > 0 ) $QUERY['lat'] = (float)$_GET['action'];

$retr = new Retriever();
$conf = new Configuration();

switch ($QUERY['action'])
{
	
	case 'shoplist':
		
		break;
	
	case 'shopinfo':
		
		break;
	
	case 'productlist':
		
		break;
	
	case 'productinfo':
		
		break;
		
}