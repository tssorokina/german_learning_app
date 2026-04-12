/**
 * Verb-End Torture Chamber — Full-Sentence Drag & Drop Exercise Engine
 * Touch-friendly: works on iPhone/Android via pointer events.
 *
 * Modes:
 *   - Tap: tap a word chip to place it in the next open slot
 *   - Drag: drag a chip onto any slot
 *   - Long-press: hold a chip to see Duden dictionary popup
 */
(function () {
    "use strict";

    const exercise = EXERCISE_DATA;
    const retryId = RETRY_ID;
    const sentenceArea = document.getElementById("sentence-area");
    const wordTray = document.getElementById("word-tray");
    const btnCheck = document.getElementById("btn-check");
    const btnReset = document.getElementById("btn-reset");
    const resultArea = document.getElementById("result-area");
    const clauseType = document.getElementById("clause-type");

    // State
    let slotElements = [];
    let chipElements = [];
    let dragState = null;
    let selectedChip = null;
    let longPressTimer = null;
    const LONG_PRESS_DURATION = 500; // ms
    const exerciseStartTime = Date.now();

    // ─── SCAFFOLD LEVELS ────────────────────────────────
    // 0 = A2/B1: translation collapsed (tap to reveal), verb slots highlighted
    // 1 = B1/B2: translation hidden, 1 hint available (reveal next correct word)
    // 2 = B2/C1: no translation, no hints
    const scaffoldLevel = exercise.scaffold_level || 0;

    // ─── INIT ────────────────────────────────────────────
    function init() {
        clauseType.textContent = exercise.clause_type.replace(/_/g, " ");

        // Scaffold Level 0: translation collapsed behind a toggle
        // Scaffold Level 1: translation hidden entirely (but hint button shown)
        // Scaffold Level 2: no translation, no hints
        var translationEl = document.getElementById("english-translation");
        if (exercise.english && translationEl) {
            if (scaffoldLevel === 0) {
                translationEl.textContent = exercise.english;
                translationEl.classList.add("scaffold-collapsed");
                translationEl.title = "Tap to reveal translation";
                translationEl.addEventListener("click", function () {
                    translationEl.classList.toggle("scaffold-collapsed");
                });
            } else {
                translationEl.style.display = "none";
            }
        }

        renderSentence();
        renderWords();

        // Scaffold Level 0: highlight verb slots
        if (scaffoldLevel === 0 && exercise.verb_indices) {
            exercise.verb_indices.forEach(function (vi) {
                if (slotElements[vi]) {
                    slotElements[vi].classList.add("verb-hint-slot");
                }
            });
        }

        // Scaffold Level 0-1: add hint button
        if (scaffoldLevel <= 1) {
            _addHintButton();
        }

        btnCheck.addEventListener("click", checkAnswer);
        btnReset.addEventListener("click", resetExercise);
    }

    let hintsUsed = 0;
    const maxHints = scaffoldLevel === 0 ? 2 : 1;

    function _addHintButton() {
        const actionBar = btnCheck.parentElement;
        const hintBtn = document.createElement("button");
        hintBtn.className = "btn btn-hint";
        hintBtn.id = "btn-hint";
        hintBtn.textContent = "Hint (" + maxHints + " left)";
        actionBar.appendChild(hintBtn);

        hintBtn.addEventListener("click", function () {
            if (hintsUsed >= maxHints) return;
            // Find next empty or wrong slot and reveal correct word
            const exercise_words = exercise.shuffled_words;
            for (let i = 0; i < slotElements.length; i++) {
                const placed = slotElements[i].querySelector(".placed-word");
                if (!placed.textContent) {
                    // Find the correct word for this position from the template
                    // We just flash the slot as a positional hint
                    slotElements[i].classList.add("flash-wrong");
                    setTimeout(function () {
                        slotElements[i].classList.remove("flash-wrong");
                    }, 1500);
                    hintsUsed++;
                    const remaining = maxHints - hintsUsed;
                    hintBtn.textContent = remaining > 0
                        ? "Hint (" + remaining + " left)"
                        : "No hints left";
                    if (remaining <= 0) hintBtn.disabled = true;
                    break;
                }
            }
        });
    }

    function renderSentence() {
        sentenceArea.innerHTML = "";
        slotElements = [];
        const numSlots = exercise.num_slots;
        const prefixes = exercise.slot_prefixes || [];
        const suffixes = exercise.slot_suffixes;

        for (let i = 0; i < numSlots; i++) {
            const wrapper = document.createElement("span");
            wrapper.className = "slot-wrapper";

            // Leading punctuation (quotes, brackets) BEFORE the slot
            if (prefixes[i]) {
                const pre = document.createElement("span");
                pre.className = "slot-punct slot-prefix";
                pre.textContent = prefixes[i];
                wrapper.appendChild(pre);
            }

            const el = document.createElement("span");
            el.className = "slot";
            el.dataset.slotIndex = i;
            el.innerHTML = '<span class="placed-word"></span>';
            slotElements.push(el);
            wrapper.appendChild(el);

            // Trailing punctuation AFTER the slot
            if (suffixes[i]) {
                const punct = document.createElement("span");
                punct.className = "slot-punct";
                punct.textContent = suffixes[i];
                wrapper.appendChild(punct);
            }

            sentenceArea.appendChild(wrapper);

            // Drop target listeners
            el.addEventListener("pointerover", onSlotOver);
            el.addEventListener("pointerout", onSlotOut);
            el.addEventListener("click", onSlotClick);
        }
    }

    function renderWords() {
        wordTray.innerHTML = "";
        chipElements = [];
        exercise.shuffled_words.forEach((word, i) => {
            const chip = document.createElement("span");
            chip.className = "word-chip";
            chip.textContent = word;
            chip.dataset.word = word;
            chip.dataset.chipIndex = i;

            // Interaction handlers
            chip.addEventListener("pointerdown", onChipDown);
            chip.addEventListener("click", onChipClick);

            chipElements.push(chip);
            wordTray.appendChild(chip);
        });
    }

    // ─── TAP TO PLACE ────────────────────────────────────
    function onChipClick(e) {
        if (dragState) return;
        const chip = e.currentTarget;
        if (chip.classList.contains("placed")) return;

        // If we just came from a long-press, skip
        if (chip._longPressTriggered) {
            chip._longPressTriggered = false;
            return;
        }

        // Tap-to-place: put in next open slot
        const nextSlot = slotElements.find(s =>
            s.querySelector(".placed-word").textContent === "");
        if (nextSlot) {
            placeWord(chip, nextSlot);
        }
    }

    function onSlotClick(e) {
        const slot = e.currentTarget;
        // If slot has a word, return it to tray
        const placed = slot.querySelector(".placed-word");
        if (placed && placed.textContent) {
            returnToTray(placed.textContent, slot);
        }
    }

    // ─── DRAG & LONG-PRESS (pointer events) ─────────────
    function onChipDown(e) {
        const chip = e.currentTarget;
        if (chip.classList.contains("placed")) return;

        e.preventDefault();

        const startX = e.clientX;
        const startY = e.clientY;
        let isDragging = false;
        chip._longPressTriggered = false;

        // Start long-press timer
        longPressTimer = setTimeout(() => {
            if (!isDragging) {
                chip._longPressTriggered = true;
                showDudenPopup(chip.dataset.word, chip);
            }
        }, LONG_PRESS_DURATION);

        chip.setPointerCapture(e.pointerId);

        const onMove = (ev) => {
            const dx = Math.abs(ev.clientX - startX);
            const dy = Math.abs(ev.clientY - startY);

            // If moved enough, start drag
            if (!isDragging && (dx > 5 || dy > 5)) {
                isDragging = true;
                clearTimeout(longPressTimer);
                startDrag(chip, ev);
            }

            if (isDragging && dragState) {
                dragState.ghost.style.left = ev.clientX + "px";
                dragState.ghost.style.top = ev.clientY + "px";

                // Highlight slot under pointer
                const target = document.elementFromPoint(ev.clientX, ev.clientY);
                slotElements.forEach(s => s.classList.remove("drag-over"));
                if (target && target.closest(".slot")) {
                    target.closest(".slot").classList.add("drag-over");
                }
            }
        };

        const onUp = (ev) => {
            clearTimeout(longPressTimer);

            if (isDragging && dragState) {
                chip.classList.remove("dragging");
                dragState.ghost.remove();

                const target = document.elementFromPoint(ev.clientX, ev.clientY);
                const slotEl = target ? target.closest(".slot") : null;
                slotElements.forEach(s => s.classList.remove("drag-over"));

                if (slotEl) {
                    const existing = slotEl.querySelector(".placed-word");
                    if (existing && existing.textContent) {
                        returnToTray(existing.textContent, slotEl);
                    }
                    placeWord(chip, slotEl);
                }

                dragState = null;
            }

            chip.removeEventListener("pointermove", onMove);
            chip.removeEventListener("pointerup", onUp);
            chip.removeEventListener("pointercancel", onUp);
        };

        chip.addEventListener("pointermove", onMove);
        chip.addEventListener("pointerup", onUp);
        chip.addEventListener("pointercancel", onUp);
    }

    function startDrag(chip, ev) {
        const ghost = document.createElement("div");
        ghost.className = "drag-ghost";
        ghost.textContent = chip.textContent;
        document.body.appendChild(ghost);
        ghost.style.left = ev.clientX + "px";
        ghost.style.top = ev.clientY + "px";

        chip.classList.add("dragging");
        dragState = { chip, ghost, originSlot: null };
    }

    function onSlotOver(e) {
        if (dragState) e.currentTarget.classList.add("drag-over");
    }
    function onSlotOut(e) {
        e.currentTarget.classList.remove("drag-over");
    }

    // ─── PLACE / RETURN ──────────────────────────────────
    function placeWord(chip, slotEl) {
        const placed = slotEl.querySelector(".placed-word");
        placed.textContent = chip.dataset.word;
        slotEl.dataset.chipId = chip.dataset.chipIndex;
        slotEl.classList.add("filled");
        chip.classList.add("placed");
        updateCheckButton();
    }

    function returnToTray(word, slotEl) {
        const placed = slotEl.querySelector(".placed-word");
        placed.textContent = "";
        const chipId = slotEl.dataset.chipId;
        delete slotEl.dataset.chipId;
        slotEl.classList.remove("filled");
        // Use chip ID for exact match (handles duplicate words correctly)
        if (chipId != null) {
            for (const c of chipElements) {
                if (c.dataset.chipIndex === chipId) {
                    c.classList.remove("placed");
                    break;
                }
            }
        }
        updateCheckButton();
    }

    function updateCheckButton() {
        const allFilled = slotElements.every(s =>
            s.querySelector(".placed-word").textContent !== "");
        btnCheck.disabled = !allFilled;
    }

    // ─── WORD LOOKUP POPUP ─────────────────────────────────
    let currentPopup = null;

    function _renderLookupBody(data) {
        let html = "";
        if (data.frequency != null) {
            html += `<div class="duden-wordtype">Häufigkeit: ${data.frequency.toLocaleString()} (Klasse ${data.frequency_class})</div>`;
        }
        if (data.synonyms && data.synonyms.length) {
            html += `<div class="duden-def"><strong>Synonyme:</strong> ${data.synonyms.join(", ")}</div>`;
        }
        if (data.collocations && data.collocations.length) {
            html += `<div class="duden-def"><strong>Kollokationen:</strong> ${data.collocations.join(", ")}</div>`;
        }
        if (data.examples && data.examples.length) {
            html += `<div class="duden-examples"><strong>Beispiele:</strong><ul>`;
            data.examples.forEach(ex => { html += `<li>${ex}</li>`; });
            html += `</ul></div>`;
        }
        if (!html) {
            html = `<div class="duden-def">Keine Informationen gefunden.</div>`;
        }
        return html;
    }

    function showDudenPopup(word, chipEl) {
        closeDudenPopup();

        const popup = document.createElement("div");
        popup.className = "duden-popup";
        popup.innerHTML = `
            <div class="duden-popup-header">
                <strong>${word}</strong>
                <button class="duden-close-btn" title="Schlie\u00dfen">&times;</button>
            </div>
            <div class="duden-popup-body">
                <div class="duden-loading">Lade...</div>
            </div>
            <div class="duden-popup-actions">
                <button class="btn btn-primary btn-sm duden-save-btn" disabled>Wort speichern</button>
                <a class="btn btn-secondary btn-sm duden-link-btn" href="https://www.openthesaurus.de/synonyme/${encodeURIComponent(word)}" target="_blank" rel="noopener">OpenThesaurus</a>
            </div>
        `;

        document.body.appendChild(popup);
        currentPopup = popup;

        const chipRect = chipEl.getBoundingClientRect();
        const popupHeight = 300;
        let top = chipRect.top - popupHeight - 8;
        if (top < 10) top = chipRect.bottom + 8;
        let left = chipRect.left;
        if (left + 320 > window.innerWidth) left = window.innerWidth - 330;
        if (left < 10) left = 10;
        popup.style.top = top + "px";
        popup.style.left = left + "px";

        popup.querySelector(".duden-close-btn").addEventListener("click", closeDudenPopup);

        let lookupData = null;
        fetch(`/api/duden/${encodeURIComponent(word)}`)
            .then(r => r.json())
            .then(data => {
                lookupData = data;
                popup.querySelector(".duden-popup-body").innerHTML = _renderLookupBody(data);

                const saveBtn = popup.querySelector(".duden-save-btn");
                saveBtn.disabled = false;
                saveBtn.addEventListener("click", () => {
                    saveWordToVocab(lookupData);
                    saveBtn.textContent = "Gespeichert!";
                    saveBtn.disabled = true;
                });
            })
            .catch(() => {
                popup.querySelector(".duden-popup-body").innerHTML =
                    '<div class="duden-def">Fehler beim Laden.</div>';
            });

        setTimeout(() => {
            document.addEventListener("click", onClickOutsidePopup);
        }, 100);
    }

    function closeDudenPopup() {
        if (currentPopup) {
            currentPopup.remove();
            currentPopup = null;
        }
        document.removeEventListener("click", onClickOutsidePopup);
    }

    function onClickOutsidePopup(e) {
        if (currentPopup && !currentPopup.contains(e.target) &&
            !e.target.closest(".word-chip")) {
            closeDudenPopup();
        }
    }

    function saveWordToVocab(lookupData) {
        const sourceSentence = exercise.template_id;
        const defParts = [];
        if (lookupData.synonyms && lookupData.synonyms.length)
            defParts.push("Synonyme: " + lookupData.synonyms.join(", "));
        if (lookupData.collocations && lookupData.collocations.length)
            defParts.push("Kollokationen: " + lookupData.collocations.join(", "));
        if (lookupData.frequency != null)
            defParts.push("Häufigkeit: " + lookupData.frequency.toLocaleString());

        fetch("/api/words", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                word: lookupData.word,
                definition: defParts.join(" · ") || lookupData.definition,
                examples: (lookupData.examples || []).join("\n"),
                source_sentence: sourceSentence
            })
        });
    }

    // ─── CHECK ANSWER ────────────────────────────────────
    async function checkAnswer() {
        const positions = slotElements.map((s, i) => ({
            slot_index: i,
            word: s.querySelector(".placed-word").textContent
        }));

        btnCheck.disabled = true;
        btnCheck.textContent = "Checking...";

        try {
            const resp = await fetch("/api/check", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    template_id: exercise.template_id,
                    positions: positions,
                    retry_id: retryId,
                    module: exercise.module || "verb_position",
                    duration_ms: Date.now() - exerciseStartTime
                })
            });

            const data = await resp.json();
            showResult(data, positions);
        } catch (err) {
            btnCheck.textContent = "Error — try again";
            btnCheck.disabled = false;
        }
    }

    function showResult(data, userPositions) {
        resultArea.classList.remove("hidden");

        const icon = document.getElementById("result-icon");
        const msg = document.getElementById("result-message");
        const correctSentence = document.getElementById("correct-sentence");
        const explanationBox = document.getElementById("explanation-box");
        const errorDetails = document.getElementById("error-details");

        if (data.correct) {
            icon.textContent = "\u2713";
            icon.style.color = "var(--success)";
            msg.textContent = "Richtig! Sehr gut!";
            msg.style.color = "var(--success)";
        } else {
            icon.textContent = "\u2717";
            icon.style.color = "var(--error)";
            msg.textContent = "Nicht ganz richtig.";
            msg.style.color = "var(--error)";
        }

        correctSentence.innerHTML = "<strong>Correct:</strong> " + data.full_sentence;
        explanationBox.innerHTML = "<strong>Rule:</strong> " + data.explanation;

        // Mark slots correct/incorrect
        if (data.slot_results) {
            slotElements.forEach((s, i) => {
                if (data.slot_results[i]) {
                    if (data.slot_results[i].is_correct) {
                        s.classList.add("correct-slot");
                    } else {
                        s.classList.add("incorrect-slot");
                    }
                }
            });
        }

        // Error details (verb-specific)
        errorDetails.innerHTML = "";
        if (data.errors && data.errors.length > 0) {
            data.errors.forEach(err => {
                const card = document.createElement("div");
                card.className = "error-detail-card";
                card.innerHTML = `
                    <div class="error-cat">${err.category_name_en}</div>
                    <div class="error-desc">${err.description}</div>
                    <div class="error-tip">${err.tip}</div>
                    <div class="error-rule">${err.rule}</div>
                `;
                errorDetails.appendChild(card);
            });
        }

        // Word-level feedback when no verb errors explain the mistake
        if (data.word_feedback && !data.correct) {
            const wf = data.word_feedback;
            const card = document.createElement("div");
            card.className = "error-detail-card word-feedback-card";
            card.innerHTML = `<div class="error-cat">${wf.hint}</div>`;
            errorDetails.appendChild(card);

            // Auto-scroll to first wrong slot and flash it
            if (wf.first_wrong_index != null && slotElements[wf.first_wrong_index]) {
                const wrongSlot = slotElements[wf.first_wrong_index];
                wrongSlot.classList.add("flash-wrong");
                wrongSlot.scrollIntoView({ behavior: "smooth", block: "center" });
            }
        }

        resultArea.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    // ─── RESET ───────────────────────────────────────────
    function resetExercise() {
        slotElements.forEach(s => {
            s.querySelector(".placed-word").textContent = "";
            s.classList.remove("filled", "correct-slot", "incorrect-slot");
        });
        chipElements.forEach(c => {
            c.classList.remove("placed", "dragging");
        });
        selectedChip = null;
        resultArea.classList.add("hidden");
        btnCheck.disabled = true;
        btnCheck.textContent = "Pr\u00fcfen";
        closeDudenPopup();
    }

    // ─── START ───────────────────────────────────────────
    init();
})();
