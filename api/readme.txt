REST-ful API dev notes

The API is to consist of two parts:
 - Info Acquisistion
   This part is read-only, it's responsible for providing structured data to the
   client app.
   
 - Info input
   The development of this section is postponed to a later date. Our initial idea
   was to have two levels of access:
   	- "overseer" access - this is efectively a trusted admin with superuser privileges
   	- store owner access - untrusted user that only has privileges to update information regarding their own store
   
   Both of these can be implemented as Web-based content management, so don't require an API
   
   At an even later date, we should add the ability for customer-type users to POST updates to the system.
   
Data to be verified and unverified (level of trustworthyness).

Info acquisition URL scheme:

/localisation/long/lat/radius
Returns a list of shops in the radius of a specified location

/localisation/baseshopinfo/id
Returns basic shop information based on shop id

/localisation/shopproductlist/id
Returns a product list for a given shop based on shop id. Think about limits and pagination

/localisation/productinfo/id
Returns basic shop information based on product id

/localisation/listproductretailers/id
Returns a list of stores retailing a particular product based on product id.

/localisation/listproductretailers/id/long/lat/radius
Same as above but narrowed down to user location.
