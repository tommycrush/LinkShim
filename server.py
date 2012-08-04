import tornado.ioloop
import tornado.web
import tornado.template
from urlparse import urlparse
import redis
import datetime
import string
import random
import time



#Admin Handler
class HashHandler(tornado.web.RedirectHandler):
    def initialize(self, cache, admin_token):
        self.cache = cache
        self.admin_token = admin_token
        self.life_of_hash = 60*60*6
    
    def get(self):
        #simple admin check. Best to move this endpoint to an internal IP for security on production
        if self.get_argument("admin_token") != self.admin_token:
            self.write({"error":1,"errorMsg":"Are you the admin?"})
            return 1

        #get the number of hashes they want. Default to 10.
        num = int(self.get_argument("num",10))
        if num > 1000000000000:
            self.write({"error":1,"errorMsg":"No more than 100 at a time, please."})
            return 1

        
        expiration = int(time.mktime(time.gmtime())) + self.life_of_hash
        tokens = []
        for i in range(num):
            #create token and add it to the database
            token = self.generateRandomToken()
            self.cache.zadd("linkshim:hashes", expiration, token)
            tokens.append(token)

        self.write({"error":0,"tokens": tokens,"expiration":expiration})
        return 1

    
    def generateRandomToken(self, size=25, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
        return "".join(random.choice(chars) for x in range(size))




#Handle requests to redirect
class RedirectHandler(tornado.web.RequestHandler):
    def initialize(self, cache, templates_dir):
        self.cache = cache
        self.loader = tornado.template.Loader(templates_dir)
    
    def get(self):
        href = self.get_argument("href")
        
        current_timestamp = int(time.mktime(time.gmtime()))
        
        #add the url to today's set
        today = datetime.date.today().strftime("%Y-%m-%d")
        self.cache.zincrby("linkshim:outbound:" + today , href, 1)
    
        #check domain for watch_list
        domain = self.getDomain(href)
        ismember = self.cache.sismember("linkshim:watchlist",domain)
        
        #if it is in the watchlist, lets totally block that domain by displaying watchlist.html
        if ismember:
            self.writeConfirmationMessage("watchlist.html",href)
            return 1

        #get expiration of the hash provided
        h = str(self.get_argument("h"))
        expiration = self.cache.zscore("linkshim:hashes", h)
        
        #if hash doesn't exist, or its expired, display the warning message
        if expiration == None or expiration < time.mktime(time.gmtime()):
            self.writeConfirmationMessage("warning.html", href)
            return 1  

        #we're all good! [domain not marked as spam, and hash is valid]
        self.smartRedirect(href)
        return 1

    #write a simple HTML page to stop user from being linked, or to warning them (you edit the HTML in watchlist.html or warning.html)
    def writeConfirmationMessage(self, file, href):
        html = self.loader.load(file).generate(href=href)
        self.write(html)
        return 1    


    #using this rather than a simple header redirect makes the referrer from this page, to protect privacy of the user
    def smartRedirect(self, href):
        #we set a refresh header just to be safe, but hopefully we won't use it.
        self.set_header("Refresh","1")
        self.set_header("URL", href)

        #IE requires a special solution.
        if self.isIE():
            self.write("<a hef='" + href + "' id='a'></a><script>document.getElementById('a').click();</script>")
        else:
            self.write("<script>document.location.replace('" + href + "');</script>")

        return 1


    #IE sucks. Let's use a helper function to detect it
    def isIE(self):
        if "User-Agent" not in self.request.headers:
            return False
        
        user_agent = self.request.headers["User-Agent"]
        if user_agent.find("MSIE") != -1:
            return True

        return False

    #get raw domain name, stripped of subdomains and ports
    def getDomain(self, href):
        url_parts = urlparse(href)
        domain = '.'.join(url_parts.netloc.split('.')[-2:])
        index =  domain.find(":")
        if index != -1:
            domain = domain[:index]

        return domain





if __name__ == "__main__":
    #connect to redis!
    redis_cache = redis.StrictRedis(host='localhost', port=6379, db=0)

    #change to random string. Strong authentication with IP checks, etc. should be required on production scripts.
    admin_token = "JTCyFFO7OMWRxlnLCp6gp4fcJaLj2234tv3U0AabE7iQ"
    listen_on_port = 8888

    #absolute path that our templates are located in
    templates_dir = "/Users/tommy/Dropbox/Web/GitHubRepos/LinkShim/templates"
    
    application = tornado.web.Application([
        (r"/r", RedirectHandler, dict(cache=redis_cache, templates_dir=templates_dir)),
        (r"/hash", HashHandler, dict(cache=redis_cache,admin_token=admin_token)),                                  
    ])
    application.listen(listen_on_port)
    tornado.ioloop.IOLoop.instance().start()
