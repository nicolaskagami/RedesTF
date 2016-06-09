/**
 * Possible parameters for request:
 *  action: "xhttp" for a cross-origin HTTP request
 *  method: Default "GET"
 *  url   : required, but not validated
 *  data  : data to send in a POST request
 *
 * The callback function is called upon completion of the request */

var config = null;
var monitor_questionario_join = null;

chrome.storage.sync.get({
    endereco: "http://0.0.0.0:3000",
    monitorar: true,
    questionario: true,
    relatorio: false,
    intervalo_minimo_de_stall : 50,
    intervalo_de_monitoramento : 1000,
    enviar_para_servidor : true
}, function(items) {
        config = items;
});

chrome.storage.onChanged.addListener(function(changes, namespace) {
        for (key in changes) {
          var storageChange = changes[key];
          config[key] = storageChange.newValue;
        }
});


function normalize(c) {
    if(c.monitorar == "true")
        c.monitorar = true;
    if(c.monitorar == "false")
        c.monitorar = false;

    if(c.questionario == "true")
        c.questionario = true;
    if(c.questionario == "false")
        c.questionario = false;

    if(c.relatorio == "true")
        c.relatorio = true;
    if(c.relatorio == "false")
        c.relatorio = false;

    console.log(c);

    c.intervalo_minimo_de_stall = Number(c.intervalo_minimo_de_stall);
    c.intervalo_de_monitoramento = Number(c.intervalo_de_monitoramento);


    if(c.enviar_para_servidor == "true")
        c.enviar_para_servidor = true;
    if(c.enviar_para_servidor == "false")
        c.enviar_para_servidor = false;


}




chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    console.log(request);

    if (request.action == "monitor") {
        $.ajax({
            url: request.url + "/api/" + request.action,
            type: request.type,
            data: JSON.stringify(request.data),
            contentType: "application/json",
            success: function(result) {
                console.log(result);
                monitor_questionario_join = $.parseJSON(result);
            }

        });
       
    }

    if (request.action == "questionario") {
        normalize(config)
        if(config.monitorar && monitor_questionario_join != null) {
            request.data["timestamp"] = monitor_questionario_join["timestamp"];
            request.data["hash"] = monitor_questionario_join["hash"];
            request.data["ip"] = monitor_questionario_join["ip"];
        } else {
            request.data["timestamp"] = "";
            request.data["hash"] = "";
            request.data["ip"] = "";
        }

        $.ajax({
            url: request.url + "/api/" + request.action,
            type: request.type,
            data: JSON.stringify(request.data),
            contentType: "application/json",
            success: function(result) {
               
            }
        });
        
    }
    
    if(request.action == "getPreferences") {
        sendResponse(config);
    }
});

