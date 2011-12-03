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

Info acquisition:

/BASE/LOCALISATION/LONG/LAT/RADIUS
/BASE/LOCALISATION/SHOPNAME/BASEINFO
/BASE/LOCALISATION/SHOPNAME/PRODUCTLIST
/BASE/LOCALISATION/PRODUCTNAME/INFO
/BASE/LOCALISATION/PRODUCTNAME/SHOPLIST


