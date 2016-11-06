Searcher = (function(){
    var settings = {
      searchURL: '/document/search'
    };

    return {
        init: function () {
            settings.searchBox = $('#search_string');
            settings.searchButton = $('#search_button');
            settings.searchResultsPanel = $('#search_results_panel');
            settings.searchResultsDiv = $('#search_results');
            settings.homepageFeaturesPanel=$('#homepage-features-panel');
            settings.searchBox.focus();
            this.bindUIActions();
        },

        doSearch: function (searchString) {
            searchQuery = settings.searchBox.val();
            $.get(settings.searchURL, {query: searchQuery}, function(data) {
                settings.searchResultsDiv.empty();
                settings.searchResultsPanel.show();
                settings.homepageFeaturesPanel.hide();
                $.each(data, function(i, result){
                    result_doc = result.document;
                    result_snippet = result.snippet;
                    settings.searchResultsDiv.append('<a href="/document/' + result_doc.id + '"> <h5>' + result_doc.title + '</h5> </a>');
                    settings.searchResultsDiv.append("<p>" + result_snippet + "</p>");
                });
            });
        },

        bindUIActions: function() {
            searchFunction = this.doSearch;
            settings.searchButton.click(function (e) {
              searchFunction(settings.searchBox.val());
            });
            settings.searchBox.on('keydown', function(e) {
                if (e.keyCode == 13)
                    settings.searchButton.click();
            });
        },
    }
})();
