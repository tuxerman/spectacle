SimpleStatusBar = (function(){
    var settings = {};

    return {
        init: function () {
            settings.statusBox = $("#status_bar");
            this.bindUIActions();
        },
        bindUIActions: function() {
            settings.statusBox.click(function (e) {
                settings.statusBox.hide();
            });
        },
    }
})();