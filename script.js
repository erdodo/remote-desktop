$(document).ready(function () {
  fetch("/ip_address.json")
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      $("#ipAddress").text(data.ip_address);
    });
  var startX, startY;
  let isMove = false;

  $("#mouseBox").on("touchstart", function (event) {
    event.preventDefault();
    var touch = event.originalEvent.touches[0];
    startX = touch.pageX;
    startY = touch.pageY;
  });

  $("#mouseBox").on("touchmove", function (event) {
    event.preventDefault();
    isMove = true;
    var touch = event.originalEvent.touches[0];
    var x = touch.pageX - startX;
    var y = touch.pageY - startY;
    startX = touch.pageX;
    startY = touch.pageY;
    const speed = $("#mouseSpeed").val();
    console.log(speed);
    $.post($("#ipAddress").text() + "/mouse_move", { x: x * speed, y: y * speed }, function (data, status) {
      console.log("Data: " + data + "\nStatus: " + status);
    });
  });

  let lastTouchEnd = 0;
  let count = 0;
  $("#mouseBox").on("touchend", function (event) {
    if (isMove) {
      isMove = false;
      return;
    }
    $.post($("#ipAddress").text() + "/mouse_click", { button: "left" }, function (data, status) {
      console.log("Data: " + data + "\nStatus: " + status);
    });
  });

  $("#mediaButton").click(function () {
    resetFooterSelect();
    if ($("#mediaBox")[0].style.display == "grid") {
      $("#mediaBox")[0].style.display = "none";
      return;
    }
    $("#mediaButton").css("border", "1px solid #000000");
    $("#mediaBox")[0].style.display = "grid";
  });

  $("#browserButton").click(function () {
    resetFooterSelect();
    if ($("#browserBox")[0].style.display == "grid") {
      $("#browserBox")[0].style.display = "none";
      return;
    }
    $("#browserButton").css("border", "1px solid #000000");
    $("#browserBox")[0].style.display = "grid";
  });

  $("#keyboardButton").click(function () {
    resetFooterSelect();
    $("#keyboardBox").focus();
    $("#test").text(initialViewportHeight + " - " + window.innerHeight);
    setTimeout(() => {
      $("#test").text(initialViewportHeight + " - " + window.innerHeight);
    }, 1000);
  });

  $("#keyboardBox").on("keyup", function (e) {
    if (e.key == "Enter") {
      const val = $("#keyboardBox").val();
      $.post($("#ipAddress").text() + "/keyboard_type", { keys: val }, function (data, status) {
        console.log("Data: " + data + "\nStatus: " + status);
      });
      $("#keyboardBox")[0].value = "";
    }
  });

  $("#functionButton").click(function () {
    resetFooterSelect();
    if ($("#functionBox")[0].style.display == "grid") {
      $("#functionBox")[0].style.display = "none";
      return;
    }
    $("#functionButton").css("border", "1px solid #000000");
    $("#functionBox")[0].style.display = "grid";
  });

  $("#appListButton").click(function () {
    resetFooterSelect();
    $.post($("#ipAddress").text() + "/app_list", function (data, status) {
      data.forEach((element) => {
        $("#appListBox").append('<button class="appButton" onclick="openApp(\'' + element + "')\">" + element + "</button>");
      });
      if ($("#appListBox")[0].style.display == "grid") {
        $("#appListBox")[0].style.display = "none";
        return;
      }
      $("#appListButton").css("border", "1px solid #000000");
      $("#appListBox")[0].style.display = "grid";
    });
  });
});

function keyPress(key) {
  $.post($("#ipAddress").text() + "/press_key", { key: key }, function (data, status) {
    console.log("Data: " + data + "\nStatus: " + status);
  });
}

function mousePress(key) {
  $.post($("#ipAddress").text() + "/mouse_click", { button: key }, function (data, status) {
    console.log("Data: " + data + "\nStatus: " + status);
  });
}

function openApp(appName) {
  $.post($("#ipAddress").text() + "/app_select", { app_name: appName }, function (data, status) {
    console.log("Data: " + data + "\nStatus: " + status);
  });
}

function resetFooterSelect() {
  $("#appListButton").css("border", "none");
  $("#appListBox").css("display", "none");

  $("#mediaButton").css("border", "none");
  $("#mediaBox").css("display", "none");

  $("#browserButton").css("border", "none");
  $("#browserBox").css("display", "none");

  $("#keyboardButton").css("border", "none");

  $("#functionButton").css("border", "none");
  $("#functionBox").css("display", "none");
}
