DocumentReviewer = (function(){
    var settings = {
    };

    return {
        init: function () {
            // form input
            settings.titleBox = $('#form_title');
            settings.contentBox = $('#form_content');
            settings.summaryBox = $('#form_summary');
            settings.originalUrlBox = $('#form_original_url');
            settings.sourceBox = $('#form_source');
            settings.publishButton = $("#publish_button");
            settings.discardButton = $("#discard_button");
            settings.docId = globalDocId;
            settings.postURL = '/document/publish/' + globalDocId;
            settings.discardURL = '/document/discard/' + globalDocId;
            settings.statusBox = $("#status_bar");

            settings.titleBox.focus();
            this.bindUIActions();
        },
        discardFunction: function () {
            $.post(settings.discardURL, function(data) {
                console.log('discard successful');
                setTimeout(function() {
                    window.location.href = '/review';
                }, 5000);
            });
        },
        publishFunction: function (editedDocInfo) {
            $.post(settings.postURL, data=editedDocInfo, function(data) {
                settings.statusBox.show();
                window.location.hash = '#status_bar';
                setTimeout(function() {
                    settings.statusBox.hide();
                    window.location.href = '/review';
                }, 5000);
            });
        },
        bindUIActions: function() {
            // publish document
            addFunction = this.publishFunction;
            settings.publishButton.click(function (e) {
                editedDocInfo = {
                    id: settings.docId,
                    title: settings.titleBox.val(),
                    content: settings.contentBox.val(),
                    summary: settings.summaryBox.val(),
                    original_url: settings.originalUrlBox.val(),
                    source: settings.sourceBox.val()
                };
                addFunction(editedDocInfo);
            });

            // discard document
            delFunction = this.discardFunction;
            settings.discardButton.click(function (e) {
                delFunction(settings.docId);
            });

            // statusbox
            settings.statusBox.click(function (e) {
                settings.statusBox.hide();
                window.location.href = '/review';
            });
        },
    }
})();
