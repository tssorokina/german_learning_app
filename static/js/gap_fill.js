/**
 * Gap-Fill Exercise Engine — for adjective declension & Konjunktiv gap exercises.
 * Shows a sentence with gaps, user selects endings/words from small tap-buttons.
 */
(function () {
    "use strict";

    const exercise = EXERCISE_DATA;
    const sentenceDisplay = document.getElementById("sentence-display");
    const btnCheck = document.getElementById("btn-check");
    const btnReset = document.getElementById("btn-reset");
    const resultArea = document.getElementById("result-area");
    const grammarHint = document.getElementById("grammar-hint");

    // State: selected answer for each gap
    let gapSelections = {};

    function init() {
        if (exercise.grammar_tip) {
            grammarHint.textContent = exercise.grammar_tip;
        }
        renderSentence();
        btnCheck.addEventListener("click", checkAnswer);
        btnReset.addEventListener("click", resetExercise);
    }

    function renderSentence() {
        sentenceDisplay.innerHTML = "";
        // Parse the template: split on {gap_N} patterns
        const template = exercise.sentence_template;
        const parts = template.split(/(\{gap_\d+\})/);

        parts.forEach(function (part) {
            const gapMatch = part.match(/^\{(gap_\d+)\}$/);
            if (gapMatch) {
                const gapId = gapMatch[1];
                const gapData = exercise.gaps.find(function (g) { return g.position === gapId; });
                if (gapData) {
                    // Create gap container
                    var gapContainer = document.createElement("span");
                    gapContainer.className = "gap-container";
                    gapContainer.dataset.gap = gapId;

                    // Show context if available
                    if (gapData.context) {
                        var ctx = document.createElement("span");
                        ctx.className = "gap-context";
                        ctx.textContent = gapData.context;
                        gapContainer.appendChild(ctx);
                    }

                    // Show hint for Konjunktiv exercises
                    if (gapData.indicative_hint) {
                        var hint = document.createElement("div");
                        hint.className = "gap-hint";
                        hint.textContent = gapData.indicative_hint;
                        gapContainer.appendChild(hint);
                    }

                    // Create option buttons
                    var optionsRow = document.createElement("div");
                    optionsRow.className = "gap-options";
                    gapData.options.forEach(function (opt) {
                        var btn = document.createElement("button");
                        btn.className = "gap-option-btn";
                        btn.textContent = opt.length <= 3 ? "-" + opt : opt;
                        btn.dataset.gap = gapId;
                        btn.dataset.value = opt;
                        btn.addEventListener("click", function () { selectOption(gapId, opt, btn); });
                        optionsRow.appendChild(btn);
                    });
                    gapContainer.appendChild(optionsRow);

                    sentenceDisplay.appendChild(gapContainer);
                }
            } else if (part) {
                var textNode = document.createElement("span");
                textNode.className = "gap-text";
                textNode.textContent = part;
                sentenceDisplay.appendChild(textNode);
            }
        });
    }

    function selectOption(gapId, value, btn) {
        // Deselect previous selection for this gap
        var allBtns = sentenceDisplay.querySelectorAll('.gap-option-btn[data-gap="' + gapId + '"]');
        allBtns.forEach(function (b) { b.classList.remove("selected"); });

        // Select this one
        btn.classList.add("selected");
        gapSelections[gapId] = value;

        updateCheckButton();
    }

    function updateCheckButton() {
        var allFilled = exercise.gaps.every(function (g) { return gapSelections[g.position]; });
        btnCheck.disabled = !allFilled;
    }

    async function checkAnswer() {
        btnCheck.disabled = true;
        btnCheck.textContent = "Checking...";

        try {
            var resp = await fetch("/api/check_gap", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    exercise_id: exercise.exercise_id,
                    answers: gapSelections
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

        // Mark gaps correct/incorrect
        if (data.gap_results) {
            data.gap_results.forEach(function (gr) {
                var container = sentenceDisplay.querySelector('.gap-container[data-gap="' + gr.position + '"]');
                if (container) {
                    if (gr.is_correct) {
                        container.classList.add("gap-correct");
                    } else {
                        container.classList.add("gap-incorrect");
                        // Show correct answer
                        var correction = document.createElement("span");
                        correction.className = "gap-correction";
                        correction.textContent = " \u2192 -" + gr.correct_answer;
                        container.appendChild(correction);
                    }
                }
            });
        }

        // Error details
        errorDetails.innerHTML = "";
        if (data.errors && data.errors.length > 0) {
            data.errors.forEach(function (err) {
                var card = document.createElement("div");
                card.className = "error-detail-card";
                card.innerHTML =
                    '<div class="error-cat">' + err.category_name_en + '</div>' +
                    '<div class="error-desc">' + err.description + '</div>' +
                    '<div class="error-tip">' + err.tip + '</div>' +
                    '<div class="error-rule">' + err.rule + '</div>';
                errorDetails.appendChild(card);
            });
        }

        resultArea.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    function resetExercise() {
        gapSelections = {};
        var allBtns = sentenceDisplay.querySelectorAll(".gap-option-btn");
        allBtns.forEach(function (b) { b.classList.remove("selected"); });
        var containers = sentenceDisplay.querySelectorAll(".gap-container");
        containers.forEach(function (c) {
            c.classList.remove("gap-correct", "gap-incorrect");
            var correction = c.querySelector(".gap-correction");
            if (correction) correction.remove();
        });
        resultArea.classList.add("hidden");
        btnCheck.disabled = true;
        btnCheck.textContent = "Pr\u00fcfen";
    }

    init();
})();
