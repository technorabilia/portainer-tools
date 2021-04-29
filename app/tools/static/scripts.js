var socket;
$(document).ready(function () {
    socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('merge response', function (data) {
        if (data.error)
            showAlert(data.message, "danger")
        else {
            showAlert(data.message + " Refresh in 5 seconds...", "success")
            setTimeout(function () {
                if (window.location.pathname == "/")
                    location.reload()
            }, 5000);
        }
    });

    $('#merge-button').submit(function () {
        socket.emit('merge templates', $('#table').bootstrapTable('getSelections'));
        return false;
    });

    function showAlert(message, alertType) {
        $('#alert-client').html('<div id="alertdiv" class="alert alert-' + alertType + ' mt-4"><span>' + message + '</span></div>')
    }
});