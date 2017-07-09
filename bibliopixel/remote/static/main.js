var ___printAPIOutput = true;

function call_api(path, success, error) {

  function callSuccess(data) {
    if (!data['status']) {
      console.log(data)
    }
    if (___printAPIOutput) console.log(JSON.stringify(data));
    success(data);
  }

  if (___printAPIOutput) console.log(path)

  $.ajax({
    type: 'GET',
    url: path,
    dataType: 'json',
    success: callSuccess,
    error: error
  });
}

function show_loading(){ $('body').addClass('loading'); }
function hide_loading(){ $('body').removeClass('loading'); }

function api_error(data){
    console.error(data);
}

function do_fail(msg){
    alert(msg);
}

var STOP_CONFIG =       {
    'bgcolor': '#ff0000',
    'display': 'STOP',
    'font_color': '#ffffff',
    'name': 'OFF_ANIM'
};

function show_btn_loading(id){
    $('#' + id).html('<i class="fa fa fa-refresh fa-spin"></i>');
}

function hide_btn_loading(id){
    var display = $('#' + id).attr('display');
    $('#' + id).html(display);
}

function add_button(config, click_func){
    var div = document.createElement('div');
    div.className = 'btn';
    div.style.background = config.bgcolor;
    div.style.color = config.font_color;
    $(div).html(config.display);
    $(div).attr('display', config.display);
    div.id = 'button_' + config.name;
    div.addEventListener('click', function(){
        click_func(config.name, $(this).attr('id'))
    });
    $('#button_list').append(div);
}

function do_main(){
    var success = function(resp){
        if(resp.status){
            var config = resp.data;

            document.body.style.background = config.ui.bgcolor;
            document.body.style.color = config.ui.font_color;
            $('#Title').text(config.ui.title);
            document.title = config.ui.title;
            add_button(STOP_CONFIG, stop_animation);
            for(i=0; i < config.animations.length; i++){
                console.log(config.animations[i]);
                add_button(config.animations[i], run_animation);
            }
            hide_loading();
        }
        else{
            do_fail(resp.msg);
        }
    };

    call_api('/api/get_config', success, api_error);
}

function run_animation(name, id){
    var success = function(data){
        if(data.status){
            // console.log(data);
        }
        else{
            api_error(data.msg);
        }

        hide_btn_loading(id);
    }

    show_btn_loading(id);
    call_api(
        '/run_animation/' + name,
        success,
        api_error
    );
}

function stop_animation(name, id){
    var success = function(data){
        if(data.status){
            // console.log(data);
        }
        else{
            api_error(data.msg);
        }

        hide_btn_loading(id);
    }

    show_btn_loading(id);
    call_api(
        '/stop',
        success,
        api_error
    );
}

$(document)
    .ready(function(){
        do_main();
    });
