  function disableYTAutoPlay() {
      var newScript = document.createElement("script");
      newScript.type = "text/javascript";
      newScript.innerText = "if(\"ytspf\" in window){ console.log('AQUI YTSPF'); ytspf.enabled = false; ytspf.config['navigate-limit'] = 0;_spf_state.config['navigate-limit'] = 0; }";
      document.body.appendChild(newScript);
      setTimeout(function() {
          var checkBox = document.getElementById("autoplay-checkbox");
          if (checkBox && checkBox.checked == true) {
              checkBox.click();
          }
      }, 3000);
      setTimeout(function() {
          var checkBox = document.getElementById("autoplay-checkbox");
          if (checkBox && checkBox.checked == true) {
              checkBox.click();
          }
      }, 15000);
  }

  function injectCode(quality) {
      var highpref = false;
      var pause = true;
      var inj1 = document.createElement('script');
      var docFrag = document.createDocumentFragment();
      var apelacao = "var sytqQuality=2; var sytqHighPref=false;var sytqPause=false;var sytqPlayer;var sytqSpeed=1;var hooked=false;var smallTimeout=10;var mediumTimeout=100;var largeTimeout=400; function sleepFor(sleepDuration){var now = new Date().getTime();while(new Date().getTime() < now + sleepDuration){}}function fakeClick(anchorObj) {if (anchorObj.click) {anchorObj.click()} else if(document.createEvent) {var evt = document.createEvent('MouseEvents'); evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null); var allowDefault = anchorObj.dispatchEvent(evt); }}function forcePause(){if(sytqPlayer.getPlayerState()===-1){setTimeout(function(){forcePause();},largeTimeout);return;}sytqPlayer.pauseVideo();if(sytqPlayer.getPlayerState()!==2){setTimeout(function(){forcePause();},smallTimeout);return;}}function forcePlay(){console.log('Entrando');if(sytqPlayer.getPlayerState()===-1){setTimeout(function(){forcePlay();},largeTimeout);console.log('Saindo');return;}sytqPlayer.playVideo();if(sytqPlayer.getPlayerState()!==1){setTimeout(function(){forcePlay();},smallTimeout);return;}}function ytPlayerHook(player,speed,quality,highpref,pause){console.log('IN: ' + Date.now());if(hooked||typeof player!=='object')return;hooked=true;sytqSpeed=speed;sytqQuality=quality;sytqHighPref=highpref;sytqPause=pause;sytqPlayer=player;/*forcePause()*/;var lbt = document.getElementsByClassName('ytp-button'); var lbtb = null; for(i = 0; i < lbt.length; i++){ if (lbt[i].className.indexOf('ytp-settings-button') > -1){ lbtb = lbt[i]; break; } } if (lbtb == null){ return; } fakeClick(lbtb); var lbt_mi = document.getElementsByClassName('ytp-menu'); var lbt_res_menu = lbt_mi[0].children[3]; console.log('LBT RES MENU'); console.dir(lbt_res_menu); fakeClick(lbt_res_menu); var lbt_pc = document.getElementsByClassName('ytp-quality-menu'); console.dir(lbt_pc); var available_opt = []; var html_opt = lbt_pc[0].children; var next=Number.MAX_VALUE; var previous=-Number.MAX_VALUE; var result_index=null; var next_index=null; var previous_index=null; for(i = 0; i < html_opt.length; i++){var html_item = html_opt[i].innerText; var current_quality = -1; if(html_item.indexOf('144p') > -1){current_quality = 1;}else if(html_item.indexOf('240p') > -1){current_quality = 2;}else if(html_item.indexOf('360p') > -1){current_quality = 3;}else if(html_item.indexOf('480p') > -1){current_quality = 4;}else if(html_item.indexOf('720p') > -1){current_quality = 5;}else if(html_item.indexOf('1080p') > -1){current_quality = 6;}else if(html_item.indexOf('1440p') > -1){current_quality = 7;}else if(html_item.indexOf('2160p') > -1){current_quality = 8;}if(current_quality != -1){	if(current_quality == quality){result_index = i;break;}else{if(current_quality < quality && current_quality > previous){previous = current_quality;previous_index = i;}else if(current_quality > quality && current_quality < next){next = current_quality;next_index = i;}}}}console.log('Q: ' + quality + ' RI: ' + result_index);console.log('N: ' + next + ' ' + next_index);console.log('P: ' + previous + ' ' + previous_index);if(result_index == null){if(previous_index == null){if(!(next_index == null)){result_index = next_index;}}else{result_index = previous_index;}}if (!(result_index == null)){correct_option=html_opt[result_index];fakeClick(correct_option);} console.log(player.getPlaybackQuality()); forcePlay(); console.log('OUT: ' + Date.now());}";

      inj1.innerHTML = apelacao + ["\nwindow.onYouTubePlayerReady = function(player){", " /*setTimeout(function(){*/ytPlayerHook(player, " + "1" + ", " + quality + ", " + highpref + ", " + pause + ");/*},10)*/;", "}"].join('\n');
      docFrag.appendChild(inj1);
      (document.head || document.documentElement).appendChild(docFrag);
      inj1.parentNode.removeChild(inj1);
      console.log(Date.now() + " INJETANDO");
  }

  function normalize(c) {
      if (c.monitorar == "true") c.monitorar = true;
      if (c.monitorar == "false") c.monitorar = false;
      if (c.questionario == "true") c.questionario = true;
      if (c.questionario == "false") c.questionario = false;
      if (c.relatorio == "true") c.relatorio = true;
      if (c.relatorio == "false") c.relatorio = false;
      console.log(c);
      nObserver = window.MutationObserver || window.WebKitMutationObserver;
      var observer = new MutationObserver(function(mutations, observer) {
          console.log(mutations);
      });
      c.intervalo_minimo_de_stall = Number(c.intervalo_minimo_de_stall);
      c.intervalo_de_monitoramento = Number(c.intervalo_de_monitoramento);
      if (c.enviar_para_servidor == "true") c.enviar_para_servidor = true;
      if (c.enviar_para_servidor == "false") c.enviar_para_servidor = false;
      console.log(c);
  }

  function simulateCtrlShiftAltD() { // Prepare function for injection into page
      function injected() { // Adjust as needed; some events are only processed at certain elements
          var element = document.body;

          function keyEvent(el, ev) {
              var eventObj = document.createEvent("Events");
              eventObj.initEvent(ev, true, true); // Edit this to fit
              eventObj.keyCode = 68;
              eventObj.which = 68;
              eventObj.ctrlKey = true;
              eventObj.shiftKey = true;
              eventObj.altKey = true;
              el.dispatchEvent(eventObj);
          } // Trigger all 3 just in case
          keyEvent(element, "keydown");
          keyEvent(element, "keypress");
          keyEvent(element, "keyup");
      } // Inject the script
      var script = document.createElement('script');
      script.textContent = "(" + injected.toString() + ")();";
      (document.head || document.documentElement).appendChild(script);
      script.parentNode.removeChild(script);
  }

  function simulateCtrlShiftAltS() { // Prepare function for injection into page
      function injected() { // Adjust as needed; some events are only processed at certain elements
          var element = document.body;

          function keyEvent(el, ev) {
              var eventObj = document.createEvent("Events");
              eventObj.initEvent(ev, true, true); // Edit this to fit
              eventObj.keyCode = 83;
              eventObj.which = 83;
              eventObj.ctrlKey = true;
              eventObj.shiftKey = true;
              eventObj.altKey = true;
              el.dispatchEvent(eventObj);
          } // Trigger all 3 just in case
          keyEvent(element, "keydown");
          keyEvent(element, "keypress");
          keyEvent(element, "keyup");
      } // Inject the script
      var script = document.createElement('script');
      script.textContent = "(" + injected.toString() + ")();";
      (document.head || document.documentElement).appendChild(script);
      script.parentNode.removeChild(script);
  }

  function randomString(length, chars) {
      var mask = '';
      if (chars.indexOf('a') > -1) mask += 'abcdefghijklmnopqrstuvwxyz';
      if (chars.indexOf('a') > -1) mask += 'abcdefghijklmnopqrstuvwxyz';
      if (chars.indexOf('#') > -1) mask += '0123456789';
      if (chars.indexOf('!') > -1) mask += '~`!@#$%^&*()_+-={}[]:";\'<>?,./|\\';
      var result = '';
      for (var i = length; i > 0; --i) result += mask[Math.round(Math.random() * (mask.length - 1))];
      return result;
  }
  var config = null;
  var $link = null;
  var start_time = Date.now();
  var timestamp2;

  function send_questionario(end, opinion) {
      var return_object = {};
      return_object["opinion"] = opinion;
      return_object["rating"] = $('#rating').raty('score');
      return_object["conteudo"] = $("#conteudo").val();
      return_object["diario"] = $("#diario").val();
      return_object["tempo"] = $('input[name="tempo"]:checked').val();
      return_object["idade"] = $("#idade").val();
      return_object["sexo"] = $('input[name="sex"]:checked').val();
      return_object["pais"] = $("#pais").val();
      return_object["comment"] = $("#comment").val();
      chrome.runtime.sendMessage({
          action: 'questionario',
          url: end,
          type: "POST",
          data: return_object,
      }, function(responseText) {});
  }

  function local_save_questionario(timestamp, opinion) {
      $("body").append("<a href='' id='dataLink2' download='questionario-" + timestamp + ".csv'></a>");
      $link2 = $("#dataLink2");
      var saveFile = "Global,Rating,Conteudo,Tempo,Diario,Idade,Sexo,Pais,Comentarios\n";
      saveFile = saveFile + opinion + ",";
      saveFile = saveFile + $('#rating').raty('score') + ",";
      saveFile = saveFile + $("#conteudo").val() + ",";
      saveFile = saveFile + $('input[name="tempo"]:checked').val() + ",";
      saveFile = saveFile + $("#diario").val() + ",";
      saveFile = saveFile + $("#idade").val() + ",";
      saveFile = saveFile + $('input[name="sex"]:checked').val() + ",";
      saveFile = saveFile + $("#pais").val() + ",";
      saveFile = saveFile + $("#comment").val() + ",";
      $link2.attr("href", 'data:Application/octet-stream,' + encodeURIComponent(saveFile))[0].click();
  }

  function local_save(result) {
      $("body").append("<a href='' id='dataLink' download='resultados-" + result.start_timestamp + ".csv'></a>");
      $link = $("#dataLink");
      var saveFile = "Start timestamp,Netmetric,Left time,Video preload,Total played time,Total played time with stall,Total stall length,Total number of stall,Dropped frames,Video duration,Video start time\n";
      saveFile = saveFile + result.start_timestamp + ",";
      saveFile = saveFile + result.netmetric + ",";
      saveFile = saveFile + result.left_time + ",";
      saveFile = saveFile + result.video_preload + ",";
      saveFile = saveFile + result.total_played_time + ",";
      saveFile = saveFile + result.total_played_time_with_stall + ",";
      saveFile = saveFile + result.total_stall_length + ",";
      saveFile = saveFile + result.total_number_of_stall + ",";
      saveFile = saveFile + result.dropped_frames + ",";
      saveFile = saveFile + result.video_duration + ",";
      saveFile = saveFile + result.video_start_time + "\n\n";
      saveFile = saveFile + "Length of each stall\n";
      saveFile = saveFile + "Video position,Timestamp,Duration of stall\n";
      for (var i = 0; i < result.length_of_each_stall.length; i++) {
          saveFile = saveFile + result.length_of_each_stall[i].current_video_position + ",";
          saveFile = saveFile + result.length_of_each_stall[i].timestamp_of_stall + ",";
          saveFile = saveFile + result.length_of_each_stall[i].duration_of_stall + ",";
          saveFile = saveFile + "\n";
      }
      saveFile = saveFile + "\n";
      saveFile = saveFile + "Volume at time\n";
      saveFile = saveFile + "Video position,Timestamp,Volume\n";
      for (var i = 0; i < result.volume_at_time.length; i++) {
          saveFile = saveFile + result.volume_at_time[i].current_video_position + ",";
          saveFile = saveFile + result.volume_at_time[i].timestamp_of_volume + ",";
          saveFile = saveFile + result.volume_at_time[i].volume + ",";
          saveFile = saveFile + "\n";
      }
      saveFile = saveFile + "\n";
      saveFile = saveFile + "Playback quality\n";
      saveFile = saveFile + "Video position,Timestamp,Width,Height\n";
      for (var i = 0; i < result.playback_quality.length; i++) {
          saveFile = saveFile + result.playback_quality[i].current_video_position + ",";
          saveFile = saveFile + result.playback_quality[i].timestamp_of_quality + ",";
          saveFile = saveFile + result.playback_quality[i].video_width + ",";
          saveFile = saveFile + result.playback_quality[i].video_height + ",";
          saveFile = saveFile + "\n";
      }
      saveFile = saveFile + "\n";
      saveFile = saveFile + "Mute state\n";
      saveFile = saveFile + "Video position,Timestamp,State\n";
      for (var i = 0; i < result.mute_state.length; i++) {
          saveFile = saveFile + result.mute_state[i].current_video_position + ",";
          saveFile = saveFile + result.mute_state[i].timestamp_of_mute_state + ",";
          saveFile = saveFile + result.mute_state[i].state + ",";
          saveFile = saveFile + "\n";
      }
      saveFile = saveFile + "\n";
      saveFile = saveFile + "Played time interval\n";
      saveFile = saveFile + "Start,End\n";
      for (var i = 0; i < result.played_time_interval.length; i++) {
          saveFile = saveFile + result.played_time_interval[i].start + ",";
          saveFile = saveFile + result.played_time_interval[i].end + ",";
          saveFile = saveFile + "\n";
      }
      saveFile = saveFile + "\n";
      saveFile = saveFile + "Buffer time\n";
      saveFile = saveFile + "Start,End\n";
      for (var i = 0; i < result.buffer_time.length; i++) {
          saveFile = saveFile + result.buffer_time[i].start + ",";
          saveFile = saveFile + result.buffer_time[i].end + ",";
          saveFile = saveFile + "\n";
      }
      saveFile = saveFile + "\n";
      saveFile = saveFile + "Video bytes decoded per second\n";
      saveFile = saveFile + "Video position,Timestamp,Bytes decoded\n";
      for (var i = 0; i < result.video_bytes_decoded_per_second.length; i++) {
          saveFile = saveFile + result.video_bytes_decoded_per_second[i].current_video_position + ",";
          saveFile = saveFile + result.video_bytes_decoded_per_second[i].timestamp_of_video_bytes_decoded + ",";
          saveFile = saveFile + result.video_bytes_decoded_per_second[i].video_bytes + ",";
          saveFile = saveFile + "\n";
      }
      saveFile = saveFile + "\n";
      saveFile = saveFile + "Audio bytes decoded per second\n";
      saveFile = saveFile + "Video position,Timestamp,Bytes decoded\n";
      for (var i = 0; i < result.audio_bytes_decoded_per_second.length; i++) {
          saveFile = saveFile + result.audio_bytes_decoded_per_second[i].current_video_position + ",";
          saveFile = saveFile + result.audio_bytes_decoded_per_second[i].timestamp_of_audio_bytes_decoded + ",";
          saveFile = saveFile + result.audio_bytes_decoded_per_second[i].audio_bytes + ",";
          saveFile = saveFile + "\n";
      }
      saveFile = saveFile + "\n";
      saveFile = saveFile + "Time in buffer\n";
      saveFile = saveFile + "Video position,Timestamp,Remaining time in buffer\n";
      for (var i = 0; i < result.time_in_buffer.length; i++) {
          saveFile = saveFile + result.time_in_buffer[i].current_video_position + ",";
          saveFile = saveFile + result.time_in_buffer[i].timestamp_of_time + ",";
          saveFile = saveFile + result.time_in_buffer[i].remaining_time_in_buffer + ",";
          saveFile = saveFile + "\n";
      }
      saveFile = saveFile + "\n";
      saveFile = saveFile + "Video Source\n";
      saveFile = saveFile + "Index,Source\n";
      for (var i = 0; i < result.video_source.length; i++) {
          saveFile = saveFile + i + "," + result.video_source[i] + ",";
          saveFile = saveFile + "\n";
      }
      saveFile = saveFile + "\n";
      saveFile = saveFile + "Network state at time\n";
      saveFile = saveFile + "Video position,Timestamp,State\n";
      for (var i = 0; i < result.network_state_at_time.length; i++) {
          saveFile = saveFile + result.network_state_at_time[i].current_video_position + ",";
          saveFile = saveFile + result.network_state_at_time[i].timestamp_of_network_state + ",";
          saveFile = saveFile + result.network_state_at_time[i].state + ",";
          saveFile = saveFile + "\n";
      }
      saveFile = saveFile + "\n";
      saveFile = saveFile + "Frames per second\n";
      saveFile = saveFile + "Video position,Timestamp,Number of frames\n";
      for (var i = 0; i < result.frame_per_second.length; i++) {
          saveFile = saveFile + result.frame_per_second[i].current_video_position + ",";
          saveFile = saveFile + result.frame_per_second[i].timestamp_of_frame + ",";
          saveFile = saveFile + result.frame_per_second[i].number_of_frames + ",";
          saveFile = saveFile + "\n";
      }
      saveFile = saveFile + "\n";
      saveFile = saveFile + "Skip play\n";
      saveFile = saveFile + "Video position,Timestamp,Duration of skip\n";
      for (var i = 0; i < result.skip_play.length; i++) {
          saveFile = saveFile + result.skip_play[i].current_video_position + ",";
          saveFile = saveFile + result.skip_play[i].timestamp_of_skip + ",";
          saveFile = saveFile + result.skip_play[i].skip_duration + ",";
          saveFile = saveFile + "\n";
      }
      $link.attr("href", 'data:Application/octet-stream,' + encodeURIComponent(saveFile))[0].click();
      console.dir(result);
  }

  $(document).ready(function() {
      var counter = 0;
      var wait_tree_seconds;
      var start_timestamp_counter;

      /* var quality = GetURLParameter("vq");
      if (quality == null) {
          quality = 0; //auto 
      }
      console.log("QUALITY: " + quality);
      if (quality > 0 && quality <= 8) {
          injectCode(quality);
      }*/

      disableYTAutoPlay();
      chrome.runtime.sendMessage({
          action: 'getPreferences'
      }, function(response) {
          config = response;
      });
      start_timestamp_counter = setInterval(function() {
          if (document.getElementsByTagName('video').length > 0) {
              var vid = document.getElementsByTagName('video')[0];
              if (vid.currentTime > 0.05) {
                  timestamp2 = Date.now() - start_time;
                  clearInterval(start_timestamp_counter);
              }
          }
      }, 50);
      wait_tree_seconds = setInterval(function() {
          if ((counter == 200 || document.getElementsByTagName('video').length > 0) && (config != null)) {
              clearInterval(wait_tree_seconds);
              normalize(config);
              if (config.monitorar == true) {
                  start_monitor(config);
              } else {
                  console.log("Não monitorar");
              }
          } else {
              counter++;
          }
      }, 50);

      function GetURLDomain() {
          var sPageURL = window.location.hostname;
          return (sPageURL);
      }
      // From http://www.jquerybyexample.net/2012/06/get-url-parameters-using-jquery.html
      function GetURLParameter(sParam) {
          var sPageURL = window.location.search.substring(1);
          var sURLVariables = sPageURL.split('&');
          for (var i = 0; i < sURLVariables.length; i++) {
              var sParameterName = sURLVariables[i].split('=');
              if ((sParameterName[0]).toUpperCase() == sParam.toUpperCase()) {
                  return sParameterName[1];
              }
          }
          return null;
      }

      function generateUUID() {
          var d = new Date().getTime();
          var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
              var r = (d + Math.random() * 16) % 16 | 0;
              d = Math.floor(d / 16);
              return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
          });
          return uuid;
      };

      function insert_into_video_information(req) {
          xw = new XMLWriter;
          console.log("1");
          xw.startElement('test');
          var info = {
              total_played_time: req.total_played_time,
              total_played_time_with_stall: req.total_played_time_with_stall,
              total_stall_length: req.total_stall_length,
              total_number_of_stall: req.total_number_of_stall,
              video_duration: req.video_duration,
              dropped_frames: req.dropped_frames,
              buffered_time: req.first_buffer_time_end - req.total_played_time,
              audio_bytes_decoded_per_second: req.audio_bytes_decoded_per_second_mean,
              video_bytes_decoded_per_second: req.video_bytes_decoded_per_second_mean,
              res_history: req.res_history,
              frame_per_second: req.frame_per_second_mean,
              video_start_time: req.video_start_time,
          };
          xw.startElement('url').text('[PSEUDOURL]').endElement();
          xw.startElement('total_played_time').text(req.total_played_time).endElement();
          xw.startElement('total_played_time_with_stall').text(req.total_played_time_with_stall).endElement();
          xw.startElement('total_stall_length').text(req.total_stall_length).endElement();
          xw.startElement('total_number_of_stall').text(req.total_number_of_stall).endElement();
          xw.startElement('video_duration').text(req.video_duration).endElement();
          xw.startElement('dropped_frames').text(req.dropped_frames).endElement();
          xw.startElement('buffered_time').text(info.buffered_time).endElement();
          xw.startElement('audio_bytes_decoded_per_second').text(req.audio_bytes_decoded_per_second_mean).endElement();
          xw.startElement('video_bytes_decoded_per_second').text(req.video_bytes_decoded_per_second_mean).endElement();
          xw.startElement('frames_per_second').text(req.frame_per_second_mean).endElement();
          xw.startElement('res_history').text(req.res_history).endElement();
          xw.startElement('video_start_time').text(req.video_start_time).endElement();
          xw.startElement('status').text('OK').endElement();
          if (!(req.netmetric == null)) {
              xw.myuuid = req.netmetric;
          } else {
              xw.myuuid = "untracked-" + generateUUID();
          }
          xw.endElement();
          console.dir(xw);
          return (xw);
      }

      function sleepFor(sleepDuration) {
          var now = new Date().getTime();
          while (new Date().getTime() < now + sleepDuration) { /* do nothing */ }
      }

      function start_monitor(configuration) {
          var send_to_server = configuration.enviar_para_servidor;
          var has_already_sent_to_server = false;
          //simulateCtrlShiftAltS();
          if (document.getElementsByTagName('video')[0] != null) {
              var url = document.URL;
              var video_element = document.getElementsByTagName('video')[0];
              console.log("VE:");
              console.dir(video_element);
              var time_interval = configuration.intervalo_de_monitoramento; //In miliseconds
              var netflix_element = $('#netflix-player');
              var pinfo_element = $('.player-info');
              /* var lbt = $('.ytp-button.ytp-settings-button');
              lbt.click();
              var aux = $('.ytp-menu');
              console.log("AUX");
              console.dir(aux);
              console.log("END AUX");*/
              /* var lbt_mi = $('.ytp-menu');
              var lbt_res_menu = lbt_mi[0].children[3];
              lbt_res_menu.click();
              var lbt_pc = $('.ytp-menu.ytp-quality-menu');
              var opt720p = lbt_pc[0].children[5];
              console.dir(opt720p);
              opt720p.click();*/
              /* console.dir(pinfo_element);
              pinfo_element = $('.player-info');
              pstream_element = $('.player-streams');
              console.log("aiahgiau");
              console.dir(pstream_element);
              options_array = pstream_element[0].childNodes[0].children[1].children[1];
              var jopt = $(options_array);
              html_geral = '';*/
              var monitor = new Monitor(video_element, url, netflix_element, pinfo_element, null, '');
              var uuid = GetURLParameter('uuid');
              var minname = GetURLParameter('minname');
              console.log("MN: " + minname);
              monitor.setNetmetricId(uuid, minname);
              $(window).on('beforeunload', function() {
                  var dt = monitor.json();
                  xmlvar = insert_into_video_information(dt);
                  chrome.runtime.sendMessage({
                      action: "send_to_local",
                      data: xmlvar
                  });
                  monitor.set_left_time();
                  monitor.stop_all_monitoring();
                  monitor.set_startup_time(timestamp2);
                  return "Você quer MESMO sair?";
              });
              //Start all monitoring process
              console.log("IMS: " + configuration.intervalo_minimo_de_stall);
              monitor.start_all_monitoring(time_interval, 150 /*configuration.intervalo_minimo_de_stall*/ );
              document.getElementsByTagName('video')[0].addEventListener("ended", function() {
                  monitor.stop_all_monitoring();
                  monitor.set_startup_time(timestamp2);
                  console.log(monitor.json());
                  if (configuration.relatorio) {
                      local_save(monitor.json());
                  }
                  var dt = monitor.json();
                  if (send_to_server && !has_already_sent_to_server) {
                      has_already_sent_to_server = true;
                      chrome.runtime.sendMessage({
                          action: 'monitor',
                          url: configuration.endereco,
                          type: "POST",
                          data: dt,
                      }, function(responseText) { /*Callback function to deal with the response*/ });
                  }
                  if ( /*configuration.questionario*/ false) {
                      BootstrapDialog.show({
                          title: "Qualidade de experiência",
                          message: $('<div></div>').load(chrome.extension.getURL("remote.html")),
                          closable: true,
                          closeByBackdrop: false,
                          closeByKeyboard: false,
                          buttons: [{
                              label: 'Boa',
                              cssClass: 'btn-primary',
                              action: function(dialogItself) {
                                  if (configuration.relatorio) {
                                      local_save_questionario(monitor.json().start_timestamp, "Boa");
                                  }
                                  if (configuration.enviar_para_servidor) {
                                      send_questionario(configuration.endereco, "Boa");
                                  }
                                  dialogItself.close();
                              }
                          }, {
                              label: 'Ruim',
                              cssClass: 'btn-danger',
                              action: function(dialogItself) {
                                  if (configuration.relatorio) {
                                      local_save_questionario(monitor.json().start_timestamp, "Ruim");
                                  }
                                  if (configuration.enviar_para_servidor) {
                                      send_questionario(configuration.endereco, "Ruim");
                                  }
                                  dialogItself.close();
                              }
                          }, {
                              label: 'Cancelar',
                              action: function(dialogItself) {
                                  dialogItself.close();
                              }
                          }]
                      });
                  }
              });
          }
      }
  });
