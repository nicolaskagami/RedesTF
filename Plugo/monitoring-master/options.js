
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

  c.intervalo_minimo_de_stall = Number(c.intervalo_minimo_de_stall);
  c.intervalo_de_monitoramento = Number(c.intervalo_de_monitoramento);


  if(c.enviar_para_servidor == "true")
    c.enviar_para_servidor = true;
  if(c.enviar_para_servidor == "false")
    c.enviar_para_servidor = false;

  

}





// Saves options to chrome.storage
function save_options() {
  var ende = document.getElementById('endereco').value;
  chrome.storage.sync.set({
    endereco: ende,
    monitorar: $('input[name="monitorar"]:checked').val(),
    questionario: $('input[name="questionario"]:checked').val(),
    relatorio: $('input[name="relatorio"]:checked').val(),
    intervalo_minimo_de_stall: $("#intervalo_minimo_de_stall").val(),
    intervalo_de_monitoramento : $("#intervalo_de_monitoramento").val(),
    enviar_para_servidor : $("#enviar_para_servidor").prop('checked')

  }, function() {
    // Update status to let user know options were saved.
    var status = document.getElementById('status');
    status.textContent = 'Configurações salvas.';
    setTimeout(function() {
      $("#status").html("&nbsp;");
    }, 750);
  });
}

// Restores select box and checkbox state using the preferences
// stored in chrome.storage.


function restore_options() {



  chrome.storage.sync.get({
    endereco: "http://0.0.0.0:3000",
    monitorar: "true",
    questionario: "true",
    relatorio: "false",
    intervalo_minimo_de_stall : 50,
    intervalo_de_monitoramento : 1000,
    enviar_para_servidor : "true"

  }, function(items) {

    normalize(items);
    //document.getElementById('color').value = items.favoriteColor;
    //document.getElementById('like').checked = items.likesColor;
    document.getElementById('endereco').value = items.endereco;
    if(items.monitorar) {
        $('input[name="monitorar"]')[0].checked = true;
    } else {
        $('input[name="monitorar"]')[1].checked = true;
    }

    if(items.questionario) {
        $('input[name="questionario"]')[0].checked = true;
    } else {
        $('input[name="questionario"]')[1].checked = true;
    }

    if(items.relatorio) {
        $('input[name="relatorio"]')[0].checked = true;
    } else {
        $('input[name="relatorio"]')[1].checked = true;
    }

    $("#intervalo_de_monitoramento").val(items.intervalo_de_monitoramento);
    $("#intervalo_minimo_de_stall").val(items.intervalo_minimo_de_stall);

    $("#enviar_para_servidor").prop('checked', items.enviar_para_servidor);

    refresh_page();

  });
}
document.addEventListener('DOMContentLoaded', restore_options);
document.getElementById('save').addEventListener('click',
    save_options);


function refresh_page() {
      if($('input[name="monitorar"]:checked').val() == "true") {
          $("#monitorando").css('visibility','visible');
      } else {
          $("#monitorando").css('visibility','hidden');
      }
};


$('input[name="monitorar"]').change(function() {
    refresh_page();
});


