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

function api_error(msg){
    $('#overlay_text').html(msg);
    $('#overlay').css("display", "block");
    console.error(msg);
}

function call_error(data){
    api_error(data.statusText);
}

function dissmiss_error(){
    $('#overlay').css("display", "none");
}

function do_fail(msg){
    alert(msg);
}

var STOP_CONFIG =       {
    'bgcolor': '#ff0000',
    'display': 'STOP',
    'font_color': '#ffffff',
    'name': 'OFF_ANIM',
    'valid': true
};

function show_btn_loading(id){
    $('#' + id).html('<i class="fa fa fa-refresh fa-spin"></i>');
}

function hide_btn_loading(id){
    var display = $('#' + id).attr('display');
    $('#' + id).html(display);
}

function add_button(config, click_func, dest='#button_list'){
    var div = document.createElement('div');
    div.className = 'btn';
    div.style.background = config.bgcolor;
    div.style.color = config.font_color;
    $(div).html(config.display);
    $(div).attr('display', config.display);
    div.id = 'button_' + config.name;
    if(config.valid){
        div.addEventListener('click', function(){
            click_func(config.name, $(this).attr('id'))
        });
    }
    $(dest).append(div);
}

function brightness_change(val){
    var success = function(resp){
        if(!resp.status){
            api_error(resp.msg);
        }
    }

    call_api('/api/brightness/' + val, success, call_error);
}

function do_main(){
    var slider = noUiSlider.create($('#brightness')[0], {
        direction: 'rtl', // Put '0' at the bottom of the slider
        orientation: 'vertical', // Orient the slider vertically
        start: 255,
        connect: [true, false],
        range: {
            'min': 0,
            'max': 255
        },
        behaviour: 'drag-tap'
    });

    var slider = $('#brightness')[0].noUiSlider;

    var success = function(resp){
        if(resp.status){
            var config = resp.data;

            document.body.style.background = config.ui.bgcolor;
            document.body.style.color = config.ui.font_color;
            $('#title').text(config.ui.title);
            document.title = config.ui.title;
            add_button(STOP_CONFIG, stop_animation);
            for(i=0; i < config.animations.length; i++){
                console.log(config.animations[i]);
                add_button(config.animations[i], run_animation);
            }

            slider.set(config.brightness);
            slider.on('set', function(){
                brightness_change(Math.round(slider.get()));
            });
            $('#overlay').click(dissmiss_error);

            hide_loading();
        }
        else{
            hide_loading();
            api_error(resp.msg + '<br />Check the server or try reloading');
        }
    };

    call_api('/api/get_config', success, call_error);
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
