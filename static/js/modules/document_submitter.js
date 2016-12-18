DocumentSubmitter = (function(){

    var settings = {
        postURL: '/document/submit'
    };

    return {
        init: function () {
            // form input
            settings.formElements = {
                title: $('#form_title'),
                summary: $('#form_summary'),
                originalUrl: $('#form_original_url'),
                source: $('#form_source'),
                submitBtn: $("#submit_button")
            };

            // elements displaying validation error messages
            settings.validationErrorBoxes = {
                title: $('#form_title_validation'),
                summary: $('#form_summary_validation'),
                originalUrl: $('#form_original_url_validation'),
                source: $('#form_source_validation')
            };

            settings.statusBox = $("#status_bar");

            settings.formElements.title.focus();
            this.bindUIActions();
        },

        validate: function () {
            settings.validationErrorBoxes.title.text('');
            settings.validationErrorBoxes.summary.text('');
            settings.validationErrorBoxes.originalUrl.text('');
            settings.validationErrorBoxes.source.text('');
            isValid = true;
            if ( settings.formElements.title.val() == '' ){
                settings.validationErrorBoxes.title.text('Title should not be empty');
                isValid = false;
            }
            if ( settings.formElements.summary.val() == '' ){
                settings.validationErrorBoxes.summary.text('Summary, however concise, is required');
                isValid = false;
            }
            if ( settings.formElements.originalUrl.val() == '' ){
                settings.validationErrorBoxes.originalUrl.text('Point to the document by pasting its original URL in the box');
                isValid = false;
            }
            if ( settings.formElements.source.val() == '' ){
                settings.validationErrorBoxes.source.text('Source of document is required to be specified');
                isValid = false;
            }
            return isValid;
        },

        submitDoc: function (newDocInfo, validatorFunc) {
            newDocInfo['g_recaptcha_response'] = $('#g-recaptcha-response').val();
            validation = validatorFunc();
            if (validation == true) {
                $.post(settings.postURL, data=newDocInfo, function(data) {
                    settings.statusBox.show();
                    setTimeout(function() {
                        settings.statusBox.click();
                    }, 5000);
                });
            }
        },

        clearAllFields: function () {
            settings.formElements.title.val('');
            settings.formElements.summary.val('');
            settings.formElements.originalUrl.val('');
            settings.formElements.source.val('');

            settings.validationErrorBoxes.title.val('');
            settings.validationErrorBoxes.summary.val('');
            settings.validationErrorBoxes.originalUrl.val('');
            settings.validationErrorBoxes.source.val('');
        },

        bindUIActions: function() {
            submitDoc = this.submitDoc;
            validatorFunc = this.validate;
            clearFields = this.clearAllFields;
            settings.formElements.submitBtn.click(function (e) {
                newDocInfo = {
                    title: settings.formElements.title.val(),
                    summary: settings.formElements.summary.val(),
                    original_url: settings.formElements.originalUrl.val(),
                    source: settings.formElements.source.val(),
                };
                submitDoc(newDocInfo, validatorFunc);
            });
            settings.statusBox.click(function (e) {
                clearFields();
                settings.statusBox.hide();
            });
        },
    }
})();
