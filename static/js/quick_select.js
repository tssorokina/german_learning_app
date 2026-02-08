/**
 * Quick-Select Exercise Engine — for prepositions & cases.
 * Shows a sentence with inline dropdowns/buttons for each gap.
 */
(function () {
    "use strict";

    const exercise = EXERCISE_DATA;
    const sentenceDisplay = document.getElementById("sentence-display");
    const btnCheck = document.getElementById("btn-check");
    const btnReset = document.getElementById("btn-reset");
    const resultArea = document.getElementById("result-area");
    const grammarHint = document.getElementById("grammar-hint");

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
        var template = exercise.sentence;
        var parts = template.split(/(\{gap_\d+\})/);

        parts.forEach(function (part) {
            var gapMatch = part.match(/^\{(gap_\d+)\}$/);
            if (gapMatch) {
                var gapId = gapMatch[1];
                var gapData = exercise.gaps.find(function (g) { return g.position === gapId; });
                if (gapData) {
                    var gapContainer = document.createElement("span");
                    gapContainer.className = "qs-gap-container";
                    gapContainer.dataset.gap = gapId;

                    // Create inline option buttons
                    gapData.options.forEach(function (opt) {
                        var btn = document.createElement("button");
                        btn.className = "qs-option-btn";
                        btn.textContent = opt;
                        btn.dataset.gap = gapId;
                        btn.dataset.value = opt;
                        btn.addEventListener("click", function () { selectOption(gapId, opt, btn); });
                        gapContainer.appendChild(btn);
                    });

                    sentenceDisplay.appendChild(gapContainer);
                }
            } else if (part) {
                var textNode = document.createElement("span");
                textNode.className = "qs-text";
                textNode.textContent = part;
                sentenceDisplay.appendChild(textNode);
            }
        });
    }

    function selectOption(gapId, value, btn) {
        var allBtns = sentenceDisplay.querySelectorAll('.qs-option-btn[data-gap="' + gapId + '"]');
        allBtns.forEach(function (b) { b.classList.remove("selected"); });
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
            var resp = await fetch("/api/check_quick_select", {
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
                var container = sentenceDisplay.querySelector('.qs-gap-container[data-gap="' + gr.position + '"]');
                if (container) {
                    if (gr.is_correct) {
                        container.classList.add("qs-correct");
                    } else {
                        container.classList.add("qs-incorrect");
                        // Show correct answer and explanation
                        var correction = document.createElement("div");
                        correction.className = "qs-correction";
                        correction.textContent = "\u2192 " + gr.correct_answer;
                        if (gr.explanation) {
                            correction.textContent += " (" + gr.explanation + ")";
                        }
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
        var allBtns = sentenceDisplay.querySelectorAll(".qs-option-btn");
        allBtns.forEach(function (b) { b.classList.remove("selected"); });
        var containers = sentenceDisplay.querySelectorAll(".qs-gap-container");
        containers.forEach(function (c) {
            c.classList.remove("qs-correct", "qs-incorrect");
            var correction = c.querySelector(".qs-correction");
            if (correction) correction.remove();
        });
        resultArea.classList.add("hidden");
        btnCheck.disabled = true;
        btnCheck.textContent = "Pr\u00fcfen";
    }

    init();
})();
