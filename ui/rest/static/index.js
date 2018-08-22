function get(id) {
    return document.getElementById(id);
}

function getUrl() {
    return 'single/' + get('address').value;
}

function setError(msg) {
    if (msg) {
        get('error_div').style.visibility = 'visible';
        get('error_text').value = msg;
    } else {
        get('error_div').style.visibility = 'hidden';
    }
}

function clickGet() {
    $.ajax({
        type: 'GET',
        url: getUrl(),
        success: function(resp) {
            setError(resp.error);
            get('value').value = resp.error ? '' : resp.value;
        },
        error: function() {
            setError('Didn\'t GET URL ' + getUrl())
        }
    });
}

function clickSet() {
    $.ajax({
        type: 'PUT',
        data: {
            value: get('value').value,
        },
        url: getUrl(),

        success: function(resp) {
            setError(resp.error);
        },

        error: function() {
            setError('Didn\'t PUT URL ' + getUrl());
        }
    });
}

function clickClear() {
    get('value').value = '';
    setError();
}
