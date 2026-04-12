/**
 * Input Lab — Flow Mode Reader
 * Renders sentences with tappable words, tracks reading progress,
 * and provides Duden lookup popups.
 */
(function () {
    "use strict";

    var data = LAB_DATA;
    var readerArea = document.getElementById("reader-area");
    var progressFill = document.getElementById("progress-fill");
    var floatingBar = document.getElementById("floating-bar");
    var segmentsRead = 0;
    var totalSegments = data.segments.length;
    var currentPopup = null;

    function init() {
        renderSentences();
        updateProgress();
    }

    function renderSentences() {
        readerArea.innerHTML = "";
        data.segments.forEach(function (seg, i) {
            var p = document.createElement("div");
            p.className = "lab-sentence";
            p.dataset.segIndex = i;
            p.dataset.segId = seg.id;

            if (seg.read_at) {
                p.classList.add("read");
                segmentsRead++;
            }

            var words = seg.sentence_text.split(/(\s+)/);
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

                if (data.unknown_words && data.unknown_words.indexOf(clean.toLowerCase()) >= 0) {
                    span.classList.add("unknown");
                }

                span.addEventListener("click", function (e) {
                    e.stopPropagation();
                    showDudenPopup(clean, span);
                });

                p.appendChild(span);
            });

            // Mark as read when clicked/tapped
            p.addEventListener("click", function () {
                if (!p.classList.contains("read")) {
                    p.classList.add("read");
                    segmentsRead++;
                    updateProgress();
                    // Notify server
                    fetch("/api/lab/" + data.text_id + "/segment/" + i + "/read", {
                        method: "POST"
                    });
                }
            });

            readerArea.appendChild(p);
        });

        updateProgress();
    }

    function updateProgress() {
        var pct = totalSegments > 0 ? (segmentsRead / totalSegments * 100) : 0;
        progressFill.style.width = pct + "%";
        if (segmentsRead >= Math.ceil(totalSegments * 0.5)) {
            floatingBar.style.display = "";
        }
    }

    // ─── WORD LOOKUP POPUP ──────────────────────────────
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

    function showDudenPopup(word, el) {
        closeDudenPopup();

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
            '  <button class="btn btn-primary btn-sm duden-save-btn" disabled>Save Word</button>' +
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

        popup.querySelector(".duden-close-btn").addEventListener("click", closeDudenPopup);

        var lookupData = null;

        fetch("/api/duden/" + encodeURIComponent(word))
            .then(function (r) { return r.json(); })
            .then(function (d) {
                lookupData = d;
                popup.querySelector(".duden-popup-body").innerHTML = _renderLookupBody(d);
                popup.querySelector(".duden-save-btn").disabled = false;
            })
            .catch(function () {
                popup.querySelector(".duden-popup-body").innerHTML =
                    '<div class="duden-def">Fehler beim Laden.</div>';
                popup.querySelector(".duden-save-btn").disabled = false;
            });

        var sentenceEl = el.closest(".lab-sentence");
        var sourceSentence = sentenceEl ? sentenceEl.textContent.trim() : "";

        popup.querySelector(".duden-save-btn").addEventListener("click", function () {
            var btn = this;
            btn.disabled = true;
            btn.textContent = "Saving...";

            fetch("/api/words", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    word: word,
                    definition: lookupData ? _buildSaveDefinition(lookupData) : "",
                    examples: lookupData && lookupData.examples ? lookupData.examples.join("\n") : "",
                    source_sentence: sourceSentence
                })
            })
                .then(function () {
                    btn.textContent = "Saved!";
                    el.classList.add("saved");
                })
                .catch(function () {
                    btn.textContent = "Error";
                    btn.disabled = false;
                });
        });

        setTimeout(function () {
            document.addEventListener("click", onClickOutside);
        }, 100);
    }

    function closeDudenPopup() {
        if (currentPopup) {
            currentPopup.remove();
            currentPopup = null;
        }
        document.removeEventListener("click", onClickOutside);
    }

    function onClickOutside(e) {
        if (currentPopup && !currentPopup.contains(e.target) && !e.target.closest(".lab-word")) {
            closeDudenPopup();
        }
    }

    init();
})();
