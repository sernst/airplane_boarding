(function () {
  var STATES = ['hidden', 'seating', 'wait', 'interchanging', 'seated'];
  var svgContainer;
  var delayTimeout;
  var passenger_count;
  var max_seats;
  var maxTime;
  var interval;
  var playSpeed = 160;
  var delta = -30;
  var time = -1;
  var passengers = [];
  var seat_positions = [];
  var aisle_positions = [];


  /**
   * Creates each seat in the airplane in the appropriate arrangement
   * given the specified project settings
   */
  function draw_seats() {
    var sections = window.project.settings.airplane;
    var xOff = Math.abs(delta);
    var height = 0;

    function addRowOfSeats(count, yOff, maxCount) {
      var seatIndex;
      var padding = Math.min(0, 0.5 * delta * (maxCount - count));

      yOff += padding;
      for (seatIndex = 0; seatIndex < count; seatIndex++) {
        seat_positions.push({'x': xOff, 'y': yOff});

        var circle = svgContainer.append('circle')
            .attr('cx', xOff)
            .attr('cy', yOff)
            .attr('r', 0.4 * Math.abs(delta))
            .classed('seat', true);
        yOff += delta;
        height = Math.min(yOff, height);
      }
      return yOff + padding;
    }

    sections.forEach(function (section) {
      var rowIndex, i, yOff;

      for (rowIndex = 0; rowIndex < section.rows; rowIndex++) {
        yOff = delta;
        for (i = 0; i < section.seats.length; i++) {
          yOff = addRowOfSeats(
              section.seats[i],
              yOff,
              max_seats[i]
          );

          if (i < section.seats.length - 1) {
            aisle_positions.push({'x': xOff, 'y': yOff});
            yOff += delta;
          }

        }
        xOff += Math.abs(delta);
      }
    });

    svgContainer.attr(
        'viewBox',
        '0 ' + height + ' ' + xOff + ' ' + Math.abs(height)
    );
  }


  /**
   * Add a circle token for each passenger in the boarding process and
   * set their initial position and visibility for time = 0.
   */
  function draw_passengers() {
    var i;

    for (i = 0; i < passenger_count; i++) {
      passengers.push(svgContainer.append('circle')
        .attr('cx', aisle_positions[0].x)
        .attr('cy', aisle_positions[0].y)
        .attr('r', 6)
        .classed("passenger", true)
        .classed("hidden", true)
      );
    }
  }


  /**
   * Converts the raw time (in seconds) to a friendly display time in the
   * format HH:MM:SS
   *
   * @param raw
   * @returns {string}
   */
  function displayTime(raw) {
    var hours = Math.floor(raw / 3600);
    raw -= hours * 3600;
    hours = (hours < 10 ? '0' : '') + hours;
    var minutes = Math.floor(raw / 60);
    raw -= minutes * 60;
    minutes = (minutes < 10 ? '0' : '') + minutes;
    var seconds = Math.floor(raw);
    seconds = (seconds < 10 ? '0' : '') + seconds;
    return hours + ':' + minutes + ':' + seconds;
  }


  /**
   * Updates the passenger status with the specified options. Any option that
   * is not explicitly included in the options object will be set to false,
   * overriding any previously set value
   *
   * @param passenger
   * @param options
   */
  function updatePassengerStatus(passenger, options) {
    STATES.forEach(function (s) {
      if (options.hasOwnProperty(s)) {
        return passenger.classed(s, options[s]);
      }
      return passenger.classed(s, false);
    });
  }


  /**
   * Moves the specified passenger to the given position (x, y) in the display.
   * The move is animated differently based on the playback state, the playback
   * speed, and whether or not the animation step is forward or backward in
   * time.
   *
   * @param passenger
   * @param x
   * @param y
   * @param forward
   * @returns {*}
   */
  function movePassenger(passenger, x, y, forward) {
    var duration = (interval ? Math.floor(0.4 * playSpeed) : 500);

    if (forward) {
      return passenger
          .transition().duration(duration).attr('cx', x)
          .transition().duration(duration).attr('cy', y);
    }

    return passenger
        .transition().duration(duration).attr('cy', y)
        .transition().duration(duration).attr('cx', x);
  }


  /**
   * Updates the animation display for the specified time. If the time is the
   * same as the previous time, nothing happens.
   */
  function update(newTime) {
    var lastTime = time;
    var airplaneLayout = $('#airplane-layout');

    time = Math.max(0, Math.min(newTime, maxTime));
    if (newTime > 0 && lastTime === time) {
      return false;
    }

    airplaneLayout.find('.time').html(displayTime(time));
    airplaneLayout.find('.speed').html(
        (0.01 * Math.round(100 * 1000 / playSpeed)).toFixed(2)
    );

    window.project.progress.forEach(function (positions, index) {
      var status = {};
      var passenger = passengers[index];
      var state = positions[time].split(':');
      var pos = parseInt(state[1], 10);

      var finalPos = parseInt(
          positions[positions.length - 1].split(':')[1]
      );

      var move = [
        aisle_positions[Math.max(0, pos)].x,
        aisle_positions[Math.max(0, pos)].y
      ];

      switch (state[0]) {
        case 'Q':
          status.wait = (
            time > 0 &&
            (positions[time - 1] === positions[time])
          );
          status.seating = status.wait && (finalPos === pos);
          status.wait = status.wait && !status.seating;
          status.hidden = pos < 0;
          break;

        case 'O':
          status.interchanging = true;
          move = [];
          break;

        case 'I':
          status.interchanging = true;
          break;

        case 'S':
          status.seated = true;
          move = [
              seat_positions[index].x,
              seat_positions[index].y
          ];
          break;
      }

      updatePassengerStatus(passenger, status);

      if (move.length > 1) {
        movePassenger(passenger, move[0], move[1], time > lastTime);
      }

    });

    return true;
  }


  /**
   * Starts the playback of the animation at the last specified time. If the
   * time has reached the maximum simulation time, the playback will start over
   * from the beginning.
   */
  function start_animation() {
    if (time === maxTime) {
      update(0);
    }

    $('#airplane-controls')
        .find('.play-button .icon')
        .html('pause');

    if (interval) {
      return;
    }

    interval = setInterval(function () {
      if (!update(time + 1)) {
        stop_animation();
      }
    }, playSpeed);
  }


  /**
   * Pauses the animation playback at the current time.
   */
  function stop_animation() {
    $('#airplane-controls')
        .find('.play-button .icon')
        .html('play_arrow');

    if (interval) {
      clearInterval(interval);
      interval = null;
    }
  }


  /**
   * Handles the user input actions from the available playback control buttons
   *
   * @param event
   * @returns {*}
   */
  function onButtonClick(event) {
    var e = $(event.currentTarget);
    var change = parseInt(e.attr('data-delta'));
    var role;

    if (delayTimeout) {
      clearTimeout(delayTimeout);
    }

    if (change !== 0) {
      return update(time + change);
    }

    role = e.attr('data-role');
    if (role === 'slower') {
      playSpeed += 20;
    } else if (role === 'faster') {
      playSpeed = Math.max(40, playSpeed - 20);
    } else if (role == 'toggle') {
      return interval ? stop_animation() : start_animation();
    }

    stop_animation();

    delayTimeout = setTimeout(start_animation, 2 * playSpeed);
  }


  /**
   * The initialization function, which is called when the CAULDRON notebook
   * display is fully loaded and ready for interaction
   */
  window.CAULDRON.on.ready.then(function () {
    passenger_count = window.project.passenger_count;
    max_seats = window.project.status.max_seats_in_row;
    maxTime = window.project.status.elapsed;
    svgContainer = d3.select($('#airplane-layout')[0])
        .append("svg")
        .attr('version', '1.1');

    $('#airplane-controls').find('.button').click(onButtonClick);

    draw_seats();
    draw_passengers();
    update(0);
  });

}());
