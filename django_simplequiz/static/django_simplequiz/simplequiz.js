(function($) {
  "use strict";

  $.fn.quiz = function(opts) {

    var node = this,
        nodeScore = node.find('.score .current'),
        nodeTimer = node.find('.timer .time'),
        nodeAnswer = node.find('input.answer'),
        nodeAnswers = node.find('.answers'),

        nodeStart = node.find('.start'),
        nodePause = node.find('.pause'),
        nodeGiveup = node.find('.give-up'),
        nodeRestart = node.find('.restart'),
        nodeNext = node.find('.next'),
        nodePrev = node.find('.prev'),
        nodeQuestion = node.find('.question'),
        nodeOverlay = node.find('.overlay'),
        nodeOverlayInner = nodeOverlay.find('.inner'),
        nodeInfo = node.find('.quiz-info-wrap'),
        nodeMistakes = node.find('.mistakes'),

        nodeResults = node.find('.results'),

        options = opts || {},
        store = {},
        settings = null,

        answers = [],

        started = null,
        finished = null,
        last_tick = null,
        time_taken = 0,
        score = 0,
        wrong_answers = 0,
        maxScore = null,

        // Index of currently active question.
        // Only needed for force_order or one_by_one.
        current_question_index = null,


        timerHandle = null;

    // Retrieve settings store.
    if (node.find('.data')) {
      store = JSON.parse(node.find('.data').html());
      if (typeof(store) !== 'object' || !('id' in store)) {
        throw new Error("Invalid datastore!");
      }
    }

    settings = $.extend(store, options);

    function buildAnswerMap() {
      var map = {};

      for (var key in settings.questions) {
        var question = settings.questions[key];

        var answer = question.answer;
        if (settings.ignore_case) {
          answer = answer.toLowerCase();
        }
        if (settings.ignore_spaces) {
          answer = answer.replace(' ', '');
        }

        var answers = answer.split('|');

        for (var i = 0; i < answers.length; i++) {
          map[answers[i]] = question;
        }
      }

      return map;
    }

    function isPaged() {
      return settings.one_by_one || settings.force_order || settings.mode === "click";
    }


    function start() {
      answers = buildAnswerMap();
      maxScore = settings.questions.length;

      started = last_tick = new Date();

      updateTimerLabel();
      initTimer();

      nodePause.removeClass('disabled');
      nodeGiveup.removeClass('disabled');
      nodeAnswer.attr('disabled', null);

      // Handle "paged" quizzes which enforce a question order.
      if (isPaged()) {
        if (settings.allow_paging) {
          nodeNext.removeClass('disabled');
          nodePrev.removeClass('disabled');
        }

        nextQuestion();
      }



      // Remove start button.
      nodeStart.fadeOut(function() {
        nodeStart.remove();
      });


    }

    function restart() {
      if (!(started && finished)) {
        return;
      }

      finished = null;
      score = 0;
      time_taken = 0;
      current_question_index = null;

      nodeAnswer.val('');
      nodeScore.html('0');

      nodeRestart.addClass('disabled');

      nodeInfo.slideUp()

      // Reset questions and answer items.
      for (var i = 0; i < settings.questions.length; i++) {
        var question = settings.questions[i];

        delete question.answered;

        var row = nodeAnswers.find('.question-' + question.id);
        row.removeClass('answered').removeClass('wrong');
        row.find('.answer').html('');
        row.find('.info').html('');
      }

      start();
    }


    function showQuestion(index) {
      var question = settings.questions[index];

      // For one_by_one or clicking, the question is shown in the question div.
      // Otherwise, the row in the table is highlighted.
      if (settings.one_by_one || settings.mode === 'click') {
        nodeQuestion.html(question.name);
      }
      else {
        nodeAnswers.find('.question-item').removeClass('active');
        nodeAnswers.find('.question-' + question.id).addClass('active');
      }

      current_question_index = index;
    }

    function nextQuestion() {
      if (!isRunning()) {
        return;
      }

      var next = null;

      // Find the next question that is yet unanswered.
      var index = (current_question_index === null) ? -1 : current_question_index;
      while (!next) {
        index += 1;
        if (index >= settings.questions.length) {
          index = 0;
        }

        if (!('answered' in settings.questions[index])) {
          next = settings.questions[index];
        }
      }

      showQuestion(index);
    }

    function prevQuestion() {
      if (!isRunning()) {
        return;
      }

      var prev = null;

      var index = current_question_index;
      while (!prev) {
        index -= 1;

        if (index < 0) {
          index = settings.questions.length - 1;
        }

        if (!('answered' in settings.questions[index])) {
          prev = settings.questions[index];
        }
      }

      showQuestion(index);
    }

    function onTick() {
      var now = new Date();
      time_taken += now - last_tick;

      if (time_taken / 1000 >= settings.time) {
        finish();
        return;
      }

      last_tick = now;

      // Update timer.
      updateTimerLabel();
    }


    function renderTime(seconds) {
      var min = Math.floor(seconds / 60);
      var sec = seconds % 60;

      var text = (min > 10 ? min : '0' + min) + ':' + (sec > 10 ? sec : '0' + sec);

      return text;
    }

    function updateTimerLabel() {
      var remaining = settings.time - Math.floor(time_taken / 1000);
      
      var label = renderTime(remaining);
      nodeTimer.html(label);
    }

    function updateScore(score) {
      nodeScore.html(score);
    }

    function initTimer() {
      timerHandle = setInterval(function () {
        onTick();
      }, 1000);
    }

    function isRunning() {
      return started && timerHandle && !finished;
    }

    function isPaused() {
      return started && !timerHandle;
    }

    function pause() {
      clearInterval(timerHandle);
      timerHandle = null;

      node.addClass('paused');
      nodeAnswer.attr('disabled', 'disabled');
      nodePause.html(settings.label_resume);

      nodeNext.addClass('disabled');
      nodePrev.addClass('disabled');
    }

    function resume() {
      last_tick = new Date();
      initTimer();

      node.removeClass('paused');
      nodeAnswer.attr('disabled', null);
      nodePause.html(settings.label_pause);

      nodeNext.removeClass('disabled');
      nodePrev.removeClass('disabled');
    }


    function finish() {
      if (!started) {
        return;
      }

      finished = new Date();

      clearInterval(timerHandle);

      var success = score === maxScore;

      if ((success || settings.show_answers_on_finish) && settings.info) {
        nodeInfo.slideDown();
      }

      for (var i = 0; i < settings.questions.length; i++) {
        var question = settings.questions[i];
        if (!('answered' in question)) {
          showAnswerRow(question, false);
        }
      }

      // onFinished() will be called by onAttemptSaved().
      saveAttempt();
    }

    /**
     * The things done by this function should only happen
     * after the attempt has been saved for authenticated users.
     *
     * The code is in it's own function to allow the ajax callback to 
     * call it from onAttemptSaved().
     */
    function onFinished() {
      nodePause.addClass('disabled');
      nodeGiveup.addClass('disabled');
      nodeAnswer.attr('disabled', 'disabled');

      nodeRestart.removeClass('disabled');
    }


    function saveAttempt() {

      // Show loading overlay.
      nodeOverlay.css('z-index', 10).show();
      nodeOverlay.find('.preloader').show();
      nodeOverlay.find('.results').hide();


      var data = {
        csrfmiddlewaretoken: settings.csrf,
        id: settings.id,
        started_at: started.toISOString(),
        finished_at: finished.toISOString(),
        time_taken: time_taken / 1000,
        score: score / maxScore,
        mistakes: wrong_answers
      };

      $.ajax({
        type: 'POST',
        url: settings.save_attempt_url,
        data: data,
        success: function(data) {
          nodeOverlay.find('.preloader').hide();
          nodeOverlay.find('.results').show();

          nodeOverlay.find('.score').html(data.score * 100 + '%');
          nodeOverlay.find('.mistakes').html(wrong_answers);
          nodeOverlay.find('.time').html(renderTime(Math.floor(time_taken / 1000)));
          nodeOverlay.find('.position').html(data.pos + ' / ' + data.attempts);

          if (data.personal_pos) {
            nodeOverlay.find('.personal-position').html(data.personal_pos + ' / ' + data.personal_attempts);
          }
          else {
            nodeOverlay.find('.register-info').show();
          }

          nodeOverlay.find('.closer').unbind('click').click(function() {
            nodeOverlay.fadeOut(function() {
              nodeOverlay.css('z-index', -10);

              onFinished();
            });
          });
        },
        error: function(xhr) {
          onFinished();
        }
      });

    }


    function onType(enter) {
      if (!started || isPaused()) {
        return;
      }

      var val = nodeAnswer.val();

      var valid = onAnswer(null, val, !enter);

      if (valid) {
        nodeAnswer.val('');

        // Flash the input box green.
        nodeAnswer.addClass('success');
        setTimeout(function() {
          nodeAnswer.removeClass('success');
        }, 300);
      }
      else {
        if (enter) {
          // Flash the input box red.
          nodeAnswer.addClass('fail');
          setTimeout(function() {
            nodeAnswer.removeClass('fail');
          }, 300);
        }
      }
    }

    function onClicked(item) {
      if (!started || isPaused()) {
        return;
      }

      var answer_id = parseInt(item.attr('data-id'));

      var valid = onAnswer(answer_id);

      if (valid) {
        item.addClass('success');
      }
      else {
        item.addClass('wrong');

        if (valid !== -1) {
          // Invalid, but quiz continues,
          // so just flash the answer red.
          setTimeout(function() {
            item.removeClass('wrong');
          }, 200);
        }

      }
    }

    function showAnswerRow(question, success) {
      var row = nodeAnswers.find('.question-' + question.id);
      if (question.name) {
        row.find('.name').html(question.name);
      }

      if (success || settings.show_answers_on_finish) {
        if (question.info) {
          row.find('.info').html(question.info);
        }
        row.find('.answer').html(question.answer.split('|')[0]);
      }

      row.addClass(success ? 'answered' : 'wrong');
    }

    function getCurrentQuestion() {
      if (current_question_index === null) {
        return null;
      }
      else {
        return settings.questions[current_question_index];
      }
    }

    function getQuestionById(id) {
      for (var i = 0; i < settings.questions.length; i++) {
        if (settings.questions[i].id === id) {
          return settings.questions[i];
        }
      }

      return null;
    }

    /**
     * Process an answer that was given.
     * 
     * @param  {[type]} answer_id      [description]
     * @param  {[type]} value          [description]
     * @param  {[type]} no_wrong_count [description]
     * @return 
     *   true for valid answer, false for invalid answer
     *   1 for valid answer if quiz finishes!
     *   -1 for invalid answer if quiz finishes!
     */
    function onAnswer(answer_id, value, no_wrong_count) {
      if (isPaused()) {
        return;
      }

      // If a value was given, try to retrieve
      // the a answer_id based on the value.
      if (typeof(value) === 'string') {
        if (settings.ignore_case) {
          value = value.toLowerCase();
        }
        if (settings.ignore_spaces) {
          value = value.replace(/\s+/g, '');
        }

        if (value in answers) {
          answer_id = answers[value].id;
        }
      }

      // Validate the answer.
      var valid = false;
      var question = null;

      if (answer_id === null) {
        // Answer was typed, and the typed answer does not fit
        // any of the question answers, so the answer is invalid.
        valid = false;
      }
      else if (current_question_index !== null) {
        // Either the quiz is in MODE_CLICK or one_by_one is enabled,
        // so there is only one active question.
        // Answer is valid if it is the answer for the current question.

        question = getCurrentQuestion();

        if (question.id === answer_id) {
          valid = true;
        }
      }
      else {
        // Answer was typed and does match an existing question answer.
        // Answer is valid if it answers a yet unanswered question.
        question = getQuestionById(answer_id);

        if (!('answered' in question)) {
          // Question not answered yet, and answer is correct, so answer is valid. 
          valid = true;
        }
      }

      if (valid) {
        // Valid, so update interface and data accordingly.
        question.answered = true;
        showAnswerRow(question, true);

        score += 1;
        updateScore(score);

        if (score === maxScore) {
          // All answeres were answered correctly, so finish.
          finish();
          valid = 1;
        }
        else {
          if (isPaged()) {
            // Show next question for paged quizzes.
            nextQuestion()
          }
        }
      }
      else {
        // Invalid.
        if (!no_wrong_count) {
          wrong_answers += 1;
          nodeMistakes.html(wrong_answers);

          if (settings.end_on_wrong_answers) {
            // If only a limited amount of wrong answers is allowed,
            // check if the amount was reached.
            if (wrong_answers >= settings.end_on_wrong_answers) {
              // Reached wrong answer limit, so finish.
              finish();
              valid = -1;
            }
          }
        }
      }

      return valid;
    }


    function initNodes() {
      // Connect buttons and other listeners.
      nodeStart.click(function() {
        start();
      });

      nodeGiveup.click(function() {
        finish();
      });

      nodeRestart.click(function() {
        restart();
      });

      nodePause.click(function() {
        if (isPaused()) {
          resume();
        }
        else {
          pause();
        }
      });

      if (settings.mode == 'type') {
        nodeAnswer.keyup(function(evt) {
          onType(evt.keyCode === 13);
        });
      }
      else if (settings.mode == 'click') {
        nodeAnswers.on('click', '.question-item', function() {
          onClicked($(this));
        });
      }

      if (settings.allow_paging) {
        nodeNext.click(function() {
          nextQuestion();
        });

        nodePrev.click(function() {
          prevQuestion();
        })
      }
    }

    function init() {
      initNodes();
      updateTimerLabel();
    }

    init();
  };


  // Auto-initialize quizzes on page load.
  $(function() {
    $('.simplequiz').each(function() {
      $(this).quiz();
    })
  });

}(jQuery));
