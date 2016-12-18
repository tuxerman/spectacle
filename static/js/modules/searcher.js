Searcher = (function() {
    var settings = {
        searchURL: '/document/search',
        defaultPageSize: 15
    };

    return {
        init: function() {
            settings.searchBox = $('#search_string');
            settings.searchButton = $('#search_button');
            settings.searchResultsPanel = $('#search_results_panel');
            settings.searchResultsDiv = $('#search_results');
            settings.homepageFeaturesPanel = $('#homepage-features-panel');
            settings.searchBoxLeftSpacer = $('#searchbox-left-spacer');
            settings.hero = $('#hero');
            settings.searchBox.focus();
            this.bindUIActions();
        },

        doSearch: function(searchString) {
            searchQuery = settings.searchBox.val();
            $.get(settings.searchURL, {
                query: searchQuery,
                page_size: settings.defaultPageSize
            }, function(data) {
                settings.searchResultsDiv.empty();
                settings.searchResultsPanel.show();
                settings.homepageFeaturesPanel.hide();
                settings.searchBoxLeftSpacer.remove();
                settings.hero.hide();
                $.each(data.results, function(i, result) {
                    result_doc_id = result.doc_id;
                    result_title = result.title;
                    result_snippet = result.snippet;
                    settings.searchResultsDiv.append('<a href="/document/' + result_doc_id + '"> <h5>' + result_title + '</h5> </a>');
                    settings.searchResultsDiv.append("<p>" + result_snippet + "</p>");
                });
            });
        },

        bindUIActions: function() {
            searchFunction = this.doSearch;
            settings.searchButton.click(function(e) {
                if (settings.searchBox.val()) {
                    searchFunction(settings.searchBox.val());
                }
            });
            settings.searchBox.on('keydown', function(e) {
                if (e.keyCode == 13)
                    settings.searchButton.click();
            });
        },
    }
})();
