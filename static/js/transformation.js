/**
 * Transformation Exercise Engine — for passive voice & nominalization.
 * Shows a source sentence, user reconstructs the target from scrambled words.
 * Reuses the tap/drag mechanic from the main app.js.
 */
(function () {
    "use strict";

    const exercise = EXERCISE_DATA;
    const sourceDisplay = document.getElementById("source-sentence");
    const sentenceArea = document.getElementById("sentence-area");
    const wordTray = document.getElementById("word-tray");
    const btnCheck = document.getElementById("btn-check");
    const btnReset = document.getElementById("btn-reset");
    const resultArea = document.getElementById("result-area");

    let slotElements = [];
    let chipElements = [];
    let dragState = null;

    function init() {
        // Show source sentence
        sourceDisplay.innerHTML = '<div class="source-label">Transform this:</div>' +
            '<div class="source-text">' + exercise.source + '</div>';

        renderSlots();
        renderWords();
        btnCheck.addEventListener("click", checkAnswer);
        btnReset.addEventListener("click", resetExercise);
    }

    function renderSlots() {
        sentenceArea.innerHTML = "";
        slotElements = [];
        for (var i = 0; i < exercise.num_slots; i++) {
            var el = document.createElement("span");
            el.className = "slot";
            el.dataset.slotIndex = i;
            el.innerHTML = '<span class="placed-word"></span>';
            slotElements.push(el);

            el.addEventListener("click", onSlotClick);
            sentenceArea.appendChild(el);
        }
    }

    function renderWords() {
        wordTray.innerHTML = "";
        chipElements = [];
        exercise.shuffled_words.forEach(function (word, i) {
            var chip = document.createElement("span");
            chip.className = "word-chip";
            // Dim optional words
            if (exercise.optional_words && exercise.optional_words.indexOf(word) !== -1) {
                chip.classList.add("optional-word");
            }
            chip.textContent = word;
            chip.dataset.word = word;
            chip.dataset.chipIndex = i;

            chip.addEventListener("pointerdown", onChipDown);
            chip.addEventListener("click", onChipClick);

            chipElements.push(chip);
            wordTray.appendChild(chip);
        });
    }

    // ─── TAP TO PLACE ────────────────────────────────
    function onChipClick(e) {
        if (dragState) return;
        var chip = e.currentTarget;
        if (chip.classList.contains("placed")) return;
        var nextSlot = slotElements.find(function (s) {
            return s.querySelector(".placed-word").textContent === "";
        });
        if (nextSlot) placeWord(chip, nextSlot);
    }

    function onSlotClick(e) {
        var slot = e.currentTarget;
        var placed = slot.querySelector(".placed-word");
        if (placed && placed.textContent) {
            returnToTray(placed.textContent, slot);
        }
    }

    // ─── DRAG ────────────────────────────────────────
    function onChipDown(e) {
        var chip = e.currentTarget;
        if (chip.classList.contains("placed")) return;
        e.preventDefault();

        var startX = e.clientX, startY = e.clientY;
        var isDragging = false;

        chip.setPointerCapture(e.pointerId);

        var onMove = function (ev) {
            var dx = Math.abs(ev.clientX - startX);
            var dy = Math.abs(ev.clientY - startY);
            if (!isDragging && (dx > 5 || dy > 5)) {
                isDragging = true;
                startDrag(chip, ev);
            }
            if (isDragging && dragState) {
                dragState.ghost.style.left = ev.clientX + "px";
                dragState.ghost.style.top = ev.clientY + "px";
                var target = document.elementFromPoint(ev.clientX, ev.clientY);
                slotElements.forEach(function (s) { s.classList.remove("drag-over"); });
                if (target && target.closest(".slot")) {
                    target.closest(".slot").classList.add("drag-over");
                }
            }
        };

        var onUp = function (ev) {
            if (isDragging && dragState) {
                chip.classList.remove("dragging");
                dragState.ghost.remove();
                var target = document.elementFromPoint(ev.clientX, ev.clientY);
                var slotEl = target ? target.closest(".slot") : null;
                slotElements.forEach(function (s) { s.classList.remove("drag-over"); });
                if (slotEl) {
                    var existing = slotEl.querySelector(".placed-word");
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
        var ghost = document.createElement("div");
        ghost.className = "drag-ghost";
        ghost.textContent = chip.textContent;
        document.body.appendChild(ghost);
        ghost.style.left = ev.clientX + "px";
        ghost.style.top = ev.clientY + "px";
        chip.classList.add("dragging");
        dragState = { chip: chip, ghost: ghost };
    }

    function placeWord(chip, slotEl) {
        var placed = slotEl.querySelector(".placed-word");
        placed.textContent = chip.dataset.word;
        slotEl.classList.add("filled");
        chip.classList.add("placed");
        updateCheckButton();
    }

    function returnToTray(word, slotEl) {
        var placed = slotEl.querySelector(".placed-word");
        placed.textContent = "";
        slotEl.classList.remove("filled");
        for (var i = 0; i < chipElements.length; i++) {
            if (chipElements[i].dataset.word === word && chipElements[i].classList.contains("placed")) {
                chipElements[i].classList.remove("placed");
                break;
            }
        }
        updateCheckButton();
    }

    function updateCheckButton() {
        var allFilled = slotElements.every(function (s) {
            return s.querySelector(".placed-word").textContent !== "";
        });
        btnCheck.disabled = !allFilled;
    }

    // ─── CHECK ANSWER ────────────────────────────────
    async function checkAnswer() {
        var positions = slotElements.map(function (s, i) {
            return {
                slot_index: i,
                word: s.querySelector(".placed-word").textContent
            };
        });

        btnCheck.disabled = true;
        btnCheck.textContent = "Checking...";

        try {
            var resp = await fetch("/api/check_transformation", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    exercise_id: exercise.exercise_id,
                    positions: positions
                })
            });

            var data = await resp.json();
            showResult(data);
        } catch (err) {
            btnCheck.textContent = "Error — try again";
            btnCheck.disabled = false;
        }
    }

    function showResult(data) {
        resultArea.classList.remove("hidden");

        var icon = document.getElementById("result-icon");
        var msg = document.getElementById("result-message");
        var correctSentence = document.getElementById("correct-sentence");
        var explanationBox = document.getElementById("explanation-box");
        var errorDetails = document.getElementById("error-details");

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
        explanationBox.innerHTML = "<strong>Rule:</strong> " + data.grammar_rule;
        if (data.grammar_tip) {
            explanationBox.innerHTML += "<br><strong>Tip:</strong> " + data.grammar_tip;
        }

        // Mark slots correct/incorrect
        if (data.slot_results) {
            slotElements.forEach(function (s, i) {
                if (data.slot_results[i]) {
                    s.classList.add(data.slot_results[i].is_correct ? "correct-slot" : "incorrect-slot");
                }
            });
        }

        errorDetails.innerHTML = "";
        resultArea.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    function resetExercise() {
        slotElements.forEach(function (s) {
            s.querySelector(".placed-word").textContent = "";
            s.classList.remove("filled", "correct-slot", "incorrect-slot");
        });
        chipElements.forEach(function (c) {
            c.classList.remove("placed", "dragging");
        });
        resultArea.classList.add("hidden");
        btnCheck.disabled = true;
        btnCheck.textContent = "Pr\u00fcfen";
    }

    init();
})();
