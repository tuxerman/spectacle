DocumentSubmitter = (function(){
    var settings = {
        postURL: '/document/submit'
    };

    return {
        init: function () {
            // form input
            settings.titleBox = $('#form_title');
            settings.contentBox = $('#form_content');
            settings.topicIdBox = $('#form_topic_id');
            settings.originalUrlBox = $('#form_original_url');
            settings.sourceBox = $('#form_source');
            settings.submitButton = $("#submit_button");

            settings.titleBox.focus();
            this.bindUIActions();
        },
        submitDoc: function (newDocInfo) {
            $.post(settings.postURL, data=newDocInfo, function(data) {
                console.log(data.id);
                alert("New document has been submitted for review:" + data.id);
            });
            window.location.href = '/';
        },
        bindUIActions: function() {
            addFunction = this.submitDoc;
            settings.submitButton.click(function (e) {
                newDocInfo = {
                    'title': settings.titleBox.val(),
                    'content': settings.contentBox.val(),
                    'topic_id': settings.topicIdBox.val(),
                    'original_url': settings.originalUrlBox.val(),
                    'source': settings.sourceBox.val()
                }
                addFunction(newDocInfo);
            });
        },
    }
})();