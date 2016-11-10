DocumentSubmitter = (function(){
    var settings = {
        postURL: '/document/submit'
    };

    return {
        init: function () {
            // form input
            settings.titleBox = $('#form_title');
            settings.summaryBox = $('#form_summary');
            settings.topicIdBox = $('#form_topic_id');
            settings.originalUrlBox = $('#form_original_url');
            settings.sourceBox = $('#form_source');
            settings.submitButton = $("#submit_button");

            settings.titleBox.focus();
            this.bindUIActions();
        },
        submitDoc: function (newDocInfo) {
            $.post(settings.postURL, data=newDocInfo, function(data) {
                alert("New document has been submitted for review");
                window.location.href = '/';
            });
        },
        bindUIActions: function() {
            addFunction = this.submitDoc;
            settings.submitButton.click(function (e) {
                newDocInfo = {
                    'title': settings.titleBox.val(),
                    'summary': settings.summaryBox.val(),
                    'topic_id': settings.topicIdBox.val(),
                    'original_url': settings.originalUrlBox.val(),
                    'source': settings.sourceBox.val()
                }
                addFunction(newDocInfo);
            });
        },
    }
})();