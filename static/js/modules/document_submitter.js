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
            settings.statusBox = $("#status_bar");

            settings.titleBox.focus();
            this.bindUIActions();
        },
        submitDoc: function (newDocInfo) {
            $.post(settings.postURL, data=newDocInfo, function(data) {
                settings.statusBox.show();
                setTimeout(function() {
                    settings.statusBox.click();
                }, 5000);
            });
        },
        clearAllFields: function () {
            settings.titleBox.val('');
            settings.summaryBox.val('');
            settings.topicIdBox.val('');
            settings.originalUrlBox.val('');
            settings.sourceBox.val('');
        },
        bindUIActions: function() {
            submitDoc = this.submitDoc;
            clearFields = this.clearAllFields;
            settings.submitButton.click(function (e) {
                newDocInfo = {
                    'title': settings.titleBox.val(),
                    'summary': settings.summaryBox.val(),
                    'topic_id': settings.topicIdBox.val(),
                    'original_url': settings.originalUrlBox.val(),
                    'source': settings.sourceBox.val()
                }
                submitDoc(newDocInfo);
            });
            settings.statusBox.click(function (e) {
                clearFields();
                settings.statusBox.hide();
            });
        },
    }
})();