DocumentReviewer = (function(){
    var settings = {
    };

    return {
        init: function () {
            // form input
            settings.titleBox = $('#form_title');
            settings.contentBox = $('#form_content');
            settings.summaryBox = $('#form_summary');
            settings.topicIdBox = $('#form_topic_id');
            settings.originalUrlBox = $('#form_original_url');
            settings.sourceBox = $('#form_source');
            settings.publishButton = $("#publish_button");
            settings.docId = globalDocId;
            settings.postURL = '/document/publish/' + globalDocId;
            settings.statusBox = $("#status_bar");

            settings.titleBox.focus();
            this.bindUIActions();
        },
        publishFunction: function (editedDocInfo) {
            $.post(settings.postURL, data=editedDocInfo, function(data) {
                settings.statusBox.show();
                setTimeout(function() {
                    settings.statusBox.hide();
                    window.location.href = '/review';
                }, 5000);
            });
        },
        bindUIActions: function() {
            addFunction = this.publishFunction;
            settings.publishButton.click(function (e) {
                editedDocInfo = {
                    'id': settings.docId,
                    'title': settings.titleBox.val(),
                    'content': settings.contentBox.val(),
                    'summary': settings.summaryBox.val(),
                    'topic_id': settings.topicIdBox.val(),
                    'original_url': settings.originalUrlBox.val(),
                    'source': settings.sourceBox.val()
                }
                addFunction(editedDocInfo);
            });
            settings.statusBox.click(function (e) {
                settings.statusBox.hide();
                window.location.href = '/review';
            });
        },
    }
})();