/**
 * Input Lab — Bridge Drill Engine
 * Full-sentence reconstruction from reading text sentences.
 * Adapted from app.js with Lab-specific check endpoint.
 */
(function () {
    "use strict";

    var exercise = EXERCISE_DATA;
    var drillMeta = LAB_DRILL;
    var sentenceArea = document.getElementById("sentence-area");
    var wordTray = document.getElementById("word-tray");
    var btnCheck = document.getElementById("btn-check");
    var btnReset = document.getElementById("btn-reset");
    var resultArea = document.getElementById("result-area");

    var slotElements = [];
    var chipElements = [];
    var dragState = null;

    function init() {
        renderSentence();
        renderWords();
        btnCheck.addEventListener("click", checkAnswer);
        btnReset.addEventListener("click", resetExercise);
    }

    function renderSentence() {
        sentenceArea.innerHTML = "";
        slotElements = [];
        for (var i = 0; i < exercise.num_slots; i++) {
            var wrapper = document.createElement("span");
            wrapper.className = "slot-wrapper";

            var el = document.createElement("span");
            el.className = "slot";
            el.dataset.slotIndex = i;
            el.innerHTML = '<span class="placed-word"></span>';
            slotElements.push(el);
            wrapper.appendChild(el);

            if (exercise.slot_suffixes[i]) {
                var punct = document.createElement("span");
                punct.className = "slot-punct";
                punct.textContent = exercise.slot_suffixes[i];
                wrapper.appendChild(punct);
            }

            sentenceArea.appendChild(wrapper);

            el.addEventListener("click", onSlotClick);
        }
    }

    function renderWords() {
        wordTray.innerHTML = "";
        chipElements = [];
        exercise.shuffled_words.forEach(function (word, i) {
            var chip = document.createElement("span");
            chip.className = "word-chip";
            chip.textContent = word;
            chip.dataset.word = word;
            chip.dataset.chipIndex = i;
            chip.addEventListener("click", onChipClick);
            chipElements.push(chip);
            wordTray.appendChild(chip);
        });
    }

    function onChipClick(e) {
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

    function placeWord(chip, slotEl) {
        slotEl.querySelector(".placed-word").textContent = chip.dataset.word;
        slotEl.classList.add("filled");
        chip.classList.add("placed");
        updateCheckButton();
    }

    function returnToTray(word, slotEl) {
        slotEl.querySelector(".placed-word").textContent = "";
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

    function checkAnswer() {
        var positions = slotElements.map(function (s, i) {
            return { slot_index: i, word: s.querySelector(".placed-word").textContent };
        });

        btnCheck.disabled = true;
        btnCheck.textContent = "Checking...";

        fetch("/api/lab/drill/check", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                segment_id: drillMeta.segment_id,
                text_id: drillMeta.text_id,
                positions: positions,
                template_id: exercise.template_id
            })
        })
            .then(function (r) { return r.json(); })
            .then(function (data) { showResult(data); })
            .catch(function () {
                btnCheck.textContent = "Error — try again";
                btnCheck.disabled = false;
            });
    }

    function showResult(data) {
        resultArea.classList.remove("hidden");

        var icon = document.getElementById("result-icon");
        var msg = document.getElementById("result-message");
        var correctSentence = document.getElementById("correct-sentence");
        var explanationBox = document.getElementById("explanation-box");

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
        if (data.explanation) {
            explanationBox.innerHTML = "<strong>Note:</strong> " + data.explanation;
        }

        if (data.slot_results) {
            slotElements.forEach(function (s, i) {
                if (data.slot_results[i]) {
                    s.classList.add(data.slot_results[i].is_correct ? "correct-slot" : "incorrect-slot");
                }
            });
        }

        resultArea.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    function resetExercise() {
        slotElements.forEach(function (s) {
            s.querySelector(".placed-word").textContent = "";
            s.classList.remove("filled", "correct-slot", "incorrect-slot");
        });
        chipElements.forEach(function (c) {
            c.classList.remove("placed");
        });
        resultArea.classList.add("hidden");
        btnCheck.disabled = true;
        btnCheck.textContent = "Pr\u00fcfen";
    }

    init();
})();
