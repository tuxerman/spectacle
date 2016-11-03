PopularTopics = (function(){
    var settings = {
      getPopularTopicsURL: '/popular',
      numTopicsToFetch: 5,
    };

    return {
        init: function () {
            this.bindUI();
            this.getPopularTopics();
        },
        bindUI: function() {
            settings.popularTopicsDiv = $('#popular_topics');
        },
        getPopularTopics: function () {
            $.get("/popular", function(data) {
                console.log(data);
            });
        }
    }
})();