LinkShim
========

Replicates Facebook Functionality of their LinkShim

When you click on a link on Facebook to an external url, they take you to a script on Facebook that redirects you to link you requested. This is an important security feature, for the following reasons:

Protects People
Creates opportunity to stop malicious and spammy sites in real-time.

Protect Privacy
Websites know where you came from by the referrer attribute in the header. On most pages, this might not be an issue. But if I clicked on a link that was on my profile, the website could glean the fact that my facebook user
name is "tommycrush" because my referrer would be "http://www.facebook.com/tommycrush". But when we use a redirect script, the referrer is simply "http://www.facebook.com/l.php"

Gather Analytics
As a website, you should know what's be linked to, shared by who, clicked by who, trends, etc. A redirect script creates that opportunity.

https://www.facebook.com/note.php?note_id=10150492832835766