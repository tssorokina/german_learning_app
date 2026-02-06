/**
 * Verb-End Torture Chamber — Drag & Drop Exercise Engine
 * Touch-friendly: works on iPhone/Android via pointer events.
 */
(function () {
    "use strict";

    const exercise = EXERCISE_DATA;
    const retryId = RETRY_ID;
    const sentenceArea = document.getElementById("sentence-area");
    const verbTray = document.getElementById("verb-tray");
    const btnCheck = document.getElementById("btn-check");
    const btnReset = document.getElementById("btn-reset");
    const resultArea = document.getElementById("result-area");
    const clauseType = document.getElementById("clause-type");

    // State
    let slotElements = [];
    let chipElements = [];
    let dragState = null; // { chip, ghost, originSlot }

    // ─── INIT ────────────────────────────────────────────
    function init() {
        clauseType.textContent = exercise.clause_type.replace(/_/g, " ");
        renderSentence();
        renderVerbs();
        btnCheck.addEventListener("click", checkAnswer);
        btnReset.addEventListener("click", resetExercise);
    }

    function renderSentence() {
        sentenceArea.innerHTML = "";
        const words = exercise.words;
        const slotIndices = new Set(exercise.slots.map(s => s.index));
        let slotIdx = 0;

        words.forEach((word, i) => {
            if (slotIndices.has(i)) {
                const slot = exercise.slots[slotIdx];
                const el = document.createElement("span");
                el.className = "slot";
                el.dataset.slotIndex = slotIdx;
                el.dataset.wordIndex = i;
                el.dataset.suffix = slot.suffix || "";
                el.innerHTML = '<span class="placed-verb"></span>' + (slot.suffix || "");
                slotElements.push(el);
                sentenceArea.appendChild(el);
                slotIdx++;

                // Drop target listeners
                el.addEventListener("pointerover", onSlotOver);
                el.addEventListener("pointerout", onSlotOut);
                el.addEventListener("click", onSlotClick);
            } else {
                const span = document.createElement("span");
                span.className = "word-token";
                span.textContent = word;
                sentenceArea.appendChild(span);
            }
        });
    }

    function renderVerbs() {
        verbTray.innerHTML = "";
        chipElements = [];
        exercise.verbs.forEach((verb, i) => {
            const chip = document.createElement("span");
            chip.className = "verb-chip";
            chip.textContent = verb;
            chip.dataset.verb = verb;
            chip.dataset.chipIndex = i;

            // Touch + mouse drag
            chip.addEventListener("pointerdown", onChipDown);
            chip.addEventListener("click", onChipClick);
            chipElements.push(chip);
            verbTray.appendChild(chip);
        });
    }

    // ─── CHIP INTERACTION ────────────────────────────────
    let selectedChip = null;

    function onChipClick(e) {
        if (dragState) return; // Ignore during drag
        const chip = e.currentTarget;
        if (chip.classList.contains("placed")) return;

        // Toggle selection
        if (selectedChip === chip) {
            chip.style.outline = "";
            selectedChip = null;
        } else {
            // Deselect previous
            if (selectedChip) selectedChip.style.outline = "";
            chip.style.outline = "2px solid #fff";
            selectedChip = chip;
        }
    }

    function onSlotClick(e) {
        const slot = e.currentTarget;

        // If slot already has a verb, return it to tray
        const placed = slot.querySelector(".placed-verb");
        if (placed && placed.textContent) {
            returnToTray(placed.textContent, slot);
            return;
        }

        // If a chip is selected, place it
        if (selectedChip && !selectedChip.classList.contains("placed")) {
            placeVerb(selectedChip, slot);
            selectedChip.style.outline = "";
            selectedChip = null;
        }
    }

    // ─── DRAG (pointer events) ───────────────────────────
    function onChipDown(e) {
        const chip = e.currentTarget;
        if (chip.classList.contains("placed")) return;

        e.preventDefault();
        chip.setPointerCapture(e.pointerId);

        // Create ghost
        const ghost = document.createElement("div");
        ghost.className = "drag-ghost";
        ghost.textContent = chip.textContent;
        document.body.appendChild(ghost);
        ghost.style.left = e.clientX + "px";
        ghost.style.top = e.clientY + "px";

        chip.classList.add("dragging");

        dragState = { chip, ghost, originSlot: null };

        const onMove = (ev) => {
            if (!dragState) return;
            ghost.style.left = ev.clientX + "px";
            ghost.style.top = ev.clientY + "px";

            // Highlight slot under pointer
            const target = document.elementFromPoint(ev.clientX, ev.clientY);
            slotElements.forEach(s => s.classList.remove("drag-over"));
            if (target && target.closest(".slot")) {
                target.closest(".slot").classList.add("drag-over");
            }
        };

        const onUp = (ev) => {
            if (!dragState) return;
            chip.classList.remove("dragging");
            ghost.remove();

            // Find slot under pointer
            // Need to temporarily hide ghost to get element below
            const target = document.elementFromPoint(ev.clientX, ev.clientY);
            const slotEl = target ? target.closest(".slot") : null;

            slotElements.forEach(s => s.classList.remove("drag-over"));

            if (slotEl) {
                const existing = slotEl.querySelector(".placed-verb");
                if (existing && existing.textContent) {
                    returnToTray(existing.textContent, slotEl);
                }
                placeVerb(chip, slotEl);
            }

            dragState = null;
            chip.removeEventListener("pointermove", onMove);
            chip.removeEventListener("pointerup", onUp);
            chip.removeEventListener("pointercancel", onUp);
        };

        chip.addEventListener("pointermove", onMove);
        chip.addEventListener("pointerup", onUp);
        chip.addEventListener("pointercancel", onUp);
    }

    function onSlotOver(e) {
        if (dragState) e.currentTarget.classList.add("drag-over");
    }
    function onSlotOut(e) {
        e.currentTarget.classList.remove("drag-over");
    }

    // ─── PLACE / RETURN ──────────────────────────────────
    function placeVerb(chip, slotEl) {
        const placed = slotEl.querySelector(".placed-verb");
        placed.textContent = chip.dataset.verb;
        slotEl.classList.add("filled");
        chip.classList.add("placed");
        updateCheckButton();
    }

    function returnToTray(verb, slotEl) {
        const placed = slotEl.querySelector(".placed-verb");
        placed.textContent = "";
        slotEl.classList.remove("filled");
        // Find the chip and un-place it
        chipElements.forEach(c => {
            if (c.dataset.verb === verb && c.classList.contains("placed")) {
                c.classList.remove("placed");
            }
        });
        updateCheckButton();
    }

    function updateCheckButton() {
        const allFilled = slotElements.every(s =>
            s.querySelector(".placed-verb").textContent !== "");
        btnCheck.disabled = !allFilled;
    }

    // ─── CHECK ANSWER ────────────────────────────────────
    async function checkAnswer() {
        const positions = slotElements.map((s, i) => ({
            slot_index: i,
            verb: s.querySelector(".placed-verb").textContent
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
                    retry_id: retryId
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
        // Hide check/reset, show result
        resultArea.classList.remove("hidden");

        const icon = document.getElementById("result-icon");
        const msg = document.getElementById("result-message");
        const correctSentence = document.getElementById("correct-sentence");
        const explanationBox = document.getElementById("explanation-box");
        const errorDetails = document.getElementById("error-details");

        if (data.correct) {
            icon.textContent = "✓";
            icon.style.color = "var(--success)";
            msg.textContent = "Richtig! Sehr gut!";
            msg.style.color = "var(--success)";
        } else {
            icon.textContent = "✗";
            icon.style.color = "var(--error)";
            msg.textContent = "Nicht ganz richtig.";
            msg.style.color = "var(--error)";
        }

        correctSentence.innerHTML = "<strong>Correct:</strong> " + data.full_sentence;
        explanationBox.innerHTML = "<strong>Rule:</strong> " + data.explanation;

        // Mark slots correct/incorrect
        if (data.slots) {
            slotElements.forEach((s, i) => {
                const placed = s.querySelector(".placed-verb").textContent;
                if (data.slots[i] && placed === data.slots[i].correct_verb) {
                    s.classList.add("correct-slot");
                } else {
                    s.classList.add("incorrect-slot");
                }
            });
        }

        // Error details
        errorDetails.innerHTML = "";
        if (data.errors && data.errors.length > 0) {
            data.errors.forEach(err => {
                const card = document.createElement("div");
                card.className = "error-detail-card";
                card.innerHTML = `
                    <div class="error-cat">${err.category_name_en}</div>
                    <div class="error-desc">${err.description}</div>
                    <div class="error-tip">💡 ${err.tip}</div>
                    <div class="error-rule">${err.rule}</div>
                `;
                errorDetails.appendChild(card);
            });
        }

        // Scroll result into view
        resultArea.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    // ─── RESET ───────────────────────────────────────────
    function resetExercise() {
        slotElements.forEach(s => {
            s.querySelector(".placed-verb").textContent = "";
            s.classList.remove("filled", "correct-slot", "incorrect-slot");
        });
        chipElements.forEach(c => {
            c.classList.remove("placed", "dragging");
            c.style.outline = "";
        });
        selectedChip = null;
        resultArea.classList.add("hidden");
        btnCheck.disabled = true;
        btnCheck.textContent = "Prüfen";
    }

    // ─── START ───────────────────────────────────────────
    init();
})();
