var LinkShim = {

    //set options
    redirect_url: "http://yoururl.com:8888/r?",
    tracker_attr: "data-track",
    params: {},

    //called on mousedown event
    changeHref: function(a) {
        var $a = $(a);
        var params = this.params;
        var url = this.redirect_url + $a.attr(this.tracker_attr);

        //build params                    
        params.href = $a.attr('href');
        for (var f in params) {
            url += "&" + f + "=" + encodeURIComponent(params[f]);
        }
    
        //change href of click            
        $a.attr('href', url);
    },

    //manually call to add PageParams
    addPageParams: function(new_params) {
        if (typeof new_params == 'object') {
            for (var f in new_params) {
                this.params[f] = new_params[f];
            }
        }
    },

    //call to listen to clicks on objects that contain the tracker_attr par            
    init: function() {
        var obj = this; //added b/c 'this' will end up refering to a tag
        $("a[" + obj.tracker_attr + "]").bind('mousedown', function(e) {
            e.preventDefault();
            obj.changeHref(this);
        });
    }
};