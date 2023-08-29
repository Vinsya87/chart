$(document).ready(function () {
  $("#updateButton").click(function () {
    var selectedValue = $("#intervalSelect").val();
    var intervalParts = selectedValue.split(",");
    var startInterval = parseInt(intervalParts[0].replace("(", "").trim());
    var endInterval = parseInt(intervalParts[1].replace(")", "").trim());

    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
      type: "POST",
      url: "/new_interval/",
      data: {
        start_timestamp: startInterval,
        end_timestamp: endInterval,
        csrfmiddlewaretoken: csrfToken,
      },
      success: function (response) {
        var newData = JSON.parse(response.data_json);
        newUpdateChart(newData);
      },
      error: function (xhr, errmsg, err) {
        console.log("Error:", xhr.status + ": " + xhr.responseText);
      },
    });
  });
});

function newUpdateChart(newData) {
  var title = `${newData[0][0]} - ${newData[newData.length - 1][1]}`;

  $('#chartTitle').text(title);

myChart.data.labels = newData.map(item => `${item[0]} - ${item[1]}`);


  myChart.data.datasets[0].data = newData.map(item => item[2]);
  myChart.data.datasets[1].data = newData.map(item => item[3]);
  myChart.options.plugins.title.text = title;
  myChart.update();
  data = newData;

  myChart_back.data.labels = myChart.data.labels;
  myChart_back.data.datasets[0].data = myChart.data.datasets[0].data;
  myChart_back.data.datasets[1].data = myChart.data.datasets[1].data;
  myChart_back.options.plugins.title.text = title;
  myChart_back.update();
}

function updateIntervalAndChart(startInterval, endInterval) {
  var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  
  $.ajax({
    type: "POST",
    url: "/new_interval/",
    data: {
      start_timestamp: startInterval,
      end_timestamp: endInterval,
      csrfmiddlewaretoken: csrfToken,
    },
    success: function (response) {
      var newData = JSON.parse(response.data_json);
      newUpdateChart(newData);
    },
    error: function (xhr, errmsg, err) {
      console.log("Error:", xhr.status + ": " + xhr.responseText);
    },
  });
}

$("#nextButton").click(function () {
  var startInterval = data[0][0];
  var endInterval = data[data.length - 1][1];
  var intervalDifference = endInterval - startInterval;

  // Сдвигаем интервалы на следующий шаг
  startInterval = endInterval;
  endInterval = endInterval + intervalDifference;

  updateIntervalAndChart(startInterval, endInterval);
});

$("#prevButton").click(function () {
  var startInterval = data[0][0];
  var endInterval = data[data.length - 1][1];
  var intervalDifference = endInterval - startInterval;

  // Сдвигаем интервалы на предыдущий шаг
  endInterval = startInterval;
  startInterval = startInterval - intervalDifference;

  updateIntervalAndChart(startInterval, endInterval);
});




$(document).ready(function () {
  var chartBack = $('#chart_back');
  var isDragging = false;
  var startX = 0;
  var startTranslate = 0;
  window.addEventListener('keydown', evt => {
    if (evt.key === 'Shift') {
      chartBack.css('pointer-events', 'none');
    }
});
  $(document).keyup(function (event) {
    if (event.key === "Shift") {
      chartBack.css('pointer-events', 'auto');
    }
  });

  $(document).mousedown(function (event) {
    if ($(event.target).is(chartBack)) {
      startX = event.clientX;
      startTranslate = parseFloat(chartBack.css('transform').split(',')[4]) || 0;
  
      if (event.shiftKey) {
        // chartBack.css('pointer-events', 'none');
      } else {
        // Когда шифт не нажат (начинаем смещение)
        isDragging = true;
      }
    }
  });
      

  $(document).mousemove(function (event) {
    if (isDragging) {
      var diffX = event.clientX - startX;
      var newTranslate = startTranslate + diffX;

      chartBack.css('transform', `translateX(${newTranslate}px)`);
    }
  });

  $(document).mouseup(function () {
    if (isDragging) {
      isDragging = false;
      var dragDistance = startTranslate - (parseFloat(chartBack.css('transform').split(',')[4]) || 0);

      if (dragDistance > 100) {
        var startInterval = data[0][0];
        var endInterval = data[data.length - 1][1];
        var intervalDifference = endInterval - startInterval;

        // Сдвигаем интервалы на предыдущий шаг
        endInterval = startInterval;
        startInterval = startInterval - intervalDifference;

        updateIntervalAndChart(startInterval, endInterval);
      } else if (dragDistance < -100) {
        var startInterval = data[0][0];
        var endInterval = data[data.length - 1][1];
        var intervalDifference = endInterval - startInterval;

        // Сдвигаем интервалы на следующий шаг
        startInterval = endInterval;
        endInterval = endInterval + intervalDifference;

        updateIntervalAndChart(startInterval, endInterval);
      }

      chartBack.css('transform', 'translateX(0px)');
    }
  });
});
