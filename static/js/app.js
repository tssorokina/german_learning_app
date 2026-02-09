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

    // ─── INIT ────────────────────────────────────────────
    function init() {
        clauseType.textContent = exercise.clause_type.replace(/_/g, " ");
        renderSentence();
        renderWords();
        btnCheck.addEventListener("click", checkAnswer);
        btnReset.addEventListener("click", resetExercise);
    }

    function renderSentence() {
        sentenceArea.innerHTML = "";
        slotElements = [];
        const numSlots = exercise.num_slots;
        const suffixes = exercise.slot_suffixes;

        for (let i = 0; i < numSlots; i++) {
            const wrapper = document.createElement("span");
            wrapper.className = "slot-wrapper";

            const el = document.createElement("span");
            el.className = "slot";
            el.dataset.slotIndex = i;
            el.innerHTML = '<span class="placed-word"></span>';
            slotElements.push(el);
            wrapper.appendChild(el);

            // Punctuation OUTSIDE the slot
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
        slotEl.classList.add("filled");
        chip.classList.add("placed");
        updateCheckButton();
    }

    function returnToTray(word, slotEl) {
        const placed = slotEl.querySelector(".placed-word");
        placed.textContent = "";
        slotEl.classList.remove("filled");
        // Find the first chip with this word that is placed and un-place it
        for (const c of chipElements) {
            if (c.dataset.word === word && c.classList.contains("placed")) {
                c.classList.remove("placed");
                break;
            }
        }
        updateCheckButton();
    }

    function updateCheckButton() {
        const allFilled = slotElements.every(s =>
            s.querySelector(".placed-word").textContent !== "");
        btnCheck.disabled = !allFilled;
    }

    // ─── DUDEN POPUP ─────────────────────────────────────
    let currentPopup = null;

    function showDudenPopup(word, chipEl) {
        // Close any existing popup
        closeDudenPopup();

        const popup = document.createElement("div");
        popup.className = "duden-popup";
        popup.innerHTML = `
            <div class="duden-popup-header">
                <strong>${word}</strong>
                <button class="duden-close-btn" title="Schlie\u00dfen">&times;</button>
            </div>
            <div class="duden-popup-body">
                <div class="duden-loading">Lade Definition...</div>
            </div>
            <div class="duden-popup-actions">
                <button class="btn btn-primary btn-sm duden-save-btn" disabled>Wort speichern</button>
                <a class="btn btn-secondary btn-sm duden-link-btn" href="https://www.duden.de/rechtschreibung/${encodeURIComponent(word)}" target="_blank" rel="noopener">Duden.de</a>
            </div>
        `;

        document.body.appendChild(popup);
        currentPopup = popup;

        // Position popup near the chip
        const chipRect = chipEl.getBoundingClientRect();
        const popupHeight = 280;
        let top = chipRect.top - popupHeight - 8;
        if (top < 10) top = chipRect.bottom + 8;
        let left = chipRect.left;
        if (left + 320 > window.innerWidth) left = window.innerWidth - 330;
        if (left < 10) left = 10;
        popup.style.top = top + "px";
        popup.style.left = left + "px";

        // Close button
        popup.querySelector(".duden-close-btn").addEventListener("click", closeDudenPopup);

        // Fetch definition
        let dudenData = null;
        fetch(`/api/duden/${encodeURIComponent(word)}`)
            .then(r => r.json())
            .then(data => {
                dudenData = data;
                const body = popup.querySelector(".duden-popup-body");
                let html = "";
                if (data.word_type) {
                    html += `<div class="duden-wordtype">${data.word_type}</div>`;
                }
                html += `<div class="duden-def">${data.definition}</div>`;
                if (data.examples && data.examples.length > 0) {
                    html += `<div class="duden-examples"><strong>Beispiele:</strong><ul>`;
                    data.examples.forEach(ex => {
                        html += `<li>${ex}</li>`;
                    });
                    html += `</ul></div>`;
                }
                body.innerHTML = html;

                // Enable save button
                const saveBtn = popup.querySelector(".duden-save-btn");
                saveBtn.disabled = false;
                saveBtn.addEventListener("click", () => {
                    saveWordToVocab(dudenData);
                    saveBtn.textContent = "Gespeichert!";
                    saveBtn.disabled = true;
                });
            })
            .catch(() => {
                const body = popup.querySelector(".duden-popup-body");
                body.innerHTML = '<div class="duden-def">Fehler beim Laden. Versuchen Sie es auf duden.de direkt.</div>';
            });

        // Close on clicking outside
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

    function saveWordToVocab(dudenData) {
        const sourceSentence = exercise.template_id;
        fetch("/api/words", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                word: dudenData.word,
                definition: dudenData.definition,
                examples: (dudenData.examples || []).join("\n"),
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
                    module: exercise.module || "verb_position"
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
