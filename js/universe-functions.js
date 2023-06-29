
// THESE FUNCTIONS ONLY TRIGGER ON PAGE INTERACTION //


function hide(univ, prefix, component) {
    var templates = document.querySelectorAll('div[id^="' + univ + '-' + prefix + '-"]');
    targetID = univ + '-' + prefix + '-' + component.filename;
    target = null;

    templates.forEach(template => {
        if(template.id == targetID) {
            target = template;
        }
    });

    if(target == null) {
        console.log("error: cannot find template ", component);
    }
    else {
        try {
        window.Plotly.purge(target.getElementsByClassName('plotly-graph-div')[0]);
        } catch (e) { }
        let n = getComment(target.childNodes[0]).nextSibling;
        while(n) {
            const next = n.nextSibling;
            $(n).remove();
            n = next;
        }
    }
}

function hideTemplates(univ) {
    const {tableLookup, pnlLookup, dnpnlLookup} = universes[univ];
    hide(univ, 'table', getCurrentTemplate(univ, tableLookup, true));
    hide(univ, 'pnl', getCurrentTemplate(univ, pnlLookup, false));
    hide(univ, 'dnpnl', getCurrentTemplate(univ, dnpnlLookup, true));
}

function navigateRange(univ, direction) {
    const {pnlLookup} = universes[univ];
    hideTemplates(univ);
    universes[univ].currentIndex += direction;
    if (universes[univ].currentIndex < 0) universes[univ].currentIndex = 0;
    if (universes[univ].currentIndex >= pnlLookup.length) universes[univ].currentIndex = pnlLookup.length - 1;
    showTemplates(univ);
    updateNavButtons(univ);
}

function updateNavButtons(univ) {
    const {currentIndex, pnlLookup} = universes[univ];
    if (currentIndex == 0) {
        rangeLabel = 'Top 5';
    } else {
        currTemplate = getCurrentTemplate(univ, pnlLookup, false);
        rangeLabel = currTemplate.range;
    }
    document.getElementById(univ + '-range-indicator').innerText = rangeLabel;
    document.getElementById(univ + '-prev').disabled = (currentIndex === 0);
    document.getElementById(univ + '-next').disabled = (currentIndex === pnlLookup.length - 1);
    document.getElementById(univ + '-top').style.visibility = (currentIndex === 0) ? 'hidden' : 'visible';
}

function goToTop(univ) {
    hideTemplates(univ);
    universes[univ].currentIndex = 0;
    showTemplates(univ);
    updateNavButtons(univ);
}

function toggleDNMode(univ, dnmode) {
    hideTemplates(univ);
    universes[univ].currentDNMode = dnmode;
    showTemplates(univ);
}

// Listen to whether dropdown item is selected
document.addEventListener("DOMContentLoaded", function () {
    var dropdownItems = document.querySelectorAll('.dropdown-item');
    dropdownItems.forEach(function (item) {
        item.addEventListener('click', function (event) {
            dropdownItems.forEach(function (i) {
                i.classList.remove('selected-item');
            });
            event.currentTarget.classList.add('selected-item');
        });
    });
});