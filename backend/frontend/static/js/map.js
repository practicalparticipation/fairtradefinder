 	var lat = 52.406822;
 	var lng = -1.519692;
 	var map;
 	var markers = [];
 	var infoWindow;
 	var geocoder;
 	var delay;
 	
 		$(document).ready(function() {
			var myOptions = {
	          center:new google.maps.LatLng(lat,lng),
	          zoom: 14,
	          mapTypeId: google.maps.MapTypeId.ROADMAP
	        };
	        map = new google.maps.Map(document.getElementById("locations_gmap"), myOptions);
	        infoWindow = new google.maps.InfoWindow();
	        geocoder = new google.maps.Geocoder();
	        setLocation(lat,lng);
	        
	        google.maps.event.addListener(map,'bounds_changed', function() {
	        	clearTimeout(delay); 
  				delay = setTimeout('refreshMap()',200)
	         });
 		});

		function updateMap(locale,parameters){
 			if(locale==null) { locale = "all"; }
 			if(parameters==null) { paramters = ""; }
	 			$.getJSON('/api/'+locale+'/locations/?lat='+lat+'&lng='+lng+'&limit=50&extra=1'+parameters, function(data) {	 		
	 				 $.each(data, function(key, marker) {
	 				 	if(marker.lat && marker.lng) {
	 				 		point = new google.maps.LatLng(marker.lat,marker.lng);

	 				 		markers[marker.id] = new google.maps.Marker({
      							position: point,
      							map: map,
      							title: marker.qualified_name
  							});

  							google.maps.event.addListener(markers[marker.id], 'click', function() {
  								infoWindow.setContent("<strong>"+marker.business_entity.name+"</strong><br/>"+marker.address +", "+marker.postcode+"<br/><a href='/view/location/"+marker.id + "'>View details & products</a>");
  								infoWindow.open(map,markers[marker.id]);
							});

  							markers[marker.id].setMap(map);
	 				 	}
	 				 });
	  			});
 			} 	
 			
 		function setLocation(newLat,newLng) {
 			lat = newLat;
 			lng = newLng;
 			point = new google.maps.LatLng(lat,lng);
 			map.setCenter(point);
 			updateMap();

 			$('#BrowseRetailers').attr('href','/view/locations/?lat='+lat+'&lng='+lng);
 			$('#BrowseRetailers').text("Browse Retailers Nearby");
 			
 			var latlng = new google.maps.LatLng(lat, lng);
		    geocoder.geocode({'latLng': latlng}, function(results, status) {
		      if(status == google.maps.GeocoderStatus.OK) {
		        if(results[1]) {
		          $('#current_location').text(results[1].formatted_address);
		        }
		      }
		    });

		        
 		}

 		function locateUser(address) {
 			if(address==null) {
 				if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(success, error);
                } else {
                    error('Geolocation not supported');
                }
 			} else {
 				$('#current_location').text("Searching for location...");
 				geocoder.geocode( { 'address': address}, function(results, status) {

      				if (status == google.maps.GeocoderStatus.OK) {
      						newLat = results[0].geometry.location.lat();
      						newLng = results[0].geometry.location.lng();
      						setLocation(newLat,newLng);
      				} else {
        				$('#current_location').text("Location search failed. Try including ',UK' on the end for local searches.");
      				}
    			});
 					
 			}
 		}

 		function refreshMap() {
 			newLat = map.getCenter().lat();
            newLng = map.getCenter().lng();
            setLocation(newLat,newLng);
 		}

        $(document).ready(function() {
            $('#locateUser').click(function() {
                locateUser();
            });
            $('#updateMap').click(function() {
                
            });
            $('#locationSearch').toggle(function() {
            	$('#LocationSearchContainer').trigger('expand');
            },
	        function() {
	        	$('#LocationSearchContainer').trigger('collapse');	
	        });

	        $('#LocationSearchForm').submit(function(){
	        	event.preventDefault();
	        	locateUser($('#LocationSearchValue').val());
	        	$('#LocationSearchContainer').trigger('collapse');	
	        	return false;
	        });
	       

        });  

		function success(position) {
		  newLat = position.coords.latitude;
		  newLng =  position.coords.longitude;
		  setLocation(newLat,newLng);
        }
        

        function error(msg) {
          var errMsg = typeof msg == 'string' ? msg : "Geolocation failed";
          $('#msg').html(errMsg);
        }