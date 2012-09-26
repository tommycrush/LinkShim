LinkShim
========

Replicates Facebook Functionality of their LinkShim

When you click on a link on Facebook to an external url, they take you to a script on Facebook that redirects you to link you requested. This is an important security feature, for the following reasons:

### Protects People
Creates opportunity to stop malicious and spammy sites in real-time.

### Protect Privacy
Websites know where you came from by the referrer attribute in the header. On most pages, this might not be an issue. But if I clicked on a link that was on my profile, the website could glean the fact that my facebook user
name is "tommycrush" because my referrer would be "http://www.facebook.com/tommycrush". But when we use a redirect script, the referrer is simply "http://www.facebook.com/l.php"

### Gather Analytics
A successful web company should know what's be linked to, shared by who, clicked by who, trends, etc. A redirect script creates that opportunity.


### Learn More About Facebook's (& thus this) LinkShim
Matt Jones, an engineer at Facebook, wrote an excellent explanation of their LinkShim
https://www.facebook.com/note.php?note_id=10150492832835766

How to Setup
========
This project is meant to be a framework you can use to quickly set a LinkShim. Thus, it is not comprehensive (for example, there is no user specific logging, which would be necessary in production). Follow these steps to setup:

### 1. Install Redis & Tornado
LinkShim uses [Redis](http://redis.io), a [NoSQL](http://en.wikipedia.org/wiki/NoSQL) technology, to maintain a spam watchlist, an analtics container, and a set of valid hashes (to prevent becoming an [OpenRedirector](https://www.owasp.org/index.php/Open_redirect))

It also uses the python (Tornado Framework)[http://www.tornadoweb.org/], a scalable, non-blocking web server. I implemented this in python rather than PHP so we can keep settings and database connections open between calls. In redirect engines, speed is of utmost importantance (behind security, of course.)

### 2. Change Settings
Download these files, place them where you want, and open server.py. Change the `admin_token` to something random/secure, and `listen_on_port` to the port you want to listen to, and templates_dir to the absolute path of your templates. (duh.)

### 3. Start er' Up.
`python server.py` will work for testing. In production, you'll want to use a daemon.

### 4. Create some Hashes
Have your frontend guys/gals hit `/hash?admin_token=YOUR_TOKEN&num=10` to create some hashes when they need them. By Default, tokens are valid for 6 hours. This endpoint should really be only avaiable internally for security reasons. It's on the same port for now just for the demo. 

### 5. Include the JS and place the Hashes
Include the JS Script on your page. Place one of the hashes in JS like so:
`<  script type="text/javascript"  >

  	LinkShim.init();
  	
		LinkShim.addPageParams({
		    pageVersion: 'a',//great for A/B testing!
		    hash: 'CREATED_HASH',
		    anyRandomPageVar: '3000'
		});
		
		
	</ script >
`