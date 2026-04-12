/**
 * Input Lab — Mining Interface
 * Tap words to look up definitions, mine up to 5 per text.
 */
(function () {
    "use strict";

    var data = LAB_MINE_DATA;
    var sentencesArea = document.getElementById("sentences-area");
    var mineTray = document.getElementById("mine-tray");
    var mineCounter = document.getElementById("mine-counter");
    var minedCount = data.mined_count || 0;
    var currentPopup = null;

    function init() {
        renderSentences();
    }

    function renderSentences() {
        sentencesArea.innerHTML = "";
        data.sentences.forEach(function (sent, i) {
            var p = document.createElement("div");
            p.className = "lab-sentence";

            var words = sent.split(/(\s+)/);
            words.forEach(function (token) {
                if (/^\s+$/.test(token)) {
                    p.appendChild(document.createTextNode(token));
                    return;
                }
                var span = document.createElement("span");
                span.className = "lab-word";
                span.textContent = token;

                var clean = token.replace(/^[^\wÄÖÜäöüß]+|[^\wÄÖÜäöüß]+$/g, "");
                span.dataset.word = clean;
                span.dataset.sentence = sent;

                span.addEventListener("click", function (e) {
                    e.stopPropagation();
                    showMinePopup(clean, sent, span);
                });

                p.appendChild(span);
            });

            sentencesArea.appendChild(p);
        });
    }

    function _renderLookupBody(d) {
        var html = "";
        if (d.frequency != null) {
            html += '<div class="duden-wordtype">Häufigkeit: ' + d.frequency.toLocaleString() + " (Klasse " + d.frequency_class + ")</div>";
        }
        if (d.synonyms && d.synonyms.length) {
            html += '<div class="duden-def"><strong>Synonyme:</strong> ' + d.synonyms.join(", ") + "</div>";
        }
        if (d.collocations && d.collocations.length) {
            html += '<div class="duden-def"><strong>Kollokationen:</strong> ' + d.collocations.join(", ") + "</div>";
        }
        if (d.examples && d.examples.length) {
            html += '<div class="duden-examples"><strong>Beispiele:</strong><ul>';
            d.examples.forEach(function (ex) { html += "<li>" + ex + "</li>"; });
            html += "</ul></div>";
        }
        if (!html) html = '<div class="duden-def">Keine Informationen gefunden.</div>';
        return html;
    }

    function _buildSaveDefinition(d) {
        var parts = [];
        if (d.synonyms && d.synonyms.length) parts.push("Synonyme: " + d.synonyms.join(", "));
        if (d.collocations && d.collocations.length) parts.push("Kollokationen: " + d.collocations.join(", "));
        if (d.frequency != null) parts.push("Häufigkeit: " + d.frequency.toLocaleString());
        return parts.join(" · ") || d.definition || "";
    }

    function showMinePopup(word, sentence, el) {
        closePopup();

        var popup = document.createElement("div");
        popup.className = "duden-popup";
        popup.innerHTML =
            '<div class="duden-popup-header">' +
            "  <strong>" + word + "</strong>" +
            '  <button class="duden-close-btn" title="Close">&times;</button>' +
            "</div>" +
            '<div class="duden-popup-body">' +
            '  <div class="duden-loading">Loading...</div>' +
            "</div>" +
            '<div class="duden-popup-actions">' +
            '  <button class="btn btn-primary btn-sm mine-btn" ' +
            (minedCount >= 5 ? "disabled" : "") + ">Mine</button>" +
            '  <a class="btn btn-secondary btn-sm" href="https://www.openthesaurus.de/synonyme/' +
            encodeURIComponent(word) + '" target="_blank" rel="noopener">OpenThesaurus</a>' +
            "</div>";

        document.body.appendChild(popup);
        currentPopup = popup;

        var rect = el.getBoundingClientRect();
        var top = rect.top - 300;
        if (top < 10) top = rect.bottom + 8;
        var left = rect.left;
        if (left + 320 > window.innerWidth) left = window.innerWidth - 330;
        if (left < 10) left = 10;
        popup.style.top = top + "px";
        popup.style.left = left + "px";

        popup.querySelector(".duden-close-btn").addEventListener("click", closePopup);

        var lookupData = null;

        fetch("/api/duden/" + encodeURIComponent(word))
            .then(function (r) { return r.json(); })
            .then(function (d) {
                lookupData = d;
                popup.querySelector(".duden-popup-body").innerHTML = _renderLookupBody(d);
            })
            .catch(function () {
                popup.querySelector(".duden-popup-body").innerHTML =
                    '<div class="duden-def">Fehler beim Laden.</div>';
            });

        popup.querySelector(".mine-btn").addEventListener("click", function () {
            if (minedCount >= 5) return;
            var btn = this;
            btn.disabled = true;
            btn.textContent = "Saving...";

            fetch("/api/lab/" + data.text_id + "/mine", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    word: word,
                    definition: lookupData ? _buildSaveDefinition(lookupData) : "",
                    examples: lookupData && lookupData.examples ? lookupData.examples.join("\n") : "",
                    source_sentence: sentence
                })
            })
                .then(function (r) { return r.json(); })
                .then(function (result) {
                    if (result.error) {
                        btn.textContent = result.error;
                        return;
                    }
                    minedCount = result.count;
                    mineCounter.textContent = minedCount + "/5";
                    btn.textContent = "Mined!";

                    var chip = document.createElement("span");
                    chip.className = "lab-mined-chip";
                    chip.textContent = word;
                    mineTray.appendChild(chip);

                    el.classList.add("mined");
                    closePopup();
                })
                .catch(function () {
                    btn.textContent = "Error";
                });
        });

        setTimeout(function () {
            document.addEventListener("click", onClickOutside);
        }, 100);
    }

    function closePopup() {
        if (currentPopup) {
            currentPopup.remove();
            currentPopup = null;
        }
        document.removeEventListener("click", onClickOutside);
    }

    function onClickOutside(e) {
        if (currentPopup && !currentPopup.contains(e.target) && !e.target.closest(".lab-word")) {
            closePopup();
        }
    }

    init();
})();
