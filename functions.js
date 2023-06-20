function formatDate() {
    var today = new Date();
    var options = { year: 'numeric', month: 'short', day: '2-digit'};
    var formattedDate = today.toLocaleDateString('en-US', options);
    document.getElementById('date').textContent = formattedDate;
}

// Append today's date to the href attributes
function appendDateToHrefs() {
    var anchors = document.getElementsByTagName('a');
    var formattedDate = getFormattedDate();

    for (var i = 0; i < anchors.length; i++) {
    var href = anchors[i].getAttribute('href');
    href += '?t=' + formattedDate;
    anchors[i].setAttribute('href', href);
    }
}

// Get today's date in YYYYMMDD format
function getFormattedDate() {
    var today = new Date();
    var year = today.getFullYear();
    var month = String(today.getMonth() + 1).padStart(2, '0');
    var day = String(today.getDate()).padStart(2, '0');
    return year + month + day;
}