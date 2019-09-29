
// var SERVER_API_IP = "http://192.168.0.4:8389/works/api/";
var SERVER_API_IP = "http://34.66.89.187:8389/works/api/";

  function loadWorkTime(csrf_token) {
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
      if ( xhttp.readyState == 4 && xhttp.status ==201) {
        var response = JSON.parse(xhttp.responseText);
        console.log(response)
        document.getElementById("currentTimeWork").innerHTML = response.currentTime;              
        }
      }

      xhttp.open("POST",  SERVER_API_IP + "currentTime", false);
      xhttp.setRequestHeader("Content-type", "application/json");
    //   var csrf_token = '{{csrf_token}}';
      xhttp.setRequestHeader("X-CSRFToken",csrf_token);
      xhttp.send();
    };

    function workStartButton(csrf_token){
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
      if ( xhttp.readyState == 4 && xhttp.status ==201) {
        var response = JSON.parse(xhttp.responseText);
        console.log(response)
        document.getElementById("currentTimeWork").innerHTML = "출근 하셨습니다."              
        }
        else if(xhttp.status==400)
        {
          alert("이미 출근 하셨습니다.")
        }
      }
      
      xhttp.open("POST", SERVER_API_IP + "start", false);
      xhttp.setRequestHeader("Content-type", "application/json");
    //   var csrf_token = '{{csrf_token}}';
      xhttp.setRequestHeader("X-CSRFToken",csrf_token);
      xhttp.send();
    };

    function workEndButton(csrf_token){
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
      if ( xhttp.readyState == 4 && xhttp.status ==201) {
        var response = JSON.parse(xhttp.responseText);
        console.log(response)
        document.getElementById("currentTimeWork").innerHTML = "퇴근 하셨습니다.";              
        }
      };

      xhttp.open("POST", SERVER_API_IP + "end", false);
      xhttp.setRequestHeader("Content-type", "application/json");
    //   var csrf_token = '{{csrf_token}}';
      xhttp.setRequestHeader("X-CSRFToken",csrf_token);
      xhttp.send();
    };

    function breakStartButton(csrf_token){
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
      if ( xhttp.readyState == 4 && xhttp.status ==201) {
        var response = JSON.parse(xhttp.responseText);
        console.log(response)
        document.getElementById("currentTimeBreak").innerHTML = "Break Start !!(" + response.serverTime +")";              
        }
        else if(xhttp.status==400)
        {
          alert("이미 쉬는 중입니다.")
        }
      }
      
      xhttp.open("POST", SERVER_API_IP + "break/start", false);
      xhttp.setRequestHeader("Content-type", "application/json");
    //   var csrf_token = '{{csrf_token}}';
      xhttp.setRequestHeader("X-CSRFToken",csrf_token);
      xhttp.send();
    };

    function breakEndButton(csrf_token){
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
      if ( xhttp.readyState == 4 && xhttp.status ==201) {
        var response = JSON.parse(xhttp.responseText);
        console.log(response)
        document.getElementById("currentTimeBreak").innerHTML = "Break End !! (" + response.serverTime +")";              
        }
      };

      xhttp.open("POST", SERVER_API_IP + "break/end", false);
      xhttp.setRequestHeader("Content-type", "application/json");
    //   var csrf_token = '{{csrf_token}}';
      xhttp.setRequestHeader("X-CSRFToken",csrf_token);
      xhttp.send();
    };

    function loadBreakTime(csrf_token) {
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
      if ( xhttp.readyState == 4 && xhttp.status ==201) {
        var response = JSON.parse(xhttp.responseText);
        console.log(response)
        document.getElementById("currentTimeBreak").innerHTML = response.currentTime;              
        }
      }

      xhttp.open("POST",  SERVER_API_IP + "break/total", false);
      xhttp.setRequestHeader("Content-type", "application/json");
    //   var csrf_token = '{{csrf_token}}';
      xhttp.setRequestHeader("X-CSRFToken",csrf_token);
      xhttp.send();
    };

    function dayOffButton(csrf_token) {
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
      if ( xhttp.readyState == 4 && xhttp.status ==201) {
        var response = JSON.parse(xhttp.responseText);
        console.log(response)
        document.getElementById("currentTimeWork").innerHTML = "DAY OFF!";              
        }
      }

      if(confirm("Day Off 및 휴가 처리 하시겠습니까?"))
      {
        xhttp.open("POST",  SERVER_API_IP + "dayoff", false);
        xhttp.setRequestHeader("Content-type", "application/json");
        // var csrf_token = '{{csrf_token}}';
        xhttp.setRequestHeader("X-CSRFToken",csrf_token);
        xhttp.send();
      }
    };

    function totalWorkTime(csrf_token) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if ( xhttp.readyState == 4 && xhttp.status ==201) {
          var response = JSON.parse(xhttp.responseText);
          console.log(response)
          document.getElementById("prefixItem").innerHTML = response.serverDate + "의 근무시간은!"
          document.getElementById("currentTimeWork").innerHTML = response.currentTime;              
          }
        }
  
        xhttp.open("POST",  SERVER_API_IP + "total", false);
        xhttp.setRequestHeader("Content-type", "application/json");
          // var csrf_token = '{{csrf_token}}';
        xhttp.setRequestHeader("X-CSRFToken",csrf_token);
        xhttp.send();
        
      };

    function getPersonId(cookieName){
      cookieName = cookieName + '=';
      var cookieData = document.cookie;
      var start = cookieData.indexOf(cookieName);
      var cookieValue = '';
      if(start != -1){
        start += cookieName.length;
        var end = cookieData.indexOf(';', start);
        if(end == -1) end = cookieData.length;
        cookieValue = cookieData.substring(start, end);
      }
      return cookieValue;
    }

    